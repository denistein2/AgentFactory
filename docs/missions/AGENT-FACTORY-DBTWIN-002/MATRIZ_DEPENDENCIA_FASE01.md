# MATRIZ_DEPENDENCIA_FASE01 — artefatos legados e schema-only

**Status:** custódia parcial concluída; matriz técnica ainda não preenchida.  
**Data:** 2026-08-02

A fonte v0.2 está disponível, mas não foi auditada integralmente. Não se deve
inferir dependência apenas pela presença dos arquivos. O pacote-fonte original
v0.3-phase01 continua ausente.

## Matriz a preencher por inspeção estática no Gate 02-A

| Artefato | Custódia | Usado no schema-only? | Usado nas fixtures? | Só legado? | Bloqueia Fase 02? |
|---|---|---|---|---|---|
| `sanitize_v2.py` v0.2 | presente | ❓ | ❓ | ❓ | ⛔ até inspeção |
| `columns.json` v0.2 | PEND-2A resolvida | ❓ (PEND-2D) | ❓ | ❓ | ⛔ até inspeção |
| Scripts 01–04 v0.2 | presentes | ❓ | ❓ | ❓ | ⛔ até inspeção |
| Scripts 00 e 05–10 | ausentes | ❓ | ❓ | ❓ | ⛔ sem evidência |
| `cells_masked=24` | documental | ❓ | ❓ | ❓ | ⛔ PEND-2C/2D |

Legenda: ❓ desconhecido até inspeção · ⛔ bloqueio conservador.

## Regra de resolução

- Se a inspeção mostrar que um artefato não participa do fluxo schema-only nem
  das fixtures, classificá-lo como auditoria histórica e registrar evidência.
- Se participar, documentar etapa/finalidade e mantê-lo como pré-condição do Gate 02-B.
- Enquanto o valor for desconhecido, não rebaixar o bloqueio.

## Estado de PEND-2

- PEND-2A localização/custódia: **RESOLVIDA**.
- PEND-2B auditoria técnica: **ABERTA**.
- PEND-2C `cells_masked=24 × columns.json`: **ABERTA**.
- PEND-2D dependência no schema-only: **ABERTA**.

PEND-2 não está integralmente encerrada.

## Ausências que impedem fechamento histórico

Pacote original v0.3-phase01, scripts 00 e 05–10, `artifacts/phase01`,
fixtures/manifests completos e evidências E2E/fingerprints da Fase 01.
