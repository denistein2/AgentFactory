-- seed_7730.sql — dados SINTÉTICOS para testar a Opção B sem PII real.
-- Reproduz os casos que a matriz de regressão exige. Zero dado da Dolce.
-- 🚩 UUIDs fixos e fabricados. Ajustar aos NOT NULL/FK reais quando o schema-only restaurar.
-- Casos: saldo suficiente / exato / insuficiente / ausente / negativo cravado.
-- (esqueleto — o agente completa contra o schema real restaurado no clone)
BEGIN;
-- tenant técnico sintético
-- INSERT INTO tenants (id, name) VALUES ('00000000-0000-0000-0000-000000000001','TENANT_TESTE');
-- stock_types PROD/BALCAO, product_variants, stock_entries para gerar saldos-alvo...
-- (deixado como TODO estruturado: o agente preenche lendo os NOT NULL do schema restaurado)
ROLLBACK; -- placeholder: NÃO aplica nada até o agente completar no clone
