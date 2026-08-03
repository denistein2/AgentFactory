# POLITICA_ISOLAMENTO_REDE — Controles estruturais + STOP GATES

**Status:** proposta de planejamento. Nenhum controle aplicado nesta sessão.
**Data:** 01/08/2026

> Fase 01 provou bloqueio remoto **por guard de ambiente**. A Fase 02 exige
> **controles estruturais** que provem o bloqueio, não apenas o declarem.

---

## 1. Princípio

Substituir a dependência **exclusiva** de guards de ambiente por defesa em camadas: guard **+** controle estrutural **+** prova verificável de ausência de conexão remota.

## 2. Camadas propostas

| Camada | Controle | Prova esperada |
|---|---|---|
| L1 — Bind | serviço apenas em `127.0.0.1` (loopback) | `ss`/`netstat` sem listener em interface pública |
| L2 — Allowlist | destinos de escrita explicitamente permitidos (lista curta) | tentativa fora da lista → recusa registrada |
| L3 — Denylist | HOMOLOG real (`bucphzinpsndsagonwiq`) e produção sempre bloqueados | rota a esses destinos inexistente/negada |
| L4 — Resolução de destino | resolver e **fixar** host/porta antes de qualquer comando | destino confirmado por evidência, não presumido |
| L5 — Egress | bloqueio de saída quando aplicável (rede do container sem rota externa de escrita) | ausência de conexão remota comprovada |
| L6 — Prova | captura de conexões durante o ciclo | `remote_database_accesses = 0`, como na Fase 01, agora estrutural |

> Nuance preservada da Fase 01: **zero acesso a banco remoto ≠ zero rede**. Um
> pull público de imagem pode ocorrer; isso é registrado e distinguido de
> conexão a banco remoto. A allowlist trata registries separadamente de bancos.

### 2.1 Rigor estrutural exigido (corrige P0-07)

Os controles anteriores tinham lacunas reconhecidas: bind em loopback controla
**entrada**, não **saída**; a denylist usava um *project ref* textual, não hosts/
IPs/protocolos; observar conexões **depois** não impede conexão; e um banco
remoto pode ser alcançado por Postgres, pooler, HTTPS REST/RPC ou APIs de
gerenciamento. A política, para PC/Gate 02-B, precisa fechar:

| Item | Definição exigida |
|---|---|
| Topologia | rede Docker interna **sem rota de egress**; postgres local + executor dentro dela |
| Camada do bloqueio | declarar **onde** (Windows / WSL / Docker network / container / processo) |
| Protocolos/portas | lista fechada do que é permitido; todo o resto negado |
| Resolução DNS | resolver e **fixar** IP no preflight; revalidar imediatamente antes do uso (evita troca de DNS entre validação e execução) |
| Registry | acesso permitido **somente antes** da execução (pull), fechado durante o ciclo |
| Vetores de banco remoto | bloquear **todos**: 5432/pooler/REST/RPC/mgmt — não só a porta Postgres |

Topologia-alvo (proposta):
```
host
└─ Docker network interna, sem rota de egress
   ├─ postgres local (loopback, porta canônica/preflight)
   └─ executor/test runner
```

## 3. Allowlist / Denylist (proposta inicial)

```
ALLOWLIST (escrita):
  - 127.0.0.1:<porta canônica a definir>      # destino local do gêmeo

DENYLIST (sempre bloqueado):
  - HOMOLOG real: bucphzinpsndsagonwiq
  - qualquer host de produção
  - qualquer destino de escrita não confirmado
```

> Porta canônica: **decisão necessária** (PEND-3) — 54329 não provada neste host (reserva WinNAT `54299–54398`); 55439 provada na Fase 01.

## 4. STOP GATES (antes de qualquer comando com capacidade de escrita)

**Correção P1-05 (tensão com M17).** "STOP gate humano em todo comando de escrita"
transformaria Denis em barramento de comandos, contra M17. Os controles são
separados em três camadas — só a terceira envolve o humano:

1. **Preflight automático (toda escrita):** destino resolvido e exibido
   (host:porta), estado anterior capturado, allowlist/denylist checadas
   **pelo executor**, sem intervenção humana.
2. **STOP técnico automático (fora da allowlist ou na denylist):** o executor
   **PARA** sozinho; não pede permissão para recusar — recusa é automática.
3. **Confirmação humana inequívoca (M18 §3):** exigida **somente** para ação
   **destrutiva, irreversível, expansão de escopo ou mudança de destino** —
   não para toda escrita.

> STOP técnico é bloqueio ativo automático, não aviso passivo. A confirmação
> humana fica reservada ao que é destrutivo/irreversível, preservando M17
> (executor roda o mecânico; Denis não é barramento) e M18 (humano confirma o
> destrutivo).

## 5. Prova de ausência de conexão remota

- Captura de conexões durante todo o ciclo, com **método de medição definido**
  (corrige P0-07): ferramenta declarada, escopo (todos os vetores: 5432/pooler/
  REST/RPC/mgmt), tratamento de falsos negativos, e ponto de coleta.
- `remote_database_accesses = 0` só é aceito com a **definição de como foi
  medido** — o número sozinho não é prova.
- Manifesto final registra `remote_database_accesses` e distingue rede-de-registry
  de rede-de-banco.
- Divergência (qualquer acesso a banco remoto inesperado) → STOP + escalonamento.

### 5.1 Porta: configurável e provada, não necessariamente canônica fixa (P2-01)

Em vez de eleger um número permanente, o contrato pode exigir, por preflight:
loopback; **porta livre** (sem listener anterior); valor **registrado no
manifesto**; validação de allowlist. A porta 55439 (provada na Fase 01) serve de
default; 54329 permanece **decisão em aberto**, não bloqueio. Uma porta
configurável e provada em preflight tende a ser mais robusta que um número fixo.

## 6. O que NÃO é prometido aqui

- Esta política é **planejamento**. A prova real de cada camada só existe após execução autorizada.
- A eficácia de L5 (egress) depende da topologia final (WSL2/Docker/WinNAT) — **hipótese a validar**, não fato.

## 7. Pendências / decisões necessárias

- **IR-1.** Porta canônica (PEND-3).
- **IR-2.** Mecanismo concreto de egress-block na topologia local — hipótese a validar.
- **IR-3.** Forma de captura de conexões que seja auditável e determinística.
