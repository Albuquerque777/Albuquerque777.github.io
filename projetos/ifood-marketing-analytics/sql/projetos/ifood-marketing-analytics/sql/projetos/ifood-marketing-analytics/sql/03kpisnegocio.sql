-- ============================================================
-- Projeto: iFood Marketing Analytics
-- Arquivo: 03kpisnegocio.sql
-- Objetivo: Criar indicadores principais para análise executiva
-- ============================================================

SELECT
    COUNT(*) AS total_clientes,
    ROUND(AVG(renda), 2) AS renda_media,
    ROUND(AVG(gasto_total), 2) AS gasto_medio_cliente,
    SUM(gasto_total) AS receita_total_analisada,
    ROUND(AVG(total_compras), 2) AS media_compras_cliente,
    SUM(resposta_campanha_final) AS total_respostas_campanha,
    ROUND(
        SUM(resposta_campanha_final) * 100.0 / COUNT(*), 
        2
    ) AS taxa_resposta_percentual
FROM vw_clientes_ifood_tratado;
