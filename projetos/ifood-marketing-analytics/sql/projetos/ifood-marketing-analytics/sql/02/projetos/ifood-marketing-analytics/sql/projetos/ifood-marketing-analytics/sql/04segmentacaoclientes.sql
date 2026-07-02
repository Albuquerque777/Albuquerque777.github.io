-- ============================================================
-- Projeto: iFood Marketing Analytics
-- Arquivo: 04segmentacaoclientes.sql
-- Objetivo: Segmentar clientes por renda e comportamento de consumo
-- ============================================================

SELECT
    id_cliente,
    idade,
    escolaridade,
    estado_civil,
    renda,
    gasto_total,
    total_compras,
    resposta_campanha_final,

    CASE
        WHEN renda >= 100000 THEN 'Alta renda'
        WHEN renda >= 50000 THEN 'Média renda'
        ELSE 'Baixa renda'
    END AS faixa_renda,

    CASE
        WHEN gasto_total >= 1500 THEN 'Cliente alto valor'
        WHEN gasto_total >= 500 THEN 'Cliente médio valor'
        ELSE 'Cliente baixo valor'
    END AS segmento_consumo,

    CASE
        WHEN resposta_campanha_final = 1 THEN 'Respondeu campanha'
        ELSE 'Não respondeu campanha'
    END AS status_resposta

FROM vw_clientes_ifood_tratado;
