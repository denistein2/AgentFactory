# PROTOCOLO DE FECHAMENTO DE SESSÃO E PR AUTÔNOMO

## Regra

Toda sessão que altere arquivos do projeto termina com branch de sessão, validação, commit/push da branch e Draft PR quando GitHub estiver disponível. Push direto em `main` é proibido. Merge permanece exclusivamente humano.

Sessão consultiva/read-only pode terminar sem PR, mas deve registrar resultado na Issue quando a missão exigir.

## Registro mínimo

Criar:

```text
docs/sessions/YYYY/YYYY-MM-DD/SESSION_<ID>.md
```

Frontmatter mínimo:

```yaml
---
session_id:
mission_id:
issue:
started_at:
finished_at:
status:
branch:
base_ref:
base_sha:
commit:
pull_request:
actor_type:
requested_executor:
actual_executor:
provider:
product_agent:
model_reported:
role:
run_id:
evidence_strength:
does_not_prove:
---
```

Quando um campo não for comprovável, usar `UNKNOWN` ou `UNVERIFIED`; nunca inferir modelo, executor, session/run id ou timestamp histórico.

As seções mínimas continuam:

1. Objetivo
2. Estado recebido
3. Decisões/Gates
4. Alterações
5. Evidências e proveniência
6. Validações
7. Desvios
8. Riscos
9. Pendências
10. Próxima sessão

Se a sessão alterar current-state material, atualizar também `docs/governance/FACTORY_LOGBOOK.md` com fonte/ref e `last_verified_at`.

## Automação

```text
human gate (quando exigido)
→ branch
→ mutate within scope
→ validate
→ session record
→ commit/push branch
→ draft PR
→ CI
→ human review/merge gate
```

## Branch

```text
session/YYYY-MM-DD/<missao>-<slug>
```

## Commit

Preferir Conventional Commits, por exemplo:

```text
docs(governance): reconcile current-state provenance
fix(manifest): correct package references
chore(repo): classify imported artifacts
```

## PR

Título:

```text
session(<missão>): <resultado>
```

Corpo mínimo:

```markdown
## Objetivo
## Alterações
## Decisões/Gates
## Evidências e validações
## Riscos e pendências
## Não prova / não escopo

## Gate
- [ ] CI verde
- [ ] Sem segredos
- [ ] Sem dados reais
- [ ] Referências válidas
- [ ] Revisão humana
```

## Validação mínima

- referências/path dos arquivos alterados;
- secret scan;
- bloqueio de dumps/dados reais;
- JSON/YAML quando alterados;
- diff contra base SHA;
- coerência de current-state (`README`/`GOVERNANCE`/`FACTORY_LOGBOOK`) quando aplicável.

## Bloqueios

Se GitHub/autenticação estiver indisponível: `status: BLOCKED_GITHUB`; gerar branch/commit local quando tecnicamente possível, patch/bundle, corpo do PR e comandos de retomada. Não declarar PR criado sem URL/número confirmados.

## Merge

O executor **não faz merge**. Decisão e execução do merge são exclusivamente humanas.
