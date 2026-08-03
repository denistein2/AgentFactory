# Banco Gêmeo — v0.2 (30/07/2026)

Corrige a auditoria do GPT sobre a v0.1 (protótipo). Mapa de PII derivado do schema
real (#7767 [BANCO]), não mais de palpite.

## Bugs corrigidos (todos provados por self-test)
1. **Fail-closed real** — v0.1 declarava `unknown_pii_candidates` mas nunca preenchia.
   v0.2: coluna com nome PII não classificada (nem no column_map nem no allow_catalog
   de nomes-de-catálogo) → PARA. Testado: pega `secret_email`.
2. **birth_date tipada** — v0.1 usava `freetext` (texto) numa coluna `date` → restore
   quebraria. v0.2: masker `date` gera data válida determinística.
3. **Varredura residual real** — v0.1 usava `Select-String -SimpleMatch "a|b|c"` (o `|`
   virava literal, não pegava nada). v0.2: regex real DENTRO do sanitizador, ignora o
   placeholder `@example.invalid`, aborta se achar email/cpf/cnpj no output.

## Correções de arquitetura (auditoria)
4. **Mapa de PII completo** — schema real revelou PII em `orders` (customer_name/phone/
   delivery_address), `cashier_sessions.operator_email`, `pix_config`. v0.1 só cobria
   contacts/tenants → teria vazado orders e operator_email.
5. **Catálogo NÃO é PII** — products/product_variants/stock_types/merc_*/payment_methods
   preservados (mascarar quebraria os testes #7730). v0.2 distingue por allow_catalog.
6. **Views ignoradas** — v_orders_calendar é view (deriva de orders), sem COPY no dump.
7. **FK auth.users** — PROVADO VAZIO [#7767 bloco2]: nenhuma FK public→auth. Esvaziar
   auth.users é seguro; colunas created_by/updated_by são uuid soltos. A tese do auditor
   ("restore quebra por FK") era falsa — confirmado por leitura, não por argumento.
8. **Dump schema-only por padrão** — golden padrão = estrutura + seed sintético (PII zero).
   `-WithData` (snapshot-de-caso) é exceção e obriga sanitização.
9. **Bind 127.0.0.1** — Postgres não exposto em todas as interfaces.
10. **Validação de $Mission** — `^[A-Za-z0-9_]+$` antes de entrar em SQL.
11. **Restore por docker cp + psql -f + template0** — não mais pipe de texto (encoding/acento).
12. **Scripts 02–04 = "EXECUTOR LOCAL RODA"** — só o 01 (dump remoto) exige Denis.

## Ainda ABERTO antes de tocar dump real (não bloqueia schema-only)
- 🚩 Inventário de colunas jsonb/text livres (metadata/notes/details) — PII pode estar em
  conteúdo sem nome revelador. O #7767 não buscou conteúdo de jsonb.
- 🚩 Versão do Postgres do HOMOLOG — confirmar no dashboard e casar no docker-compose.
- Teste ponta a ponta com banco fictício com PII deliberadamente espalhada.
- Topologia do Codex: tem shell+Docker na máquina Windows? Define se ele roda 02–04 sozinho.
