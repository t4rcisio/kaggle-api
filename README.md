# Backend Challenge 🏅 2022 - Covid Daily Cases


[Deploy da API](https://kaggleapi.herokuapp.com) <br/>
[Repositório API principal](https://github.com/t4rcisio/Covid-Daily-Cases)

```

Esse repositório faz parte do Challenge Covid Daily Cases.

O módulo consiste em uma API desenvolvida em Python, que ultilizando-se 
da API do Kaggle, baixa um arquivo CSV de um repositório de 
reports de casos de Covid no mundo.
Esses dados então são usados para alimentar um banco de dados hospedado
na plataforma mongoDB.
```

## Rotas
```
A API possui duas rotas, a "/" e "/kaggle"


url: /    [GET]
code: 200
Retorno: "Backend Challenge 2021 🏅 - Covid Daily Cases"

url: /kaggle    [GET]
code: 200
Retorno[0]: {Status: "Updated"} -> Caso o banco esteja atualizado
Retorno[1]: {Status: "Updating"} -> Caso o banco esteja em processo de atualização


```


## Especificações

```
O script da API está configurada para atualizar o banco de dados a 
cada 24h.

A API principal do "Challenge Covid Daily Cases" sempre que é acessada, faz uma requisição
para o endereço /kaggle, de forma que o script em python verifica se é preciso atualizar 
o banco.
Em caso afirmativo, o script faz uma requisição a API da Kaggle, recebendo um novo arquivo CSV, e postriormente faz toda a substituição da base de dados.

```

## O ARQUIVO .ENV ESTÁ PREENCHIDO, MAS AS CREDENCIAIS SÃO TEMPORÁRIAS



