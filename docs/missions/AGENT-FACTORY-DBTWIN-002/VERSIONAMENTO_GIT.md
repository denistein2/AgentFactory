# VERSIONAMENTO_GIT — Estratégia de versionamento (condição #1)

> **Correção residual (parecer):** a árvore da fábrica é a de `ESTRUTURA_CANONICA.md`; onde este doc adicionava `fixtures/` na raiz ou dizia 'idêntica', prevalece a árvore canônica. Referência a 'validação de links Markdown' leia-se 'validação de referências de caminho'.


**Repositório:** `denistein2/AgentFactory`
**Status:** proposta de planejamento. Nenhum **versionamento canônico** executado nesta sessão.
**Desvio registrado:** houve um `git init` local temporário para checagem auxiliar de referências, **revertido em seguida** — sem commit, remote ou push. Não constitui o versionamento canônico do Gate 02-A. Registrado, não apagado.
**Data:** 01/08/2026

> Versionar o pacote é **saída (pós-condição) do Gate 02-A** e **entrada obrigatória do Gate 02-B**. Não é pré-condição do próprio 02-A (corrige P0-REV-02): o 02-A é aprovado contra o manifesto pré-Git e produz o commit.
> Os comandos abaixo são **propostas controladas**, não ações realizadas.

---

## 1. Estrutura proposta do repositório

```
AgentFactory/
├─ README.md
├─ governance/
│  ├─ M17_FRONTEIRA_EXECUTOR.md
│  ├─ M18_DECISAO_HUMANA_SUBSTITUTIVA.md
│  └─ decisions/
│     ├─ current/
│     │  └─ DECISAO_SUBSTITUTIVA_SCHEMA_ONLY.md               # canônica atual
│     └─ history/
│        ├─ 2026-07-31_DECISAO_DUMP_COMPLETO__ORIGINAL.md     # bytes intactos
│        └─ 2026-08-01_STATUS_SUBSTITUICAO_DUMP_COMPLETO.md   # marcador de status
├─ missions/
│  ├─ DBTWIN-001/
│  │  └─ HANDOFF_DBTWIN_001.md
│  └─ DBTWIN-002/
│     ├─ PLAN_DBTWIN_002.md
│     ├─ ESTRUTURA_CANONICA.md
│     └─ docs/
│        ├─ CONTRATO_FASE_02.md
│        ├─ GATE_HUMANO_FASE_02.md
│        ├─ ORIGEM_SCHEMA_ONLY.md
│        ├─ POLITICA_ISOLAMENTO_REDE.md
│        ├─ ESTRATEGIA_AUDITORIA.md
│        ├─ VALIDACAO_SUPABASE.md
│        ├─ FIXTURES_SINTETICAS.md
│        ├─ MATRIZ_RASTREABILIDADE.md
│        ├─ MATRIZ_DEPENDENCIA_FASE01.md
│        └─ specs/
│           ├─ EVIDENCE_MANIFEST_SPEC.md
│           ├─ SCHEMA_INVENTORY_SPEC.md
│           ├─ FINGERPRINT_SPEC.md
│           ├─ SCHEMA_SOURCE_MANIFEST.md
│           └─ PACKAGE_IMPORT_MANIFEST.md
├─ package/
│  └─ stein-db-twin/            # scripts 00–10, sanitize_v2.py, columns.json (após auditoria/custódia)
├─ fixtures/                    # SOMENTE fixtures sintéticas
└─ .gitignore
```

> Árvore única e canônica: idêntica a `missions/DBTWIN-002/ESTRUTURA_CANONICA.md`.
> Links relativos do plano/README seguem-na (corrige P1-01). Validação automática
> de links Markdown é pré-condição de commit.
>
> A colocação exata de `stein-db-twin` (submódulo vs. diretório) é **decisão necessária** (VG-1).

---

## 2. Commit-base

- Proposta: primeiro commit contém **apenas** documentação de governança e planejamento (este pacote) + `.gitignore`. **Nenhum artefato executável de dados.**
- Mensagem sugerida do commit-base:
  ```
  chore(dbtwin-002): commit-base — pacote de planejamento schema-only (sem execução)
  ```
- O commit-base serve de âncora para **prova de delta**: toda mudança posterior é medida contra ele.

## 3. Arquivos obrigatórios

- Todos os `.md` de governança, plano, contrato, gate, especificações e matriz.
- `.gitignore` restritivo.
- `README.md` apontando para `PLAN_DBTWIN_002.md` como fonte de estado.

## 4. Arquivos e conteúdos IGNORADOS (`.gitignore` proposto)

```gitignore
# Dumps e dados — NUNCA versionar
*.sql
*.dump
Testbank.sql
**/dumps/**
**/real_data/**

# Credenciais e segredos
.env
*.env
**/secrets/**
*.key
*.pem
service_role*
anon_key*

# Logs e evidências volumosas de execução
*.log
**/logs/**
**/evidence/raw/**

# Artefatos de container/local
**/pgdata/**
**/.docker/**
```

> Exceção controlada: **fixtures sintéticas** vivem em `fixtures/` e **são**
> versionadas — mas o padrão `*.sql` as ignoraria. Resolver com um
> `!fixtures/**/*.sql` explícito **somente** para fixtures comprovadamente
> sintéticas, e com revisão humana antes de remover o ignore. Registrado como
> **decisão necessária** para não abrir brecha a dump real.

### 4.1 `.gitignore` não é controle de segurança (corrige P1-13)

`.gitignore` não impede `git add -f`, não detecta dump renomeado (`.json`,
`.csv`, `.zip`, `.backup`, sem extensão) e não vê conteúdo. Controles **ativos**
exigidos antes do Gate 02-A:

- **pre-commit hook** com validação de paths permitidos (allowlist positiva);
- **scanner de segredos** (chaves, tokens, `service_role`, JWT);
- **scanner de PII/dados tabulares** (heurística de linhas de negócio);
- **limite de tamanho** de arquivo;
- **CI** que rejeita extensões e padrões proibidos, inclusive `add -f`;
- **revisão humana obrigatória**;
- **lista positiva de fixtures** + **manifesto** que declara cada fixture como sintética.

`.gitignore` é a primeira barreira, não a única nem a que prova segurança.

## 5. Política por tipo de conteúdo

| Tipo | Versionar? | Regra |
|---|---|---|
| Documentação/governança | Sim | Fonte da verdade |
| Scripts do pacote (auditados) | Sim | Após auditoria de código |
| Fixtures sintéticas | Sim | Somente sintéticas; whitelisting explícito |
| Dumps com dados reais | **Nunca** | `.gitignore` **+ controles ativos** (ver §4.1) — `.gitignore` sozinho não é controle de segurança |
| Credenciais/segredos | **Nunca** | Fora do repo; usar cofre/ambiente |
| Logs de execução | Não (raw) | Só sumários/manifestos curados |
| Evidências (fingerprints/manifestos) | Sim (curadas) | Sem PII, sem segredo |

## 6. Branches, tags, hashes, prova de delta

### 6.0 Validação de referências de caminho (não "links Markdown")

Os documentos usam **referências textuais** entre crases (`` `arquivo.md` ``),
não links Markdown. A validação, portanto, é de **referências de caminho**, com
relatório classificado (rodada 2):

```
Os totais vigentes são regenerados em `evidence/reports/BROKEN_REFERENCES.md`.
`columns.json` está presente; pacote v0.3-phase01, scripts 00 e 05–10,
`artifacts/phase01`, fixtures/manifests completos e evidências E2E/fingerprints
continuam declarados ausentes.
```

"Arquivos declarados-ausentes" são pré-condições futuras já documentadas, não
defeitos. Nenhum caminho inválido remanescente. Esta validação roda antes de
qualquer commit (Gate 02-A).

- **Branches:** `main` (canônico), `mission/dbtwin-002-planning` (este pacote), futuras `mission/dbtwin-002-exec-prep` após aprovação.
- **Tags:** `v0.3-phase01` é apenas referência documental; nenhuma tag foi criada
  nesta missão. O pacote-fonte original correspondente continua ausente.
- **Hashes:** cada entregável referenciado por commit hash; fingerprints de fixtures e de resultados registrados nos manifestos (não como blobs grandes no Git).
- **Prova de delta:** diffs contra o commit-base; a Fase 02, quando executada, gera manifesto com hashes de entrada/saída comparáveis ao baseline — a evidência de delta é **verificável**, não declarada.

## 7. Condição permanente

> Versionar o pacote (commit-base + estrutura acima) permanece **pré-condição
> obrigatória**: o versionamento da documentação é **saída do Gate 02-A** (produzida após aprovação) e o
> commit-base/hashes fixados são condição do **Gate 02-B** (B-PC1). Sem isso, o
> fluxo não avança.

## 8. Pendências / decisões necessárias

- **VG-1.** `stein-db-twin` como submódulo ou diretório — decisão necessária.
- **VG-2.** Regra de exceção `!fixtures/**/*.sql` — decisão necessária, com revisão humana.
- **VG-3.** Local do cofre de segredos (fora do Git) — decisão necessária.
