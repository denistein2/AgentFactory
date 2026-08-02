# VALIDACAO_SUPABASE — Semântica Supabase vs. PostgreSQL puro

**Status:** planejamento. Nenhuma conexão Supabase nesta sessão.
**Data:** 01/08/2026

> Um schema-only restaurado em PostgreSQL puro **não** reproduz automaticamente a
> semântica Supabase. Este documento separa o que pode ser **restaurado
> diretamente**, o que precisa ser **reproduzido semanticamente** e o que deve
> ser **simulado** — e proíbe melhorias oportunistas.

---

## 1. Classificação por tratamento

| Elemento | Restaura direto | Reproduz semanticamente | Simula | Nota |
|---|:---:|:---:|:---:|---|
| Tabelas/colunas/tipos/enums | ✅ | | | DDL padrão |
| Constraints/índices/sequences | ✅ | | | DDL padrão |
| Views / materialized views | ✅ | | | Revisar dependências |
| Funções / RPCs | ✅ | ⚠ | | Cuidar de `search_path`/owner |
| Triggers | ✅ | | | Dependem de funções |
| Extensões | ⚠ | ⚠ | | Precisam existir no destino |
| **RLS habilitada** | ✅ | | | Flag por tabela |
| **Policies** | ✅ | ⚠ | | Dependem de roles/claims JWT |
| **Grants/permissões** | ⚠ | ⚠ | | Dependem de roles existirem |
| Roles do Supabase (`anon`, `authenticated`, `service_role`) | | ⚠ | ✅ | Reproduzir papéis, não clonar segredos |
| `SECURITY DEFINER` / ownership | | ⚠ | | Owner define privilégio efetivo |
| `search_path` | | ✅ | | Fonte comum de bug de segurança |
| **JWT / claims** (`auth.uid()`, `auth.jwt()`) | | | ✅ | Simular claims em teste, sem Auth real |
| **Tenant** (multi-tenant) | | ✅ | ✅ | Fixtures de tenants fictícios |
| `auth.users` / sessões / identidades | | | ✅ | **Nunca clonar**; simular referências |
| Storage / buckets | | | | Fora de escopo desta missão |

Legenda: ✅ direto · ⚠ requer cuidado/condição · (vazio) não aplicável.

## 2. Pontos de atenção de segurança

- **`SECURITY DEFINER` + `search_path`:** funções definer com `search_path` aberto são vetor clássico de escalonamento. A validação confirma o `search_path` fixado de cada função definer — **verificar fidelidade**, não "consertar".
- **Policies dependem de roles e de claims:** sem `authenticated`/`anon` reproduzidos e sem claims JWT simuladas, as policies não exercem o comportamento real. A simulação de claims é feita **em teste**, sem instanciar Auth real nem segredos.
- **Grants exigem roles existentes:** reproduzir os papéis (`anon`, `authenticated`, `service_role`) como **roles locais equivalentes**, sem importar segredos nem `service_role` real.

## 3. Como provar o comportamento (com fixtures sintéticas)

Cada regra sensível vira um cenário determinístico:
- tenant A não enxerga linhas de tenant B (RLS);
- `anon` bloqueado onde só `authenticated` acessa;
- RPC `SECURITY DEFINER` respeita o `search_path` fixado;
- variante inválida é rejeitada pela **camada canônica identificada no inventário**
  (FK, constraint, trigger, função ou policy), no tenant correto — não se presume policy.

Os cenários vivem em `FIXTURES_SINTETICAS.md` e são reproduzíveis sem Auth real.

## 3.1 Plano operacional executável (corrige P1-11)

A classificação da §1 não é plano. O plano executável exige, **conforme aplicável
ao produto**, definir e testar concretamente:

- role usada na conexão; `SET ROLE`; memberships; `BYPASSRLS`;
- owners; `ALTER DEFAULT PRIVILEGES`; privilégios de schema; `EXECUTE` em funções;
- função local equivalente a `auth.uid()` e `auth.jwt()`; **formato exato das claims**;
- comportamento com claims **ausentes ou malformadas**;
- `FORCE ROW LEVEL SECURITY` onde aplicável;
- teste de RPC `SECURITY DEFINER` (owner + `search_path` fixado);
- tratamento de `service_role` (papel local equivalente, **sem** segredo real);
- funções do schema `auth` que o produto use;
- publicações/realtime e outros objetos Supabase **se** fizerem parte do produto.

> **Atribuição de responsabilidade (P1-11 / P1-08).** "Policy nega variante
> inválida" pode estar atribuindo a uma **policy** o que é responsabilidade de
> **FK, constraint ou função**. Cada cenário deve nomear a **camada** exata que
> rejeita (RLS vs. constraint vs. trigger vs. função), não presumir policy.

## 4. Proibição de melhoria oportunista

> **Primeiro fidelidade, depois evolução.** Se a validação revelar uma policy
> frágil, um `search_path` aberto ou um grant amplo demais, isso é **registrado
> como achado**, não corrigido nesta missão. Correção pertence a missão de
> evolução própria, com seu próprio gate.

## 4.1 Fronteira de estado — matviews e sequences (P1-12)

Distinguir **definição** de **estado operacional**: inclui-se a definição da
materialized view e da sequence; **exclui-se** o conteúdo materializado e o valor
corrente. A inicialização local é determinada **pelas fixtures**, não herdada de
estado real. Detalhe em `specs/SCHEMA_INVENTORY_SPEC.md §2`.

## 5. Pendências / hipóteses

- **SB-1.** Mapa exato role-produto → role-local — **hipótese a validar** (PEND-4).
- **SB-2.** Quais extensões o produto exige e sua disponibilidade no destino — inventário pendente.
- **SB-3.** Forma de simular claims JWT em teste de modo determinístico e sem segredos — definir.
- **SB-4.** Formato exato das claims e comportamento com claims ausentes/malformadas — definir.
