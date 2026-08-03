# SECURITY

## Invariantes de segurança da Stein Agent Factory

1. **Nunca versionar** dumps reais, dados reais, PII ou dados de clientes.
2. **Nunca centralizar segredos** neste repositório. Cada fábrica (Produto,
   Agentes, Conteúdo) retém as próprias credenciais, para que uma fuga de sandbox
   não alcance produção.
3. **PII: quarentena, não remoção.** Procedimento: detectar → classificar → STOP
   → registrar → decidir explicitamente. Nunca "remover PII" silenciosamente.
4. **Gate fail-closed:** na dúvida, para. Decisão humana antes de qualquer
   transição de fase ou contato com dado real.
5. **Handoff Agentes→Conteúdo** exige gate PII fail-closed antes de qualquer
   conteúdo de sessão não-sanitizado chegar ao pipeline público.

## Se um segredo/dado real for encontrado (STOP-03)

Parar imediatamente. Mover para quarentena (`archive/quarantine-index/` só o
registro, nunca o conteúdo). Registrar sem expor. Não commitar.

## Reporte

Questões de segurança são tratadas diretamente por Denis Stein (responsável).
