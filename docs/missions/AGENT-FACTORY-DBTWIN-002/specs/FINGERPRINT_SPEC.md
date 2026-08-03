# FINGERPRINT_SPEC — Especificação de fingerprint reproduzível

**Status:** minuta de especificação (planejamento). Nenhum fingerprint calculado nesta sessão.
**Data:** 01/08/2026

> Corrige P0-02. Sem esta especificação, expressões como "bit a bit",
> "determinístico" e "o fingerprint bate" permanecem declarativas.

---

## 1. Relação de estados (corrigida)

A formulação anterior `inicial ≠ destrutivo = final` estava **errada**: afirmava
`destrutivo = final`, contradizendo o resultado da Fase 01. A relação correta,
sem ambiguidade de associatividade, é o conjunto de três afirmações:

```
inicial  = final
inicial ≠ destrutivo
final   ≠ destrutivo
```

Qualquer documento que precise expressar a relação usa **estas três linhas**,
nunca a cadeia `a ≠ b = c`.

> Referência dos valores declarados na Fase 01 (a **reconferir** por reprodução,
> nunca reusados como prova — ver `ESTRATEGIA_AUDITORIA.md`):
> - inicial/final: `1966329b…b035f219`
> - destrutivo:    `87a9fe6c…c7c6292c`
> Os valores acima estão **abreviados de propósito**; o artefato real exige hash
> completo (§3).

## 2. Algoritmo e identidade

- **Algoritmo:** SHA-256 (a fixar formalmente no manifesto; se a Fase 01 usou
  outro, registrar e justificar — não presumir).
- **Hash completo obrigatório:** 64 hex chars. Abreviação só em prosa
  explicativa, nunca em manifesto.
- **Objeto do fingerprint:** definir explicitamente **o que** entra —
  proposta: dump lógico canonicalizado do estado de dados+objetos alvo, não o
  arquivo bruto do container.

## 3. Canonicalização (pré-condição do determinismo)

> **Aviso de segurança (corrige P1-REV-06).** Owner, memberships e privilégios são
> parte **material** da semântica de `SECURITY DEFINER`, RLS e grants. Se forem
> normalizados no fingerprint **estrutural/de segurança**, dois schemas com
> comportamentos de segurança diferentes podem parecer iguais. Por isso a
> normalização de identidades só é permitida no **fingerprint de dados** — nunca
> no estrutural/de segurança.

### 3.1 Fingerprint de dados (pode normalizar identidades operacionais)

Antes de hashear, normalizar o que varia sem mudar semântica de dados:

| Fonte de variação | Tratamento |
|---|---|
| Ordenação de linhas/objetos | `ORDER BY` canônico estável por chave |
| Timestamps de geração | excluídos do escopo hasheado |
| OIDs | excluídos/normalizados |
| Owners / roles efêmeras **operacionais** | normalizados para papel lógico |
| Valores correntes de sequences | conforme fronteira de estado (ver `SCHEMA_INVENTORY_SPEC` e P1-12) |
| Encoding / locale / collation | fixados e declarados (ver pinagem de ambiente) |
| Fim de linha / whitespace | normalizados |

### 3.2 Fingerprint estrutural/de segurança (preserva a relação de privilégios)

**Não** normaliza a relação de privilégios. Preserva, com aliases **lógicos**
(nunca apagando a relação):

- **owner lógico** de cada objeto;
- **grants** por role;
- **memberships** de role;
- **`BYPASSRLS`**;
- **`SECURITY DEFINER`** e o **owner** que define o privilégio efetivo;
- **`search_path`** fixado de cada função definer;
- estado de **RLS**/`FORCE ROW LEVEL SECURITY` por tabela.

O mapeamento pode usar aliases lógicos para roles (`role_authenticated`,
`role_service`), mas **a relação de privilégios entre eles não pode desaparecer**.
Dois schemas com privilégios diferentes **devem** produzir fingerprints
estruturais diferentes.

## 4. Escopo por tipo de fingerprint

- **Fingerprint de estado de dados:** conteúdo das tabelas-alvo após canonicalização (§3.1 — pode normalizar identidades operacionais).
- **Fingerprint estrutural/de segurança:** owner lógico, grants, memberships, `BYPASSRLS`, `SECURITY DEFINER`, `search_path`, RLS/FORCE (§3.2 — **não** normaliza a relação de privilégios).
- **Fingerprint de inventário de objetos:** lista canônica de objetos do schema
  (ver `SCHEMA_INVENTORY_SPEC.md`) — separado do estado de dados.
- **Fingerprint de fixture:** hash do artefato de fixture versionado.

Os quatro são registrados **separadamente**; não se colapsam num número único.
Em especial, o **de dados** e o **estrutural/de segurança** são distintos: um
schema pode ter os mesmos dados e privilégios diferentes.

## 5. Pendências

- **FP-1.** Confirmar o algoritmo efetivamente usado na Fase 01 antes de comparar.
- **FP-2.** Definir a ferramenta de canonicalização (script determinístico, versionado e ele próprio hasheado).
- **FP-3.** Decidir tratamento de sequences no fingerprint (definição vs. valor corrente).
