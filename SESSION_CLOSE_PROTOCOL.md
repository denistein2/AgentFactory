# PROTOCOLO DE FECHAMENTO DE SESSÃO E PR AUTÔNOMO

## Regra

Toda sessão que altere arquivos do projeto deve terminar com PR.

O agente pode, autonomamente, criar a branch de sessão, validar, fazer commit,
enviar essa branch e abrir ou atualizar o Draft PR. Push direto em `main` é
proibido. O merge permanece exclusivamente humano.

## Exceções

Uma sessão puramente consultiva, sem alteração no repositório, registra apenas uma nota de sessão quando necessário.

## Fechamento mínimo

Criar:

```text
docs/sessions/YYYY/YYYY-MM-DD/SESSION_<ID>.md
```

Preencher:

```yaml
---
session_id:
date:
mission:
platform:
status:
branch:
commit:
pull_request:
---
```

Seções:

1. Objetivo
2. Estado recebido
3. Decisões
4. Alterações
5. Evidências
6. Validações
7. Desvios
8. Riscos
9. Pendências
10. Próxima sessão

## Automação pretendida

```text
branch -> validate -> commit -> push -> draft PR -> CI -> human gate
```

## Branch

```text
session/YYYY-MM-DD/<missao>-<slug>
```

## Commit

Preferir Conventional Commits:

```text
docs(dbtwin): reconcile Gate 02-A package
chore(repo): classify imported artifacts
fix(manifest): correct package references
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

## Decisões

## Evidências e validações

## Riscos e pendências

## Gate
- [ ] CI verde
- [ ] Sem segredos
- [ ] Sem dados reais
- [ ] Referências válidas
- [ ] Revisão humana
```

## Bloqueios

Se não houver GitHub/autenticação:

```text
status: BLOCKED_GITHUB
```

A sessão deve gerar:

- branch local;
- commits locais;
- patch ou bundle;
- corpo do PR;
- comandos exatos de retomada.

Não declarar PR criado sem URL e número confirmados. Falta de autenticação ou
acesso bloqueia apenas as etapas remotas; não revoga a autorização para branch,
validação e commit locais.

## Merge

O agente não faz merge. A decisão e a execução do merge são exclusivamente humanas.

## CI mínimo recomendado

- markdown lint;
- verificação de links e referências;
- detecção de arquivos duplicados por hash;
- secret scan;
- verificação de nomes proibidos;
- validação de manifestos JSON;
- teste dos scripts;
- bloqueio de dumps e dados reais.
