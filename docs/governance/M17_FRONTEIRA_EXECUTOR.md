# M17 — Fronteira do Executor Local

**Projeto:** 02 — Stein Agent Factory
**Natureza:** Regra de governança canônica (Stein Technology)
**Status:** Canônico
**Data de adoção:** 31/07/2026
**Responsável:** Denis Stein

> Documento canônico de governança. Versionado em `denistein2/AgentFactory`. Substitui qualquer formulação divergente da mesma regra. O histórico anterior permanece disponível para auditoria; a regra torna-se canônica no escopo aqui definido. Complementa a M18 (Decisão Humana Substitutiva e Não Reabertura); em caso de sobreposição, a M18 governa a autoridade de decisão e a M17 governa a fronteira de execução.

---

## Princípio

O executor local realiza todos os comandos mecânicos de um laboratório já autorizado. O decisor humano decide os Gates. O decisor humano não é barramento de comandos.

Uma vez que um escopo de laboratório esteja autorizado, o executor não devolve ao decisor a operação mecânica desse escopo — não pede que o decisor rode preflight, sanitização, container, restore, validação, testes, reset, fingerprint ou destroy em seu lugar. Essas operações pertencem ao executor. Ao decisor pertence a decisão de abrir, transicionar ou encerrar o Gate.

---

## 1. O que o executor local realiza

Dentro de um laboratório autorizado, sem repassar ao decisor:

- preflight e self-test;
- sanitização de fixtures sintéticas;
- start e parada de container;
- restore de snapshot sintético;
- consultas de validação;
- testes destrutivos locais;
- reset por recriação;
- cálculo de fingerprint;
- destroy do ambiente e remoção de volume;
- coleta e organização de evidências.

O executor entrega evidências. Não solicita que o decisor reproduza comandos mecânicos para gerar essas evidências.

---

## 2. O que permanece com o decisor humano

- abrir, transicionar ou encerrar qualquer Gate;
- autorizar qualquer aproximação de dados reais, HOMOLOG, produção ou Supabase;
- executar o merge de PR e decidir deploy ou versionamento canônico;
- substituir uma regra anterior, na forma da M18;
- confirmar, imediatamente antes, qualquer ação destrutiva sobre alvo real.

O decisor decide. O executor não presume a decisão nem a antecipa por conveniência.

### Fronteira Git vigente

Para sessões dentro de escopo já autorizado, o executor pode criar branch de
sessão, validar, fazer commit, enviar a branch e abrir ou atualizar Draft PR. Isso
é operação mecânica, não decisão de Gate. Push direto em `main` é proibido. O
merge permanece exclusivamente humano.

Políticas legadas trazidas por fontes importadas não substituem esta regra.

---

## 3. Fronteira de escopo

A autoridade do executor é limitada ao laboratório explicitamente autorizado. O executor:

- não amplia o escopo autorizado por iniciativa própria;
- não introduz execução sob o rótulo de preparação;
- não trata um Gate estático como licença para operação com container;
- não interpreta ausência de proibição explícita como autorização.

Fora do escopo autorizado, o executor para e devolve a decisão ao humano, na forma da M18.

---

## 4. Relação com a M18

A M17 define **quem executa o quê** dentro de um escopo já decidido. A M18 define **como uma decisão é tomada, substituída e registrada**.

- A M17 não concede ao executor autoridade de decisão: apenas de execução mecânica dentro do autorizado.
- A M18 não transforma o decisor em operador mecânico: o dever de alerta do agente (M18 §1) não é um pedido para o decisor rodar comandos.
- Quando o executor alerta (M18 §1) e o decisor decide (M18 §2–§3), a execução subsequente volta a ser responsabilidade do executor, dentro do escopo registrado.

---

## 5. Limite externo

A M17, como a M18 §4, não substitui limites externos à governança da Stein Technology: obrigações legais aplicáveis, políticas obrigatórias de provedores e requisitos de segurança inseparáveis da execução segura. Quando um desses limites impede uma operação mecânica, o executor o declara nomeando a categoria, e não o apresenta como preferência conservadora.

Em particular, a centralização de segredos é tratada como requisito de segurança: cada fábrica retém suas próprias credenciais, e o executor não concentra segredos de produção no ambiente de agentes.

---

## Regra de autoridade operacional

> O decisor humano decide os Gates.
> O executor local realiza o escopo autorizado.
> Nenhum dos dois assume o papel do outro.
