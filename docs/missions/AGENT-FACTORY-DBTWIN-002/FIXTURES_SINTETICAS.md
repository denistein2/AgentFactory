# FIXTURES_SINTETICAS — Dados de teste próprios para o gêmeo comportamental

**Status:** especificação de planejamento. Nenhuma fixture gerada/executada.
**Data:** 01/08/2026

> **Nenhuma fixture será derivada de Roger, Kellen ou de qualquer cliente real.**
> Todos os dados abaixo são fictícios, próprios e desenhados para provar
> comportamentos da arquitetura do produto.

---

## 1. Critérios obrigatórios

Toda fixture deve ser:
- **Relevante** — representa um cenário real do domínio (produção de alimentos/receitas/estoque).
- **Determinística** — mesma execução → mesmo resultado (IDs, ordem e seeds fixos).
- **Versionável** — mora no repositório em `fixtures/` (whitelisting explícito; ver `VERSIONAMENTO_GIT.md`).
- **Mínima** — apenas o necessário para cada prova; sem volume supérfluo.
- **Adversarial quando preciso** — inclui casos que **devem** falhar/bloquear, para provar invariantes.

## 2. Entidades sintéticas base (fictícias)

- **Produto fictício:** ex. "Bolo de Teste".
- **Variantes:** válidas e uma inválida (para prova negativa).
- **Ficha técnica sintética:** composição controlada.
- **Ingredientes e sub-receitas:** com quantidades conhecidas.
- **Estoque inicial conhecido:** valores fixos para conferência de baixa/crédito.
- **Pedidos / ordens de produção artificiais:** OPs com efeito previsível.
- **Tenants fictícios:** Tenant A e Tenant B (para isolamento).
- **Usuários/perfis fictícios:** por role (`anon`, `authenticated`), sem Auth real.

> Todos os identificadores são claramente sintéticos, mas **compatíveis com os
> tipos reais** (corrige P1-10). Prefixos como `TENANT_A`/`SYN-` são apenas
> **aliases legíveis**; o valor real respeita o tipo da coluna (UUID, enum, FK).

### 2.1 Catálogo de aliases → valores determinísticos (P1-10)

Onde a coluna for UUID, usar UUIDs válidos, versão 4, **determinísticos**:

```
TENANT_A = 00000000-0000-4000-8000-000000000001
TENANT_B = 00000000-0000-4000-8000-000000000002
SYN-USER-ANON          = 00000000-0000-4000-8000-000000000010
SYN-USER-AUTHENTICATED = 00000000-0000-4000-8000-000000000011
```

Enums e FKs usam valores que **existem** no schema-only; nenhum alias textual é
inserido cru numa coluna tipada. O catálogo de aliases é versionado junto às
fixtures.

## 3. Catálogo inicial de cenários

| ID | Cenário | Tipo | Oracle |
|---|---|---|---|
| CN-01 | OP com sub-receita | normal | PENDENTE DE ORACLE CANÔNICO (composto; decompor em atômicos — ver §3.2) |
| CN-02 | Estoque suficiente | normal | PENDENTE DE ORACLE CANÔNICO |
| CB-01 | Estoque no limite exato | borda | PENDENTE DE ORACLE CANÔNICO |
| CB-02A | Quantidade zero | borda | PENDENTE DE ORACLE CANÔNICO (constraint + SQLSTATE a identificar) |
| CB-02B | Quantidade fracionada | borda | PENDENTE DE ORACLE CANÔNICO (unidade/regra a identificar) |
| AD-01 | Variante inválida | adversarial | PENDENTE DE ORACLE CANÔNICO (camada a nomear: FK/constraint/trigger/função/policy) |
| AD-02 | Estoque insuficiente | adversarial | PENDENTE DE ORACLE CANÔNICO (bloqueia **ou** permite — decisão do produto) |
| AD-03 | Acesso cross-tenant (A lê B) | adversarial | PENDENTE DE ORACLE CANÔNICO (esperado: negado por RLS — confirmar no inventário) |
| AD-04 | `anon` em recurso `authenticated` | adversarial | PENDENTE DE ORACLE CANÔNICO (esperado: negado por policy — confirmar camada) |
| AD-05 | Escrita fora do tenant do JWT | adversarial | PENDENTE DE ORACLE CANÔNICO (confirmar camada e efeito) |
| AD-06 | Sub-receita com ciclo/ref inválida | adversarial | PENDENTE DE ORACLE CANÔNICO (separar em casos distintos) |

> **Regra (P1-REV-03):** nenhum comportamento aparece como "esperado" antes de a
> fonte/oracle estar definida. Cada oracle é preenchido na tabela de §3.1 a partir
> de regra canônica do produto; até lá, o catálogo permanece `PENDENTE DE ORACLE
> CANÔNICO`. Os cenários de segurança (AD-03/04/05) trazem a expectativa apenas
> como **hipótese a confirmar** no inventário, não como oracle fechado.

> Exemplo-guia (do briefing): "Uma OP com sub-receita baixa corretamente os
> insumos, credita o produto acabado, respeita o tenant e não aceita variante
> inválida." — coberto por CN-01 + AD-01.

### 3.1 Cada cenário referencia uma regra canônica (corrige P1-08)

Vários cenários embutiam **decisão de negócio** não fundamentada (ex.: AD-02
"estoque insuficiente bloqueia OP" é decisão do produto, não consequência técnica
universal; no projeto, um default não deve endurecer silenciosamente em
comportamento permanente). Cada cenário passa a citar regra, fonte e **oracle
exato**:

| Cenário | Regra | Fonte | Oracle exato |
|---|---|---|---|
| AD-02 | Estoque insuficiente bloqueia OP | decisão humana/regra do produto (a confirmar) | bloqueia **ou** permite — definir |
| CB-02A | quantidade zero | constraint X (a identificar) | erro SQLSTATE Y |
| CB-02B | quantidade fracionada | unidade/regra Z (a identificar) | valor final esperado |
| AD-01 | variante inválida | **camada** a nomear (FK/constraint/policy/função) | rejeição na camada correta |

### 3.2 Atômico antes de composto (P1-08)

CN-01 testa vários comportamentos ao mesmo tempo (baixa + crédito + tenant +
variante). Cenários **compostos** só existem **depois** dos **atômicos**
correspondentes passarem. Cada comportamento vira um teste atômico próprio antes
de entrar num cenário composto.

## 4. Falha limpa ≠ ausência de evidência (corrige P1-09)

A formulação anterior confundia as duas. O correto:

```
Sem estado de domínio parcial.
Com registro de evidência COMPLETO.
```

Todo `EXPECTED_FAIL` **produz** evidência completa de que: falhou **pelo motivo
esperado** (SQLSTATE/erro previsto); **não** alterou estado de domínio; fez
**rollback**; deixou o banco no **fingerprint esperado**. O manifesto de teste é
**concluído** mesmo quando o cenário falha como esperado. O que não deve existir é
**estado de domínio parcial** — não a evidência.

## 5. Determinismo e seeds

- Seeds fixos e documentados por cenário.
- IDs atribuídos explicitamente (não aleatórios).
- Fingerprint de cada fixture registrado, permitindo prova de que a mesma fixture foi usada.

## 6. Fronteira

As fixtures provam **arquitetura e regras**, não replicam a operação de nenhum cliente. Reproduzir defeito que dependa de dados reais é missão separada (`AGENT-FACTORY-INCIDENT-REPRO-001`), fora daqui.

## 7. Pendências

- **FX-1.** Mapear cada cenário aos objetos concretos do schema-only (depende de PEND-1/inventário).
- **FX-2.** Definir formato das fixtures (SQL semente vs. loader) compatível com o whitelisting do `.gitignore`.
