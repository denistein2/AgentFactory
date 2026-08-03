# PROTOCOLO EXCHANGE-01 — Transferência Drive ↔ Local

**Projeto:** Stein Agent Factory
**Natureza:** teste sintético de capacidade e integridade
**Estado inicial:** nenhuma integração presumida
**Dados permitidos:** exclusivamente sintéticos
**GitHub:** fora do primeiro teste
**Documento:** canônico
**Data de emissão:** 2026-08-02T14:44:01-0300

---

## 1. Princípios

```
GitHub = verdade versionada
Local  = verdade em execução
Drive  = custódia e intercâmbio
```

O Google Drive **não** é considerado zona limpa.

Todo arquivo recebido do Drive começa com o estado:

```
NÃO CONFIÁVEL — AGUARDANDO CLASSIFICAÇÃO
```

Nenhum arquivo do Exchange deve ser sobrescrito. Cada transferência gera um novo nome e um novo registro de evidência.

---

## 2. Estrutura do Drive

```
Stein Agent Factory/
└── Exchange/
    ├── 00_QUARANTINE/
    ├── 10_INBOX/
    ├── 20_OUTBOX/
    └── 90_ARCHIVE/
```

**Funções**

- `00_QUARANTINE`: arquivo recebido, ainda não classificado;
- `10_INBOX`: arquivo sintético ou autorizado para entrada;
- `20_OUTBOX`: resultado produzido localmente;
- `90_ARCHIVE`: evidências preservadas, sem sobrescrita.

---

## 3. Regra de nomes

Usar timestamp, missão e versão:

```
2026-08-02T144100-0300__EXCHANGE-01__entrada_teste__v001.md
```

Para resultados:

```
2026-08-02T144100-0300__EXCHANGE-01__saida_teste__v001.md
```

Nunca substituir `v001`. Uma alteração produz `v002`.

**Regra de custódia:** o nome canônico carrega o histórico. Toda verificação de integridade (§7, §10) opera sobre o **nome completo timestamped**, nunca sobre um nome reduzido. Provar a integridade de um arquivo e arquivar outro quebra a cadeia de custódia.

---

## 4. Etapa 0 — Matriz de capacidade real

Antes da transferência, testar e registrar se o executor consegue:

| Capacidade | Resultado |
|---|---|
| Listar pasta do Drive | PENDENTE |
| Ler metadados | PENDENTE |
| Baixar arquivo | PENDENTE |
| Enviar novo arquivo | PENDENTE |
| Criar pasta | PENDENTE |
| Mover arquivo | PENDENTE |
| Substituir arquivo existente | NÃO TESTAR |
| Excluir arquivo | NÃO TESTAR |

A arquitetura **não pode presumir escrita** no Drive.

Se houver somente leitura:

```
Drive → local: suportado
local → Drive: exige caminho alternativo
```

O caminho alternativo pode ser Google Drive Desktop, navegador ou upload manual controlado.

---

## 5. Arquivo sintético de entrada

Conteúdo:

```
STEIN-EXCHANGE-TEST
mission=EXCHANGE-01
version=001
classification=SYNTHETIC
pii=false
expected_destination=LOCAL_WORKSPACE
```

Salvar no Drive como:

```
10_INBOX/2026-08-02T144100-0300__EXCHANGE-01__entrada_teste__v001.md
```

---

## 6. Evidência na origem

Antes de baixar, registrar:

```
transfer_id
nome_do_arquivo
caminho_no_drive
tamanho_em_bytes
sha256_origem
sha256_provenance
data_hora
classificacao
executor
```

**Regra de proveniência do hash.** Quando o conector não fornecer o SHA-256 nativo do Drive, baixar uma cópia de referência e calcular localmente. Nesse caso:

```
sha256_origem      = HASH DA PRIMEIRA CÓPIA MATERIALIZADA
sha256_provenance  = FIRST_MATERIALIZED_COPY
```

Quando o conector fornecer o hash nativo:

```
sha256_provenance  = DRIVE_NATIVE
```

**Nunca** afirmar que um valor foi calculado pelo Drive quando ele veio da primeira cópia materializada. O campo `sha256_provenance` é obrigatório no manifesto e preserva essa distinção para auditoria futura.

---

## 7. Verificação local

O caminho verificado é o **nome canônico completo** (§3), não um nome reduzido.

**PowerShell**

```powershell
$file = "C:\Stein\AgentFactory\Exchange\10_INBOX\2026-08-02T144100-0300__EXCHANGE-01__entrada_teste__v001.md"

(Get-Item $file).Length
(Get-FileHash $file -Algorithm SHA256).Hash.ToLower()
```

**WSL/Linux**

```bash
FILE="2026-08-02T144100-0300__EXCHANGE-01__entrada_teste__v001.md"
stat -c %s "$FILE"
sha256sum "$FILE"
```

Registrar:

```
tamanho_origem = tamanho_local
sha256_origem  = sha256_local
```

Resultado permitido:

```
TRANSFERÊNCIA ÍNTEGRA
```

Em caso de diferença:

```
STOP — DIVERGÊNCIA DE CUSTÓDIA
```

O arquivo divergente **não** entra no workspace operacional.

---

## 8. Classificação antes do uso

Executar a sequência:

```
detectar → classificar → decidir → registrar → liberar ou bloquear
```

Classificações mínimas:

```
SYNTHETIC
PUBLIC
INTERNAL
CONFIDENTIAL
PII-SUSPECTED
REAL-CUSTOMER-DATA
UNKNOWN
```

Somente `SYNTHETIC`, `PUBLIC` ou material explicitamente autorizado pode sair da quarentena neste teste.

> **PEND-EXCHANGE-1 (bloqueante para transferência não-sintética).**
> Neste teste tudo é `SYNTHETIC`, então não há tensão. Mas na primeira transferência de material real — especialmente material recebido pelo celular — esta Etapa 8 passa a ser o portão mais importante, acima da verificação de hash (§7). O hash prova que os bytes não mudaram; **não** prova que os bytes eram seguros. Antes de qualquer transferência não-sintética, definir quem/o quê executa a detecção de PII nesta etapa. Mesmo portão fail-closed Agentes→Conteúdo, aplicado à perna de entrada. Resolução pendente.

---

## 9. Produção da saída local

Criar um **novo** arquivo, sem alterar a entrada:

```
2026-08-02T144100-0300__EXCHANGE-01__saida_teste__v001.md
```

Registrar antes do upload:

```
tamanho_saida_local
sha256_saida_local
caminho_local
data_hora
```

---

## 10. Upload para o Drive

Enviar para:

```
20_OUTBOX/
```

**Não** substituir arquivo existente.

Após o upload:

1. confirmar nome e tamanho no Drive;
2. baixar novamente o arquivo para um caminho **diferente**;
3. recalcular tamanho e SHA-256;
4. comparar com a saída local original.

Exemplo de caminho de reconferência:

```
workspace/recheck/2026-08-02T144100-0300__EXCHANGE-01__saida_teste__v001__downloaded.md
```

A prova final deve ser:

```
sha256_saida_local  = sha256_rebaixado_do_drive
tamanho_saida_local = tamanho_rebaixado_do_drive
```

---

## 11. Manifesto da transferência

Criar:

```
EXCHANGE_MANIFEST_2026-08-02T144100-0300.json
```

Ver esqueleto canônico em `EXCHANGE_MANIFEST_SKELETON.json`. Campos obrigatórios incluem `sha256_provenance` em `source`.

---

## 12. Critérios de sucesso

```
arquivo sintético utilizado
nenhuma PII encontrada
nenhuma sobrescrita realizada
capacidade de leitura confirmada ou negada
capacidade de escrita confirmada ou negada
hash Drive → local conferido
hash local → Drive → local conferido, se escrita disponível
manifesto completo (incluindo sha256_provenance)
```

Resultado:

```
PASS — CAPACIDADE E INTEGRIDADE CONFIRMADAS
```

ou:

```
EXPECTED_LIMITATION — DRIVE SOMENTE LEITURA
```

ou:

```
STOP — DIVERGÊNCIA DE CUSTÓDIA
```

---

## 13. O que este teste NÃO prova

```
integridade de transporte ≠ ausência de PII
integridade de transporte ≠ segurança do conteúdo
integridade de transporte ≠ versionamento Git
Drive disponível         ≠ sincronização automática
upload concluído         ≠ bytes reconferidos
```

O teste não envolve GitHub, Docker, banco, Supabase, HOMOLOG, produção nem dados reais.

---

## 14. Sequência de integração (após este teste)

Primeiro provar Drive ↔ local. Só depois adicionar a terceira perna:

```
Drive → local → GitHub
GitHub → local → Drive
```

Cada transição com manifesto, tamanho, SHA-256 e STOP em caso de divergência. Não abstrair a integração dos três ambientes antes de provar as duas primeiras pernas concretamente (disciplina rule-of-three).

---

## Changelog

- **v001 (2026-08-02):** emissão canônica. Correções aplicadas sobre o rascunho:
  - §7 alinhado ao nome canônico completo timestamped (era `entrada_teste.md` reduzido).
  - §6 e §11: adicionado campo obrigatório `sha256_provenance` (`DRIVE_NATIVE` | `FIRST_MATERIALIZED_COPY`).
  - §8: marcado **PEND-EXCHANGE-1** para detecção de PII em transferência não-sintética.
