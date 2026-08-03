# PROTOCOLO CROSS-AUDIT 01 — Dupla Construção, Auditoria Cruzada e Gate Humano

**Projeto:** Stein Agent Factory
**Natureza:** protocolo de controle de qualidade interno da fábrica
**Função:** decidir o que vira regra canônica, com defesa em quatro níveis
**Documento:** canônico
**Data de emissão:** 2026-08-02T14:44:01-0300
**Dependência:** herda a custódia de arquivos do PROTOCOLO_EXCHANGE_01 (nomes versionados, não-sobrescrita, manifesto, reconferência por re-download)

---

## 0. Critério de entrada (FREIO — leia antes de tudo)

> **Este protocolo é caro. Não é o modo padrão de trabalho.**
> A esteira completa — construção cega, congelamento, auditoria cruzada, reconciliação, gate humano — só se justifica quando o custo de um erro é alto E a divergência entre modelos é informativa. Para a maioria das decisões, uma construção simples com revisão basta.

**Uma decisão QUALIFICA para a esteira completa quando atende a pelo menos DOIS destes:**

- erro é dispendioso ou difícil de reverter (RLS, permissões, política de cancelamento, contrato de agente, arquitetura estrutural);
- há tensão real entre alternativas legítimas (não uma resposta óbvia);
- a decisão vira regra canônica que outras decisões herdarão;
- toca dados, segurança ou fronteira entre fábricas.

**Uma decisão NÃO qualifica quando:**

- a resposta é convergente e óbvia (os dois agentes produzirão o mesmo);
- é reversível a baixo custo;
- é puramente mecânica ou de formatação;
- o overhead do circuito custa mais do que o erro que ele previne.

**Regra de proteção do ERP:** a fábrica é infraestrutura de suporte ao ERP Food Control. Nenhuma missão cross-audit deve furar a fila de uma atividade do ERP dentro da janela de 60 dias. Se a esteira for aplicada, aplicá-la a uma decisão **real e já enfileirada** do ERP — não a um objeto sintético auto-referente.

---

## 1. Arquitetura dos papéis

```
GPT
├── construtor da proposta A
└── auditor da proposta B

Claude
├── construtor da proposta B
└── auditor da proposta A

Codex
├── executor local
├── verificador de hashes, arquivos, referências e diferenças
└── montador da matriz de reconciliação (NUNCA decisor)

Denis
└── decisor da regra, régua de negócio e Gate
```

---

## 2. Fluxo em sete fases

### Fase 1 — Entrada comum imutável

Pacote de origem com: MISSÃO, FONTES, RESTRIÇÕES, PERGUNTAS A RESPONDER, CRITÉRIOS DE ACEITAÇÃO. Recebe tamanho e SHA-256. Os dois construtores recebem exatamente os mesmos bytes.

### Fase 2 — Construção cega (com congelamento mecânico)

Sem ver a resposta do outro:

```
GPT   → GPT_CONSTRUCAO__v001.md
Claude → CLAUDE_CONSTRUCAO__v001.md
```

Cada entrega acompanha: arquivo, manifesto, tamanho, SHA-256, fontes utilizadas, suposições, decisões não tomadas.

> **REFORÇO 1 — congelamento é ato mecânico, não convenção.**
> A Fase 2 termina com um `FREEZE_MANIFEST` por artefato: SHA-256 + timestamp + declaração "nenhuma versão posterior existe neste instante". O congelamento é verificável, não prometido. A não-sobrescrita já é garantida pelos nomes versionados do EXCHANGE-01.

### Fase 3 — Troca controlada

Os pacotes são cruzados. Cada auditor recebe: a missão original, as fontes originais, o artefato do outro construtor, e uma régua de auditoria comum.

> **REFORÇO 2 — invariante de independência do auditor.**
> O auditor vê **missão + fontes + artefato + régua. Nada mais.** A defesa informal, o raciocínio ou o contexto adicional do construtor NÃO chegam ao auditor nesta fase. Contaminar isso destrói a avaliação pelos méritos. A defesa do construtor só aparece na Fase 5, depois do parecer emitido.

### Fase 4 — Auditoria cruzada

Cada auditor classifica os achados:

```
CONFORME
CORREÇÃO OBJETIVA
CONTRADIÇÃO
LACUNA DE EVIDÊNCIA
DECISÃO HUMANA NECESSÁRIA
MELHORIA OPCIONAL
FORA DE ESCOPO
```

Não misturar: erro técnico ≠ preferência de arquitetura ≠ decisão de negócio.

### Fase 5 — Direito de resposta (com teto de rodadas)

Cada construtor responde à auditoria do seu arquivo:

```
ACEITO
ACEITO PARCIALMENTE
CONTESTO COM EVIDÊNCIA
DECISÃO HUMANA NECESSÁRIA
```

Se houver correção, nasce v002. A v001 permanece arquivada. Nada é apagado.

> **REFORÇO 3 — teto de uma rodada (herda M18).**
> Máximo de uma rodada de resposta: v001 → v002. Se após a v002 a divergência persistir, ela NÃO volta para auditoria — sobe direto para `DECISÃO HUMANA ABERTA` na Fase 7. Alerta-se uma vez, registra-se, não se reabre a mesma objeção sem novo fato. A auditoria cruzada tem o mesmo direito de fechar que Denis tem.

### Fase 6 — Reconciliação (Codex consolida, não decide)

O Codex recebe todos os artefatos, auditorias e manifestos e gera a matriz de reconciliação.

> **REFORÇO 4 — fronteira do executor (herda M17).**
> O Codex só preenche células que sejam **fatos verificáveis**: existe/não existe, hash confere/não confere, trecho X diverge do trecho Y. No momento em que uma célula exigir julgamento ("qual é melhor"), o valor obrigatório é `DECISÃO HUMANA`. O Codex NUNCA preenche uma célula com preferência e NUNCA cria meio-termo automático. Ele consolida fatos; Denis decide regras.

Formato da matriz:

| Tema | GPT | Claude | Auditor GPT | Auditor Claude | Estado |
|---|---|---|---|---|---|
| Regra A | proposta | proposta | parecer | parecer | consenso |
| Regra B | proposta | proposta | divergência | divergência | decisão humana |
| Evidência C | presente | ausente | confirmado | confirmado | lacuna |

### Fase 7 — Decisão humana

Denis recebe três blocos: CONSENSOS, CORREÇÕES OBJETIVAS, DECISÕES HUMANAS ABERTAS. E decide:

```
APROVAR PROPOSTA GPT
APROVAR PROPOSTA CLAUDE
APROVAR COMBINAÇÃO ESPECÍFICA
DEVOLVER PARA NOVA RODADA
NÃO ADOTAR
```

Só depois nasce o documento canônico.

---

## 3. Estrutura no Drive (por missão)

```
Stein Agent Factory/
└── Exchange/
    └── EXCHANGE-CROSSAUDIT-XXX/
        ├── 00_QUARANTINE/
        ├── 10_SOURCE_LOCKED/
        ├── 20_GPT_CONSTRUCTION/
        ├── 21_CLAUDE_AUDIT/
        ├── 30_CLAUDE_CONSTRUCTION/
        ├── 31_GPT_AUDIT/
        ├── 40_CODEX_RECONCILIATION/
        ├── 50_HUMAN_DECISION/
        └── 90_ARCHIVE/
```

Nenhum arquivo é substituído. Herda todas as regras de custódia do EXCHANGE-01.

---

## 4. Quatro níveis de defesa

1. construção independente (diversidade real antes do consenso);
2. crítica adversarial (auditoria cruzada);
3. verificação mecânica (Codex);
4. decisão humana (Gate de Denis).

Evita quatro falhas: agente autocertificar sua entrega; dois agentes concordarem por ancoragem; Codex inventar decisão de negócio; Denis receber vinte arquivos sem saber onde está a divergência real.

---

## 5. Fronteira com ferramentas de mercado

O núcleo de valor (custódia criptográfica, não-sobrescrita, separação erro/preferência/negócio, autoridade humana do gate) é **governança**, não orquestração. Ferramentas como Agents SDK, AutoGen ou LangGraph podem servir de transporte/orquestração, mas não fornecem essas invariantes.

> **ATENÇÃO:** AutoGen por padrão faz os agentes compartilharem contexto e iterarem até aprovação — o oposto da construção cega (Fase 2 / REFORÇO 2). Se usar orquestração de mercado, a forma dela não deve diluir as invariantes deste protocolo.

---

## 6. Pendências abertas

### PEND-CROSSAUDIT-1 — objeto do primeiro teste (DECISÃO DE DENIS)

O objeto proposto `EXCHANGE-CROSSAUDIT-001` (definir política de nomenclatura/arquivamento do próprio Exchange) é auto-referente: essa política **já existe** no PROTOCOLO_EXCHANGE_01. Duas leituras, testes distintos:

- **Leitura A — validar o mecanismo:** o objeto é só pretexto de baixo risco. Nesse caso os agentes devem construir **sem** ver o protocolo existente, senão convergem por ancoragem e a auditoria não encontra divergência para exercitar.
- **Leitura B — melhorar a política existente:** o protocolo atual entra como FONTE do pacote imutável, e a pergunta vira "o que falta/está errado" — o que é auditoria, não construção cega.

As duas são legítimas mas diferentes. Denis decide qual, antes de montar `10_SOURCE_LOCKED`.

**Recomendação de sequência (proteção dos 60 dias):** o cross-audit NÃO deve entrar antes do teste EXCHANGE-01 (Etapa 0 + transferência sintética Drive↔local), que é barato e desbloqueia o trabalho remoto. Quando entrar, aplicar preferencialmente a uma decisão **real já enfileirada** do ERP, conforme §0.

---

## Changelog

- **v001 (2026-08-02):** emissão canônica. Sobre o desenho original de dupla construção:
  - §0: adicionado **critério de entrada** (freio de complexidade / proteção dos 60 dias do ERP).
  - REFORÇO 1: congelamento como ato mecânico (FREEZE_MANIFEST).
  - REFORÇO 2: invariante de independência do auditor.
  - REFORÇO 3: teto de uma rodada de resposta (herda M18).
  - REFORÇO 4: fronteira do executor Codex (herda M17).
  - §6: marcado **PEND-CROSSAUDIT-1** (objeto do primeiro teste — decisão de Denis).
