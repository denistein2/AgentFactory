# EVIDENCE_MANIFEST_SPEC — Contrato do manifesto de evidência

**Status:** minuta de especificação (planejamento). Nenhum manifesto gerado nesta sessão.
**Data:** 01/08/2026

> Corrige P0-08. O contrato exige manifesto/delta, mas nenhum documento definia o
> formato. Este é o esquema mínimo; sem ele, "delta verificável" é declarativo.

---

## 1. Esquema (proposto, versionado)

```json
{
  "manifest_version": "1.0",
  "mission": "AGENT-FACTORY-DBTWIN-002",
  "phase": "02",
  "gate": "02-B",
  "created_at_utc": "<timestamp confiável>",
  "executor_commit": "<hash do commit do executor>",
  "environment": {
    "postgres_image_digest": "<sha256:...>",
    "postgres_version": "<x.y>",
    "docker_version": "<...>",
    "compose_version": "<...>",
    "extensions": [{"name": "<ext>", "version": "<...>"}],
    "locale": "<...>", "timezone": "<...>", "collation": "<...>",
    "arch": "<...>"
  },
  "schema_source": {
    "source_manifest_ref": "specs/SCHEMA_SOURCE_MANIFEST.md",
    "schema_artifact_sha256": "<64 hex>",
    "inventory_ref": "SCHEMA_INVENTORY_SPEC"
  },
  "fixtures": [
    {"id": "<CN-01>", "sha256": "<64 hex>"}
  ],
  "fingerprints": {
    "algo": "sha256",
    "canonicalization": "FINGERPRINT_SPEC v1",
    "data_initial": "<64 hex>",
    "data_destructive": "<64 hex>",
    "data_final": "<64 hex>",
    "structural_security": "<64 hex>",
    "inventory": "<64 hex>",
    "relations_checked": ["data_initial==data_final", "data_initial!=data_destructive", "data_final!=data_destructive"]
  },
  "scenarios": [
    {"id": "<AD-02>", "expected": "EXPECTED_FAIL", "observed": "EXPECTED_FAIL",
     "sqlstate": "<...>", "rollback_confirmed": true, "partial_domain_state": false}
  ],
  "network_isolation": {
    "remote_database_accesses": 0,
    "measurement_method": "<ver POLITICA_ISOLAMENTO_REDE>",
    "registry_pull_distinguished": true
  },
  "exit_code": 0,
  "custody": {
    "package_import_manifest_ref": "specs/PACKAGE_IMPORT_MANIFEST.md"
  }
}
```

## 2. Regras

- **Versão do manifesto** obrigatória; mudança de esquema incrementa versão.
- **Hashes completos** (64 hex), nunca abreviados no manifesto.
- **Timestamps confiáveis**: fonte declarada; excluídos do escopo hasheado do fingerprint (ver `FINGERPRINT_SPEC §3`).
- **Status por cenário** deve existir mesmo para EXPECTED_FAIL (ver P1-09): falha limpa **produz** evidência completa; o que não existe é **estado de domínio parcial**, não a evidência.
- **Cadeia de custódia** referenciada, não presumida.

## 3. Pendências

- **EM-1.** Fonte de timestamp confiável no ambiente local.
- **EM-2.** Local de armazenamento das evidências curadas (versionável, sem PII/segredo).
