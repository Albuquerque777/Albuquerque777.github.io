-- ============================================================
-- Projeto: iFood Marketing Analytics
-- Arquivo: 04_segmentacao_clientes.sql
-- Objetivo: Segmentar clientes por renda, consumo e resposta à campanha
-- Autor: Alexander Albuquerque
-- ============================================================

CREATE OR REPLACE VIEW vw_segmentacao_clientes_ifood AS
SELECT
    id_cliente,
    idade,
    escolaridade,
    estado_civil,
    renda,
    total_dependentes,
    gasto_total,
    total_compras,
    compras_web,
    compras_catalogo,
    compras_loja,
    visitas_web_mes,
    resposta_campanha_final,
    reclamacao,

    CASE
        WHEN idade < 30 THEN 'Até 29 anos'
        WHEN idade BETWEEN 30 AND 39 THEN '30 a 39 anos'
        WHEN idade BETWEEN 40 AND 49 THEN '40 a 49 anos'
        WHEN idade BETWEEN 50 AND 59 THEN '50 a 59 anos'
        ELSE '60 anos ou mais'
    END AS faixa_etaria,

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
        WHEN total_compras >= 20 THEN 'Compra frequente'
        WHEN total_compras >= 10 THEN 'Compra moderada'
        ELSE 'Compra baixa'
    END AS perfil_compra,

    CASE
        WHEN resposta_campanha_final = 1 THEN 'Respondeu campanha'
        ELSE 'Não respondeu campanha'
    END AS status_resposta_campanha,

    CASE
        WHEN reclamacao = 1 THEN 'Cliente com reclamação'
        ELSE 'Cliente sem reclamação'
    END AS status_reclamacao

FROM vw_clientes_ifood_tratado;
