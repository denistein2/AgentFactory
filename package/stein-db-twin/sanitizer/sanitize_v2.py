#!/usr/bin/env python3
"""
Sanitizador v0.2 — Banco Gêmeo dos Agentes, Stein Technology.

Correções sobre v0.1 (auditoria GPT + schema real #7767):
  1. FAIL-CLOSED REAL: uma allowlist de colunas "conhecidas seguras" (catálogo) + o
     column_map. Qualquer coluna cujo NOME bate padrão de PII e que NÃO está nem no
     column_map nem na allowlist -> PARA e reporta (não deixa passar).
  2. MÁSCARA TIPADA: 'date' gera data sintética válida (não texto), preservando o tipo
     da coluna no restore.
  3. VARREDURA RESIDUAL no próprio sanitizador (regex real de email/cpf/cnpj), não no
     PowerShell -SimpleMatch quebrado. Se achar padrão de PII no OUTPUT, aborta.
  4. Mapa de PII vem do schema real (#7767), inclui orders/cashier_sessions/pix_config.

Uso:
    python3 sanitize_v2.py --self-test
    python3 sanitize_v2.py --in dump.sql --out snap.sql --config columns.json --manifest m.json
"""

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone, date


# --------------------------- maskers -----------------------------------------

def _h(v, salt): return hashlib.sha256((salt + "|" + v).encode()).hexdigest()[:12]

def mask_name(v, s):    return v if not v else f"Cliente Teste {_h(v,s)[:6].upper()}"
def mask_email(v, s):   return v if not v else f"user_{_h(v,s)}@example.invalid"
def mask_phone(v, s):
    if not v: return v
    d = re.sub(r"\D", "", v)
    return "0" * max(len(d), 8)
def mask_doc(v, s):
    if not v: return v
    d = re.sub(r"\D", "", v)
    t = _h(v, s)
    nums = "".join(str(int(c, 16) % 10) for c in t)
    while len(nums) < len(d): nums += nums
    return nums[:len(d)] if d else v
def mask_address(v, s): return v if not v else f"Endereco Teste {_h(v,s)[:6].upper()}"
def mask_freetext(v, s):return v if not v else f"[sanitizado {_h(v,s)[:6]}]"
def mask_date(v, s):
    """Data sintética VÁLIDA e determinística (preserva tipo date no restore)."""
    if not v: return v
    hv = int(_h(v, s), 16)
    year = 1970 + (hv % 40)          # 1970..2009
    month = 1 + (hv // 40) % 12
    day = 1 + (hv // 480) % 28        # 1..28 evita mês curto
    return date(year, month, day).isoformat()

MASKERS = {
    "name": mask_name, "email": mask_email, "phone": mask_phone,
    "doc": mask_doc, "address": mask_address, "freetext": mask_freetext,
    "date": mask_date,
}

# padrões de nome de coluna que DISPARAM suspeita de PII (para o fail-closed)
PII_NAME_PATTERNS = re.compile(
    r"(email|mail|phone|telefone|fone|celular|cpf|cnpj|document|"
    r"address|endereco|logradouro|bairro|cep|birth|nascim|operator_email|"
    r"customer_name|merchant_name)",
    re.IGNORECASE,
)

# regex de PII para varredura do OUTPUT (fail-closed pós-sanitização)
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@(?!example\.invalid)[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
CPF_RE   = re.compile(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b")
CNPJ_RE  = re.compile(r"\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b")


COPY_START = re.compile(
    r"^COPY\s+(?P<table>[\w\.\"]+)\s*\((?P<cols>[^)]*)\)\s+FROM\s+stdin;", re.IGNORECASE)

def _split_cols(s): return [c.strip().strip('"') for c in s.split(",")]


def sanitize_stream(lines, column_map, salt, drop_tables, allow_catalog):
    out, stats = [], {"cells_masked": 0, "tables_masked": {}, "tables_dropped": {},
                      "failclosed_hits": []}
    i, n = 0, len(lines)
    while i < n:
        line = lines[i]
        m = COPY_START.match(line.strip())
        if not m:
            out.append(line); i += 1; continue

        table = m.group("table").strip().strip('"').replace('"', "")
        cols = _split_cols(m.group("cols"))
        out.append(line)

        # FAIL-CLOSED: colunas suspeitas de PII não classificadas
        colmap = column_map.get(table, {})
        for c in cols:
            full = f"{table}.{c}"
            if PII_NAME_PATTERNS.search(c):
                classified = (c in colmap) or (full in allow_catalog)
                if not classified:
                    stats["failclosed_hits"].append(full)

        # corpo
        body = []; i += 1
        while i < n and lines[i].rstrip("\n") != r"\.":
            body.append(lines[i]); i += 1
        terminator = lines[i] if i < n else "\\.\n"

        if table in drop_tables:
            stats["tables_dropped"][table] = len(body)
            out.append(terminator); i += 1; continue

        mask_idx = {cols.index(c): t for c, t in colmap.items() if c in cols}
        rows_masked = 0
        for row in body:
            if mask_idx:
                fields = row.rstrip("\n").split("\t")
                changed = False
                for idx, mtype in mask_idx.items():
                    if idx < len(fields) and fields[idx] != r"\N":
                        nv = MASKERS[mtype](fields[idx], salt)
                        if nv != fields[idx]:
                            fields[idx] = nv; stats["cells_masked"] += 1; changed = True
                if changed: rows_masked += 1
                out.append("\t".join(fields) + "\n")
            else:
                out.append(row)
        if colmap:
            stats["tables_masked"][table] = {"rows": len(body), "rows_masked": rows_masked}
        out.append(terminator); i += 1
    return out, stats


def scan_residual_pii(text):
    """Fail-closed pós-sanitização: procura PII que escapou. Retorna lista de amostras."""
    hits = []
    for name, rx in (("email", EMAIL_RE), ("cpf", CPF_RE), ("cnpj", CNPJ_RE)):
        for mm in rx.finditer(text):
            hits.append((name, mm.group(0)))
            if len(hits) >= 20: return hits
    return hits


def run(in_path, out_path, config_path, salt, manifest_path):
    cfg = json.load(open(config_path, encoding="utf-8"))
    column_map = cfg["column_map"]
    drop_tables = set(cfg.get("drop_tables", []))
    allow_catalog = set(cfg.get("_not_pii_catalog", []))

    lines = open(in_path, encoding="utf-8", errors="replace").readlines()
    out_lines, stats = sanitize_stream(lines, column_map, salt, drop_tables, allow_catalog)

    # FAIL-CLOSED 1: coluna PII suspeita não classificada
    if stats["failclosed_hits"]:
        raise SystemExit(
            "STOP (fail-closed): colunas candidatas a PII NÃO classificadas — "
            "revisar antes de sanitizar:\n  " + "\n  ".join(sorted(set(stats["failclosed_hits"])))
        )

    data = "".join(out_lines)

    # FAIL-CLOSED 2: PII residual no output
    residual = scan_residual_pii(data)
    if residual:
        amostra = "; ".join(f"{k}:{v}" for k, v in residual[:5])
        raise SystemExit(f"STOP (fail-closed): PII residual no output: {amostra}")

    open(out_path, "w", encoding="utf-8").write(data)
    sha = hashlib.sha256(data.encode()).hexdigest()
    manifest = {
        "snapshot_id": f"ERP-HOMOLOG-{datetime.now(timezone.utc).strftime('%Y-%m-%d')}-01",
        "source_project_ref": "bucphzinpsndsagonwiq",
        "sanitized": True, "sanitizer_version": "0.2",
        "contains_customer_pii": False, "contains_auth_data": False,
        "drop_tables": sorted(drop_tables),
        "cells_masked": stats["cells_masked"],
        "tables_masked": stats["tables_masked"],
        "tables_dropped": stats["tables_dropped"],
        "failclosed_ok": True, "residual_pii_scan": "clean",
        "sha256": sha, "created_at": datetime.now(timezone.utc).isoformat(),
    }
    json.dump(manifest, open(manifest_path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    return manifest


# --------------------------- self-test ---------------------------------------

def _self_test():
    salt = "t"
    # máscara tipada de date produz data válida ISO
    d = mask_date("1990-05-15", salt)
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", d), d
    date.fromisoformat(d)  # não levanta = válida
    assert mask_date("1990-05-15", salt) == mask_date("1990-05-15", salt)  # determinística
    print("mask_date OK:", d)

    cfg = {
        "column_map": {
            "public.orders": {"customer_name": "name", "customer_phone": "phone", "delivery_address": "address"},
            "public.contacts": {"name": "name", "email": "email", "birth_date": "date"},
        },
        "drop_tables": ["auth.users"],
        "_not_pii_catalog": ["public.products.name", "public.product_variants.name"],
    }
    json.dump(cfg, open("/tmp/cfg2.json", "w"))

    sample = [
        "COPY public.contacts (id, name, email, birth_date, tenant_id) FROM stdin;\n",
        "u1\tManuela\tmanuela@dolce.com\t1990-05-15\tt1\n",
        "\\.\n",
        "COPY public.orders (id, customer_name, customer_phone, delivery_address, total) FROM stdin;\n",
        "o1\tJose Silva\t51999998888\tRua X 123\t500.00\n",
        "\\.\n",
        "COPY public.products (id, name, price) FROM stdin;\n",   # catálogo: NÃO mascara
        "p1\tBrigadeiro 15gr\t2.50\n",
        "\\.\n",
        "COPY public.sales (id, customer_id, total_amount) FROM stdin;\n",  # dado que agente precisa
        "s1\tu1\t500.00\n",
        "\\.\n",
    ]
    out, stats = sanitize_stream(sample, cfg["column_map"], salt,
                                 set(cfg["drop_tables"]), set(cfg["_not_pii_catalog"]))
    j = "".join(out)
    assert "manuela@dolce.com" not in j, "email vazou"
    assert "Manuela" not in j, "nome vazou"
    assert "1990-05-15" not in j, "birth_date nao mascarada"
    assert "Jose Silva" not in j and "51999998888" not in j and "Rua X 123" not in j, "orders PII vazou"
    assert "Brigadeiro 15gr" in j, "catalogo foi mascarado (ERRO)"
    assert "s1\tu1\t500.00" in j, "dado de venda alterado"
    assert not stats["failclosed_hits"], f"fail-closed falso positivo: {stats['failclosed_hits']}"
    print("stream v0.2 OK — cells_masked =", stats["cells_masked"])

    # fail-closed DEVE disparar em coluna PII não classificada
    sample_leak = [
        "COPY public.mistery (id, secret_email) FROM stdin;\n",
        "m1\tvazado@x.com\n",
        "\\.\n",
    ]
    _, st2 = sanitize_stream(sample_leak, {}, salt, set(), set())
    assert "public.mistery.secret_email" in st2["failclosed_hits"], "fail-closed NAO disparou"
    print("fail-closed OK — pegou coluna PII nao classificada")

    # varredura residual pega email real
    assert scan_residual_pii("blah user@real.com blah"), "residual scan cego"
    assert not scan_residual_pii("ok user_abc@example.invalid ok"), "residual falso positivo no placeholder"
    print("residual scan OK")
    print("SELF-TEST v0.2 PASSOU")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="in_path"); ap.add_argument("--out", dest="out_path")
    ap.add_argument("--config", dest="config_path"); ap.add_argument("--salt", default="CHANGE-ME")
    ap.add_argument("--manifest", dest="manifest_path"); ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test: _self_test(); sys.exit(0)
    if not (a.in_path and a.out_path and a.config_path and a.manifest_path):
        ap.error("--in/--out/--config/--manifest obrigatórios ou --self-test")
    print(json.dumps(run(a.in_path, a.out_path, a.config_path, a.salt, a.manifest_path),
                     indent=2, ensure_ascii=False))
