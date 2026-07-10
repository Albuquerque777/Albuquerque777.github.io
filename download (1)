# Medidas DAX - Referência

> Este arquivo documenta as principais medidas utilizadas no projeto. Ajuste os nomes das tabelas e colunas conforme o PBIX final.

```DAX
Compras Total =
CALCULATE(
    COUNTROWS('CRUZAMENTO_ID_OFICIAL'),
    'CRUZAMENTO_ID_OFICIAL'[FLAG_EXISTE_ARIBA] = TRUE()
)
```

```DAX
Valor Compras Total =
CALCULATE(
    COALESCE(SUM('CRUZAMENTO_ID_OFICIAL'[VALOR_PC_ARIBA]), 0),
    'CRUZAMENTO_ID_OFICIAL'[FLAG_EXISTE_ARIBA] = TRUE()
)
```

```DAX
Status Macro Compras =
VAR StatusLimpo =
    UPPER(TRIM(COALESCE('CRUZAMENTO_ID_OFICIAL'[STATUS_CONTRATACAO_ARIBA], "")))
RETURN
SWITCH(
    TRUE(),
    StatusLimpo IN {"GANHO", "GANHA", "CONCLUÍDO", "CONCLUIDO", "CONCLUÍDA", "CONCLUIDA"}, "Ganho",
    StatusLimpo IN {"EM ANDAMENTO", "ANDAMENTO", "EM TRATAMENTO"}, "Em Andamento",
    StatusLimpo IN {"CANCELADO", "CANCELADA", "PERDIDO", "PERDIDA", "DECLINADO", "DECLINADA", "DECLINOU", "RECUSADO", "RECUSADA"}, "Sem Contratação",
    "Outros"
)
```

```DAX
Qtd Ganhos =
CALCULATE(
    [Compras Total],
    'CRUZAMENTO_ID_OFICIAL'[STATUS_MACRO_COMPRAS] = "Ganho"
)
```

```DAX
Qtd S/ Contrat. =
CALCULATE(
    [Compras Total],
    'CRUZAMENTO_ID_OFICIAL'[STATUS_MACRO_COMPRAS] = "Sem Contratação"
)
```

```DAX
Taxa Sucesso =
DIVIDE(
    [Qtd Ganhos],
    [Qtd Ganhos] + [Qtd S/ Contrat.],
    0
)
```
