# MISSÃO AGENT-FACTORY-REPO-001
## Consolidação documental, faxina segura, Google Drive e baseline GitHub v1

**Responsável humano:** Denis Stein  
**Projeto:** Stein Agent Factory / Fábrica de Agentes  
**Data de abertura:** 2026-08-02  
**Estado inicial:** `READY_FOR_INVENTORY`  
**Modo:** preservação primeiro; nenhuma exclusão destrutiva antes de inventário, hashes e Gate Humano.

---

## 1. Problema que esta missão resolve

Os materiais da Fábrica de Agentes e do DB Twin estão distribuídos entre:

- `C:\SteinAgentFactory\stein-db-twin-v0.2`;
- `Downloads`;
- pacotes `.zip` e `.tar`;
- documentos repetidos com sufixos como `(1)`, `(3)` e `(4)`;
- pastas por data;
- pastas opacas chamadas `files`, `files2`, `files3`, `files4` e `files5`;
- Google Drive;
- sessões do ChatGPT;
- sessões e artefatos do Claude;
- possíveis arquivos ainda apenas no celular.

O problema não é somente “arrumar pastas”. É necessário determinar:

1. qual arquivo é canônico;
2. qual é histórico;
3. qual foi substituído;
4. qual é duplicata idêntica;
5. qual tem o mesmo nome, mas conteúdo diferente;
6. qual pacote está incompleto;
7. quais referências estão quebradas;
8. o que pertence ao GitHub;
9. o que pertence ao Drive;
10. o que deve permanecer em quarentena.

---

## 2. Objetivo

Produzir uma base única, rastreável e versionável da Stein Agent Factory, com:

- inventário integral dos arquivos locais e dos arquivos coletados do celular/Claude/Drive;
- classificação documental;
- estrutura canônica local;
- estrutura canônica no Google Drive;
- repositório GitHub próprio;
- baseline organizacional v1;
- protocolo obrigatório de fechamento de sessão;
- criação autônoma de Pull Request após cada sessão que altere o projeto;
- preservação das decisões e evidências históricas sem misturá-las com o estado atual.

---

## 3. Interpretação correta da “v1”

A v1 desta missão será uma **baseline organizacional e documental do repositório da Stein Agent Factory**.

Ela não poderá ser usada para afirmar, sem evidência adicional:

- paridade do DB Twin;
- conclusão da DBTWIN-002;
- aprovação do Gate 02-A;
- aprovação do Gate 02-B;
- auditoria integral do código;
- reprodução independente do pipeline;
- conexão autorizada com Supabase ou dados reais.

Versão sugerida da baseline:

```text
stein-agent-factory factory/v1.0.0-foundation
```

A versão interna do módulo DB Twin deve ser preservada e reconciliada separadamente. Não se deve escolher entre `v0.2`, `v0.3-phase01` ou outra versão apenas pelo nome das pastas.

---

## 4. Princípios obrigatórios

### P1 — Preservar antes de limpar

Nenhum arquivo será apagado na primeira etapa.

### P2 — Hash antes de decidir

Toda classificação de duplicidade deverá usar SHA-256.

### P3 — Mesmo nome não significa mesmo conteúdo

Arquivos como:

```text
README.md
README(3).md
README(4).md
MANIFESTO_PRE_GIT_DBTWIN_002.md
MANIFESTO_PRE_GIT_DBTWIN_002(1).md
```

devem ser comparados por conteúdo e hash.

### P4 — ZIP não é fonte canônica

Pacotes compactados servem como entrega, transporte, release ou evidência. O conteúdo canônico deve existir em árvore legível e versionada.

### P5 — GitHub e Drive têm papéis diferentes

**GitHub:**

- código;
- documentação canônica;
- decisões;
- missões;
- contratos;
- scripts;
- manifests pequenos;
- histórico de alterações;
- PRs e Gates.

**Google Drive:**

- exportações brutas de sessões;
- pacotes `.zip` e `.tar`;
- releases binárias;
- evidências pesadas;
- capturas de tela;
- intercâmbios com Claude/Codex;
- backups de custódia;
- quarentena.

### P6 — Nunca apagar história para “deixar bonito”

Conteúdo substituído deve ser movido para `superseded` ou `history`, com referência ao sucessor.

### P7 — PR autônomo não significa merge autônomo

O encerramento da sessão pode criar branch, commit, push e PR automaticamente. O merge permanece sujeito ao Gate Humano até nova decisão.

---

## 5. Escopo

### Incluído

- pasta local `C:\SteinAgentFactory`;
- arquivos relacionados ao projeto em `Downloads`;
- arquivos coletados do celular;
- arquivos exportados do Claude;
- arquivos já existentes no Google Drive;
- sessões do ChatGPT relacionadas à Fábrica de Agentes;
- DBTWIN-001 e DBTWIN-002;
- documentação, scripts, manifests, fixtures, policies, auditorias, handoffs e prompts;
- criação do repositório e publicação da baseline v1.

### Fora de escopo nesta missão

- conexão com Supabase;
- dados reais;
- produção;
- execução do Gate 02-B;
- alteração funcional do ERP Food Control;
- descarte definitivo de arquivos sem Gate Humano;
- reescrita técnica completa de `sanitize_v2.py`, `columns.json` ou scripts `00–10`.

---

## 6. Fontes conhecidas a coletar

### 6.1 Local

```text
C:\SteinAgentFactory\stein-db-twin-v0.2
C:\Users\<USUARIO>\Downloads
```

### 6.2 Estruturas visíveis atualmente

```text
stein-db-twin-v0.2/
├── artifacts/
├── config/
├── docs/
├── fixtures/
├── manifests/
├── policies/
├── sanitizer/
├── scripts/
├── seeds/
├── .gitignore
├── CHANGELOG.md
└── README.md
```

### 6.3 Zonas de confusão já identificadas

```text
docs/2026-08-01/files/
docs/2026-08-01/Versao01/
docs/2026-08-02/files/
docs/2026-08-02/files.zip
docs/2026-08-02/files2.zip
docs/2026-08-02/files3.zip
docs/2026-08-02/files4.zip
docs/2026-08-02/files5.zip
```

Além de downloads com nomes repetidos, como:

```text
README(3)
README(4)
MANIFESTO_PRE_GIT_DBTWIN_002(1)
RELATORIO_VALIDACAO_REFERENCIAS_DBTWIN_002(1)
RELATORIO_RECONSTRUCAO_DBTWIN_002(1)
stein-db-twin-v0.2.tar(1)
```

---

## 7. Classificação documental obrigatória

Cada arquivo deverá receber exatamente uma classificação primária:

| Código | Classificação | Significado |
|---|---|---|
| `CANONICAL_ACTIVE` | Canônico ativo | Fonte atual de verdade |
| `HISTORICAL_EVIDENCE` | Evidência histórica | Registro necessário, mas não atual |
| `SUPERSEDED` | Substituído | Mantido com indicação do sucessor |
| `DUPLICATE_IDENTICAL` | Duplicata idêntica | Mesmo SHA-256 de outro arquivo |
| `DUPLICATE_DIVERGENT` | Duplicata divergente | Nome/conceito semelhante, conteúdo diferente |
| `GENERATED_ARTIFACT` | Artefato gerado | Pode ser recriado por processo definido |
| `RELEASE_PACKAGE` | Pacote de release | ZIP/TAR de distribuição |
| `RAW_SESSION_EXPORT` | Exportação bruta | Chat, Claude, captura ou arquivo recebido |
| `INCOMPLETE` | Incompleto | Declara dependências ausentes |
| `QUARANTINE` | Quarentena | Origem ou significado ainda não resolvido |
| `OUT_OF_SCOPE` | Fora do projeto | Não pertence à Fábrica de Agentes |

Campos adicionais:

- caminho de origem;
- nome;
- extensão;
- tamanho;
- data de modificação;
- SHA-256;
- missão;
- sessão;
- versão declarada;
- sucessor canônico;
- referências recebidas;
- referências emitidas;
- decisão humana;
- destino proposto.

---

## 8. Estrutura canônica proposta do repositório

```text
stein-agent-factory/
├── README.md
├── CHANGELOG.md
├── GOVERNANCE.md
├── CONTRIBUTING.md
├── SECURITY.md
├── .gitignore
├── .gitattributes
│
├── docs/
│   ├── architecture/
│   ├── governance/
│   │   ├── gates/
│   │   ├── policies/
│   │   └── decisions/
│   │       ├── current/
│   │       └── history/
│   ├── missions/
│   │   ├── AGENT-FACTORY-DBTWIN-001/
│   │   ├── AGENT-FACTORY-DBTWIN-002/
│   │   └── AGENT-FACTORY-REPO-001/
│   ├── sessions/
│   │   └── YYYY/
│   │       └── YYYY-MM-DD/
│   ├── audits/
│   ├── handoffs/
│   ├── prompts/
│   ├── runbooks/
│   └── references/
│
├── projects/
│   └── db-twin/
│       ├── README.md
│       ├── CHANGELOG.md
│       ├── config/
│       ├── fixtures/
│       ├── manifests/
│       ├── policies/
│       ├── sanitizer/
│       ├── scripts/
│       ├── seeds/
│       └── tests/
│
├── evidence/
│   ├── manifests/
│   ├── hashes/
│   ├── reports/
│   └── small-artifacts/
│
├── tools/
│   ├── inventory/
│   ├── validation/
│   └── session-close/
│
├── templates/
│   ├── mission/
│   ├── handoff/
│   ├── decision/
│   ├── audit/
│   └── pull-request/
│
└── archive/
    ├── superseded/
    ├── raw-session-index/
    └── quarantine-index/
```

### Regra importante

Arquivos `.zip`, `.tar`, screenshots e exportações brutas não deverão ser mantidos normalmente dentro do Git. O repositório deverá guardar:

- manifesto;
- hash;
- nome do pacote;
- localização no Drive;
- data;
- responsável;
- relação com a missão.

---

## 9. Estrutura canônica proposta do Google Drive

```text
Stein Agent Factory/
├── 00_INBOX/
│   ├── CELULAR/
│   ├── CLAUDE/
│   ├── CHATGPT/
│   └── DOWNLOADS_PC/
│
├── 01_CANONICAL_EXPORTS/
│   ├── REPOSITORY_SNAPSHOTS/
│   └── SIGNED_DECISIONS/
│
├── 02_RAW_SESSIONS/
│   ├── CHATGPT/
│   ├── CLAUDE/
│   └── CODEX/
│
├── 03_EVIDENCE/
│   ├── DBTWIN-001/
│   ├── DBTWIN-002/
│   └── REPO-001/
│
├── 04_RELEASES/
│   ├── STEIN_AGENT_FACTORY/
│   └── DB_TWIN/
│
├── 05_AUDIT_EXCHANGE/
│   ├── INCOMING/
│   └── OUTGOING/
│
├── 90_SUPERSEDED/
│
└── 99_QUARANTINE/
```

### Regra do `00_INBOX`

Tudo entra primeiro no INBOX. Nada é considerado canônico por estar no Drive.

---

## 10. Plano de execução

## Etapa A — Freeze e custódia

1. Não renomear, mover ou apagar arquivos.
2. Criar uma cópia de segurança da pasta atual.
3. Executar o script de inventário somente leitura.
4. Gerar:
   - `inventory.csv`;
   - `inventory.json`;
   - `duplicate-groups.csv`;
   - `summary.json`;
   - `errors.log`.
5. Calcular SHA-256 de todos os arquivos.
6. Registrar a árvore de pastas.

**Saída:** fotografia confiável do estado inicial.

---

## Etapa B — Coleta das fontes externas

1. Baixar os arquivos ainda presentes somente no celular.
2. Exportar os materiais relevantes do Claude.
3. Exportar ou copiar as sessões do ChatGPT relacionadas ao projeto.
4. Colocar tudo em:

```text
00_INBOX/<ORIGEM>/<DATA>/
```

5. Não misturar material coletado com conteúdo canônico.
6. Reexecutar o inventário.

**STOP GATE B:** nenhuma classificação final antes de reunir as fontes conhecidas.

---

## Etapa C — Expansão segura de pacotes

1. Cada ZIP/TAR recebe hash antes da extração.
2. Extrair para:

```text
_work/extracted/<SHA256_DO_PACOTE>/
```

3. Nunca extrair por cima de uma pasta existente.
4. Inventariar o conteúdo extraído.
5. Comparar pacote versus árvore já existente.
6. Registrar:
   - arquivos ausentes;
   - arquivos extras;
   - arquivos idênticos;
   - arquivos divergentes.

---

## Etapa D — Reconstrução cronológica das sessões

Criar um registro por sessão contendo:

```text
session_id
data
plataforma
missão
objetivo
arquivos recebidos
arquivos produzidos
decisões
desvios
auditorias
estado final
handoff
sucessora
```

Sessões já conhecidas a mapear:

```text
2026-07-31 — Projeto Fábrica de Agentes
2026-07-31 — Sessão AGENT-FACTORY-DBTWIN
2026-08-01 — Sessão Iniciada AGENT-FACTORY-DBTWIN-001
2026-08-01 — Sessão iniciada DBTWIN
2026-08-02 — Organização, Drive e baseline GitHub
```

Esta lista é inicial e não substitui a leitura integral dos arquivos e exportações.

---

## Etapa E — Canonicalização

Para cada conceito com múltiplos candidatos:

1. comparar hash;
2. comparar conteúdo;
3. identificar data e sessão de origem;
4. verificar referências recebidas;
5. verificar se existe decisão que o substitui;
6. escolher o canônico;
7. mover o antigo para `history` ou `superseded`;
8. criar cabeçalho de status;
9. registrar o sucessor.

Cabeçalho recomendado:

```yaml
---
status: canonical | historical | superseded | draft | quarantine
mission: AGENT-FACTORY-DBTWIN-002
created_at: YYYY-MM-DD
supersedes: caminho/ou/null
superseded_by: caminho/ou/null
source_session: identificador
sha256_at_import: hash
---
```

---

## Etapa F — Validação das referências

Validar separadamente:

- links Markdown reais;
- referências textuais a arquivos;
- caminhos relativos;
- arquivos declarados, mas ausentes;
- referências não concretas;
- caminhos abreviados com `...`;
- referências para ZIP/TAR;
- divergência de maiúsculas/minúsculas;
- conflito entre caminhos antigos e estrutura canônica.

---

## Etapa G — Montagem do repositório limpo

1. Criar uma nova pasta de staging.
2. Copiar apenas os arquivos classificados e aprovados.
3. Não reorganizar diretamente em cima da pasta confusa.
4. Incluir:
   - README;
   - GOVERNANCE;
   - estrutura canônica;
   - decisões;
   - missões;
   - módulo DB Twin;
   - scripts de inventário e validação;
   - índices;
   - manifests.
5. Não incluir:
   - arquivos temporários;
   - cópias numeradas;
   - pacotes repetidos;
   - arquivos do sistema;
   - segredos;
   - dados reais;
   - caches;
   - `node_modules`;
   - volumes;
   - dumps não autorizados.

---

## Etapa H — Gate da baseline v1

A baseline somente poderá ser publicada quando houver:

- inventário integral das fontes reunidas;
- classificação de 100% dos arquivos;
- zero conflito canônico não resolvido;
- lista explícita de pendências;
- validação de referências;
- secret scan;
- árvore final aprovada;
- README honesto;
- versão da Fábrica separada da versão do DB Twin;
- manifesto pré-Git;
- hashes da árvore de importação;
- decisão humana.

---

## Etapa I — Publicação GitHub

Nome sugerido:

```text
denistein2/stein-agent-factory
```

Fluxo:

```text
main
└── bootstrap/repository-v1
```

Primeiro PR:

```text
chore(repo): establish Stein Agent Factory v1 foundation
```

Tag somente depois do merge e conferência:

```text
factory/v1.0.0-foundation
```

O PR deverá explicar explicitamente que esta é uma baseline organizacional, não conclusão técnica da DBTWIN-002.

---

## Etapa J — Migração para o Google Drive

1. Criar a estrutura canônica.
2. Copiar os arquivos do INBOX.
3. Subir pacotes e evidências pesadas.
4. Gerar índice com:
   - Drive file/folder ID;
   - nome;
   - hash local;
   - missão;
   - categoria;
   - caminho canônico;
   - URL;
   - data.
5. Somente depois mover a pasta antiga para `90_SUPERSEDED` ou `99_QUARANTINE`.
6. Não apagar a origem até a conferência de contagem, tamanho e hashes.

---

## 11. Protocolo obrigatório de fechamento de sessão

Toda sessão que altere o projeto deverá produzir:

```text
docs/sessions/YYYY/YYYY-MM-DD/SESSION_<ID>.md
```

Conteúdo mínimo:

- objetivo;
- contexto recebido;
- decisões;
- arquivos criados;
- arquivos alterados;
- arquivos removidos;
- comandos;
- evidências;
- testes;
- desvios;
- riscos;
- pendências;
- próximo passo;
- hash do estado;
- branch;
- commit;
- PR.

### Fluxo autônomo

```text
1. atualizar arquivos;
2. executar validações;
3. gerar fechamento da sessão;
4. criar branch;
5. commit;
6. push;
7. abrir PR;
8. anexar resumo e evidências;
9. registrar URL do PR;
10. encerrar a sessão.
```

### Nome de branch

```text
session/YYYY-MM-DD/<missao>-<resumo>
```

### Título de PR

```text
session(<missão>): <resultado principal>
```

### Regra de segurança

- PR autônomo: autorizado como objetivo operacional.
- Merge automático: proibido até nova decisão.
- Falha de validação: PR deve permanecer draft.
- Falha de push ou autenticação: sessão termina em `BLOCKED`, com pacote local e instruções de retomada.

---

## 12. Critérios de aceitação

A missão será considerada concluída quando:

- [ ] todas as fontes conhecidas forem coletadas;
- [ ] todo arquivo tiver SHA-256;
- [ ] todo arquivo tiver classificação;
- [ ] duplicatas idênticas e divergentes estiverem separadas;
- [ ] a cronologia das sessões estiver reconstruída;
- [ ] a árvore canônica estiver aprovada;
- [ ] o Drive estiver estruturado;
- [ ] o repositório GitHub existir;
- [ ] o primeiro PR estiver aberto;
- [ ] a baseline for mergeada após Gate Humano;
- [ ] a tag `factory/v1.0.0-foundation` estiver publicada após merge humano;
- [ ] o protocolo de fechamento estiver testado;
- [ ] uma sessão de prova criar PR de ponta a ponta;
- [ ] nenhum dado real ou segredo tiver sido versionado;
- [ ] os arquivos antigos estiverem preservados em histórico ou quarentena.

---

## 13. STOP GATES

### STOP-01 — Fontes faltantes

Parar se ainda houver arquivos relevantes somente no celular ou Claude sem coleta.

### STOP-02 — Duplicata divergente

Parar a canonicalização do conceito se houver dois candidatos diferentes e nenhuma decisão suficiente.

### STOP-03 — Segredo ou dado real

Parar imediatamente se forem encontrados:

- chaves;
- tokens;
- `.env`;
- credenciais;
- dumps reais;
- PII;
- dados de clientes.

Mover para quarentena segura e registrar sem expor o conteúdo.

### STOP-04 — Versão inconsistente

Parar a tag se a versão da Fábrica estiver sendo confundida com a versão técnica do DB Twin.

### STOP-05 — Exclusão sem custódia

Nenhuma exclusão antes de:

- hash;
- contagem;
- destino;
- backup;
- aprovação humana.

### STOP-06 — GitHub indisponível

Se o repositório ou autenticação não estiverem disponíveis, gerar pacote Git-ready e terminar como `BLOCKED_GITHUB`, sem fingir publicação.

---

## 14. Entregáveis finais

```text
INVENTORY_BASELINE.csv
INVENTORY_BASELINE.json
DUPLICATE_GROUPS.csv
SESSION_LEDGER.md
CANONICAL_FILE_MAP.csv
SUPERSEDED_MAP.csv
BROKEN_REFERENCES.md
DRIVE_INDEX.csv
MANIFESTO_PRE_GIT.md
REPOSITORY_TREE.txt
README.md
GOVERNANCE.md
SESSION_CLOSE_PROTOCOL.md
FIRST_PR_BODY.md
RELEASE_MANIFEST_foundation.json
```

---

## 15. Decisão recomendada agora

A ação imediata correta não é mover arquivos manualmente.

A ação correta é:

```text
1. congelar;
2. inventariar;
3. coletar celular/Claude/Drive;
4. comparar hashes;
5. classificar;
6. montar staging limpo;
7. revisar;
8. publicar por PR.
```

**Estado após emissão desta missão:** `READY_FOR_INVENTORY`
