# GOVERNANCE — Stein Agent Factory

Regras canônicas de governança. Este arquivo indexa; os documentos detalhados
vivem em `docs/governance/`.

## Autoridade e precedência

`M17/M18 → decisões atuais → Gate → contrato → plano-mestre → especificações → matriz`

- **M17 — Fronteira do Executor** (`docs/governance/M17_FRONTEIRA_EXECUTOR.md`):
  o executor local roda comandos mecânicos; Denis decide os gates; Denis não é
  barramento de comandos.
- **M18 — Decisão Humana Substitutiva e Não-Reabertura**
  (`docs/governance/M18_DECISAO_HUMANA_SUBSTITUTIVA.md`): Claude alerta uma vez,
  registra a decisão humana e não reabre a mesma objeção sem novo fato. M18 não
  desloca obrigações legais, políticas de provedor nem requisitos de segurança
  inseparáveis da execução segura.

## Princípios permanentes

1. **Taxonomia de evidência:** `coerência documental ≠ reprodução de execução ≠ auditoria de código`.
2. **Preservar antes de limpar** — nada é apagado antes de inventário, hash e gate.
3. **Hash antes de decidir** — duplicidade se resolve por SHA-256, não por nome.
4. **Mesmo nome ≠ mesmo conteúdo.**
5. **ZIP/TAR não é fonte canônica** — só transporte/release/evidência.
6. **Não-erasura** — conteúdo substituído vai para `history`/`superseded` com referência ao sucessor, nunca deletado.
7. **Divulgação honesta** — ações temporárias (ex.: um `git init` revertido) são registradas, não apagadas.
8. **Fonte única por tipo de artefato** — um documento canônico por artefato.

## Dois gates da Fase 02

- **Gate 02-A** — preparação estática (sem container). Versionamento é saída, não entrada.
- **Gate 02-B** — execução (sobe container). Primeira etapa: B0 — preflight de isolamento.

Estado: `CANDIDATO A GATE 02-A — NÃO APROVADO`.

## Protocolos de fábrica

- `docs/governance/PROTOCOLO_EXCHANGE_01.md` — transferência Drive↔Local (sintético).
- `docs/governance/PROTOCOLO_CROSSAUDIT_01.md` — dupla construção + auditoria cruzada (caro; não é o modo padrão).
- `SESSION_CLOSE_PROTOCOL.md` (raiz) — fechamento obrigatório de sessão + PR autônomo.

## Fechamento de sessão e PR

Toda sessão que altera o projeto termina com branch de sessão, validação, commit,
push da branch e abertura ou atualização de Draft PR, quando houver base remota e
autenticação. O agente está autorizado a executar essas etapas sem nova
confirmação. **Push direto em `main` é proibido e merge é sempre exclusivamente
humano.** Ver `SESSION_CLOSE_PROTOCOL.md`.

As políticas encontradas dentro de fontes importadas, inclusive
`package/stein-db-twin/policies/human-gates.json` e `permissions.json`, são
políticas legadas subordinadas a esta governança raiz; preservá-las não altera a
fronteira vigente.
