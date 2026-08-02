# ESTRATEGIA_AUDITORIA — Auditoria técnica da Fase 02

**Status:** planejamento. Custódia e self-test local não equivalem a auditoria técnica integral.
**Data:** 01/08/2026

> Regra permanente: **coerência documental ≠ reprodução de execução ≠ auditoria
> de código.** PASS documental da Fase 01 **não** é prova de corretude técnica e
> não pode ser reutilizado como tal.

---

## 1. Frentes de auditoria

### F1 — Revisão integral de código
Alvos disponíveis na fonte v0.2, classificada como `IMPORTED_UNAUDITED_LEGACY_SOURCE`:
- `sanitize_v2.py` — lógica de sanitização; verificar que mascara o que declara e não vaza.
- `columns.json` — sob custódia; PEND-2A resolvida, auditoria PEND-2B aberta.
- Scripts 01–04 — revisar ordem, idempotência, tratamento de falha e efeitos remotos.

Continuam ausentes o pacote original v0.3-phase01 e os scripts 00 e 05–10; não
há como fingir auditoria sobre arquivos não recebidos.

### F2 — Reprodução independente do E2E
- Rodar o ciclo completo **de novo**, de forma independente, não apenas reler artefatos.
- Comparar fingerprints obtidos com os declarados na Fase 01 (valores abreviados
  aqui; hash completo e canonicalização em `specs/FINGERPRINT_SPEC.md`):
  - inicial/final `1966329b…b035f219`
  - destrutivo `87a9fe6c…c7c6292c`
- **Relação esperada (corrigida — P0-02), sem cadeia ambígua `a ≠ b = c`:**
  ```
  inicial  = final
  inicial ≠ destrutivo
  final   ≠ destrutivo
  ```
  Qualquer das três falhando → STOP.
- Comparação só é reproduzível sob `specs/FINGERPRINT_SPEC.md` (algoritmo,
  canonicalização, tratamento de OIDs/owners/timestamps/sequences).

### F3 — Cruzamento `cells_masked` × `columns.json`
- Pendência explícita: `cells_masked = 24` **nunca** cruzado contra `columns.json`.
- Procedimento (refinado — P1-07). Uma coluna sensível pode não ter linhas
  elegíveis numa fixture; nesse caso, ausência de célula mascarada **não** prova
  ausência de cobertura. O cruzamento distingue quatro coisas, por
  `tabela`/`coluna`:
  ```
  cobertura da política   (a coluna está declarada em columns.json?)
  cobertura da fixture     (há linhas elegíveis para mascarar?)
  contagem observada       (linhas efetivamente transformadas)
  correção da transformação(tipo de máscara correto; sem falso pos./neg.)
  ```
  Registrar: `tabela, coluna, tipo de transformação, linhas elegíveis, esperadas,
  transformadas, falsos positivos, falsos negativos`.
- **Condicional (P0-06):** só é pré-condição do Gate 02-B **se**
  `MATRIZ_DEPENDENCIA_FASE01.md` marcar `columns.json`/`cells_masked` como usados
  no fluxo schema-only. Caso a matriz os classifique como legado puro da Fase 01,
  isto permanece auditoria histórica, não bloqueio da Fase 02.
- **Aberto:** `columns.json` está presente, mas PEND-2C e PEND-2D continuam sem
  fechamento técnico. Presença não prova cobertura nem dependência.

## 2. Matriz de nível de evidência

Cada afirmação de resultado é classificada — sem colapsar níveis:

| Item | Coerência documental | Reprodução de execução | Auditoria de código |
|---|---|---|---|
| Ciclo E2E fim a fim | Fase 01 ✅ | Fase 02 (F2) ⏸ | — |
| Fingerprints/hashes | Fase 01 (consistência cruzada) ✅ | F2 recomputa ⏸ | — |
| `sanitize_v2.py` correto | — | — | F1 ⏸ |
| `cells_masked` correto | declarado | — | F3 ⏸ (aberto) |
| RLS/policies fiéis | — | F2 + `VALIDACAO_SUPABASE` ⏸ | F1 ⏸ |
| Isolamento de rede | Fase 01 (guard) | F2 estrutural ⏸ | — |

Legenda: ✅ feito · ⏸ planejado/pendente · ⛔ bloqueado · — não aplicável.

## 3. Independência das leituras

- Fase 01 teve **três leituras** (GPT, Claude, Denis) **independentes entre si mas sobre o mesmo conjunto de artefatos** — não três reproduções.
- Fase 02 deve incluir **pelo menos uma reprodução independente real** (F2), distinta de releitura.
- **Graus de independência (P1-06)** — reexecutar o mesmo código na mesma máquina
  prova repetibilidade, não independência. O Gate 02-B **nomeia** o nível exigido:
  ```
  Nível 1 — nova execução, ambiente limpo, mesmo pipeline (repetibilidade)
  Nível 2 — executor/revisor distinto, mesmo pipeline
  Nível 3 — inventário e fingerprints recalculados por implementação independente
  Nível 4 — ambiente independente
  ```
  O nível é decisão do decisor (B-PC9), não presumido pelo agente.

## 4. Saídas de auditoria

- Relatório por frente (F1/F2/F3) com nível de evidência explícito.
- Lista de divergências (se houver) — **registradas, não corrigidas** nesta missão.
- Atualização da `MATRIZ_RASTREABILIDADE.md`.

## 5. Regra anti-reuso

Nenhum PASS anterior é promovido a "correto" sem a frente correspondente. Onde a auditoria não foi feita, o item permanece **declarado**, não **provado**.

## 6. Pendências

- **AUD-1.** Auditar `columns.json`, cruzar `cells_masked=24` e determinar sua
  dependência no schema-only (PEND-2B/2C/2D).
- **AUD-2.** Ambiente de reprodução independente do E2E — definir sem reabrir a Fase 01 nem reexecutar Docker fora de escopo autorizado.
- **AUD-3.** Avaliar, sem corrigir nesta missão: `-WithData`,
  `source_project_ref` hardcoded, referências realistas à Dolce no self-test,
  residual scan limitado, `jsonb`/texto livre, restore parcial, seed skeleton com
  `ROLLBACK` e PEND-3.
