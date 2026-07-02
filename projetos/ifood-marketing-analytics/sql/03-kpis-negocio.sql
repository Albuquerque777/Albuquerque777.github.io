-- ============================================================
-- Projeto: iFood Marketing Analytics
-- Arquivo: 03-kpis-negocio.sql
-- Objetivo: Criar indicadores principais para análise executiva
-- Autor: Alexander Albuquerque
-- ============================================================

CREATE OR REPLACE VIEW vw_kpis_negocio_ifood AS
SELECT
    COUNT(*) AS total_clientes,

    ROUND(AVG(renda), 2) AS renda_media,

    ROUND(AVG(idade), 2) AS idade_media,

    SUM(gasto_total) AS receita_total_analisada,

    ROUND(AVG(gasto_total), 2) AS gasto_medio_por_cliente,

    ROUND(AVG(total_compras), 2) AS media_compras_por_cliente,

    SUM(total_compras) AS total_compras,

    SUM(compras_web) AS total_compras_web,

    SUM(compras_catalogo) AS total_compras_catalogo,

    SUM(compras_loja) AS total_compras_loja,

    SUM(resposta_campanha_final) AS total_clientes_que_responderam,

    ROUND(
        SUM(resposta_campanha_final) * 100.0 / COUNT(*),
        2
    ) AS taxa_resposta_campanha_percentual,

    SUM(reclamacao) AS total_reclamacoes,

    ROUND(
        SUM(reclamacao) * 100.0 / COUNT(*),
        2
    ) AS taxa_reclamacao_percentual

FROM vw_clientes_ifood_tratado;
