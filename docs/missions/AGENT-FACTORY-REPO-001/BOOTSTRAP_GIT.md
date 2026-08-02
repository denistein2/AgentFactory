# BOOTSTRAP GIT — retomada governada

**Regra:** a árvore completa entra por Draft PR. Push direto em `main` é proibido.
O agente pode criar branch, validar, commitar, enviar a branch e abrir/atualizar o
Draft PR. Merge é exclusivamente humano.

## Pré-requisitos

- `git` instalado;
- repositório remoto acessível e autenticação válida;
- nenhuma tag `factory/v1.0.0-foundation` criada antes do merge.

## Caso A — `main` existe

```bash
git fetch origin
git switch main
git pull --ff-only origin main
git switch -c bootstrap/org-001-foundation

# executar todas as validações da missão antes do commit
git add .
git commit -m "chore(repo): establish AgentFactory foundation"
git push -u origin bootstrap/org-001-foundation
gh pr create --draft --base main --head bootstrap/org-001-foundation \
  --title "chore(repo): establish AgentFactory foundation" \
  --body-file docs/missions/AGENT-FACTORY-REPO-001/FIRST_PR_BODY.md
```

Fluxo canônico: `main → bootstrap/org-001-foundation → validar → commit → push da
branch → Draft PR → revisão humana → merge humano`.

Não declarar PR criado sem URL e número confirmados.

## Caso B — repositório vazio e sem `main`

Encerrar com:

```text
status: BLOCKED_BASE_BRANCH
reason: o repositório não possui main mínima para servir de base ao Draft PR
```

Não colocar a árvore completa diretamente em `main`. É necessária uma `main`
mínima, criada por ação humana/administrativa, para que a branch
`bootstrap/org-001-foundation` tenha base de comparação. Depois que `main`
existir, retomar pelo Caso A.

## Tag — somente depois do merge

```bash
git switch main
git pull --ff-only origin main
git tag -a factory/v1.0.0-foundation -m "Baseline organizacional"
git push origin factory/v1.0.0-foundation
```

Esta missão não cria tag.
