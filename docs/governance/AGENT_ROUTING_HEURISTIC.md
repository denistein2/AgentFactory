# AGENT_ROUTING_HEURISTIC — Seleção de executor por capacidade e risco

**Missão de origem:** GOVERNANCE-RESET-FACTORY-001  
**Issue:** #3  
**Status:** candidato canônico até merge humano

## Regra-mãe

**Selecionar capacidade e papel primeiro; resolver provider/produto/modelo disponível depois.** Não hardcode um modelo como regra permanente quando a necessidade real é uma capacidade.

## Sequência de routing

```text
natureza da missão
→ risco
→ reversibilidade
→ capacidades requeridas
→ fontes/ferramentas necessárias
→ independência executor↔auditor
→ permissões disponíveis
→ Gate Humano necessário
→ custo/latência
→ executor/provider/modelo disponível
```

Custo e latência entram depois de capacidade, risco e permissão.

## Perguntas mínimas

1. A missão é leitura, escrita reversível, escrita canônica, execução, auditoria ou decisão?
2. O erro é barato de reverter?
3. Precisa de GitHub, Drive, browser, ambiente local, banco ou outro conector?
4. O mesmo agente estaria autocertificando sua própria entrega?
5. Existe permissão explícita para a operação?
6. Há Gate humano antes ou depois da etapa?
7. Qual executor disponível satisfaz essas condições com menor complexidade?

## Independência

Quando o custo do erro é alto e independência é material, executor e auditor devem ser diferentes por papel e, quando justificável, por produto/provider. `PROTOCOLO_CROSSAUDIT_01.md` continua sendo a esteira cara e não padrão.

## Routing padrão

- tarefa mecânica, reversível e autorizada → executor capaz, sem Gate adicional;
- leitura/auditoria read-only → agente com acesso às fontes, sem mutação;
- escrita em branch/Draft PR já autorizada → executor GitHub; merge continua humano;
- decisão de negócio/arquitetura canônica, expansão de escopo, produção, dado real, credencial ou destruição real → Gate Humano;
- verificação independente → auditor que não dependa da defesa privada do construtor.

## Registro

A escolha final deve aparecer no `MISSION_MANIFEST_STANDARD` como `requested_executor` e `actual_executor`, incluindo limitações e `does_not_prove`.
