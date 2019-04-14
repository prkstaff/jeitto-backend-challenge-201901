#Desafio Backend Python

Este desafio tem como intuito testar as habilidades de desenvolvimento e arquitetura de software do candidato à uma vaga no time de engenharia da Jeitto.

## Problema: Recarga de telefônica
Implementar uma API para permitir a compra de créditos telefônicos onde o usuário, após informar o número à ser recarregado a compra será efetuada.


### Pesquisa por produtos
O primeiro recurso que deve ser implementado é o que irá permitir a manutenção (CRUD) e busca por produtos compativeis para serem utilizado na recarga. O mesmo deverá, em seu metodo GET, também receber um parâmetro "company_id" e retornar um json com os produtos daquela compania informada. Como no exemplo abaixo:

Exemplo 1.1: GET /CompanyProducts?company_id=claro_11

```json
{
"company_id": "claro_11",
  "products":[
    {"id": "claro_10", "value": 10.0},
    {"id": "claro_20", "value": 20.0}
  ]
}
```

Exemplo 1.2: GET /CompanyProducts
```json
[
    {
        "company_id": "claro_11",
        "products":[
            {"id": "claro_10", "value": 10.0},
            {"id": "claro_20", "value": 20.0}
        ]
    },
    {
        "company_id": "tim_11",
        "products":[
            {"id": "tim_10", "value": 10.0},
            {"id": "tim_20", "value": 20.0}
        ]
    }
]
```

Obs.: Os demais metodos, deverão seguir a mesma estrutura do payload indicado no exemplo 1.1.


### Efetivação da recarga
O segundo recurso deverá efetivar a recarga telefônica propriamente dita. Permitirá um POST com os dados necessários para a recarga, bem como GETs para busca de dados como nos exemplos abaixo:

Exemplo 2.1: POST /PhoneRecharges
```json
{
    "company_id": "claro_11",
    "product_id": "claro_10",
    "phone_number": "5511999999999",
    "value": 10.00
}
```

Exemplo 2.2: GET /PhoneRecharges?id=id_da_recarga
```json
{
    "id": "id_da_recarga",
    "created_at": "2019-02-01T13:00:00.000Z",
    "company_id": "claro_11",
    "product_id": "claro_10",
    "phone_number": "5511999999999",
    "value": 10.00
}
```

Exemplo 2.3: GET /PhoneRecharges?phone_number=5511999999999
```json
[
    {
        "id": "id_da_recarga",
        "created_at": "2019-02-01T13:00:00.000Z",
        "company_id": "claro_11",
        "product_id": "claro_10",
        "phone_number": "5511999999999",
        "value": 10.00
    },
    {
        "id": "id_da_recarga",
        "created_at": "2019-03-14T13:00:00.000Z",
        "company_id": "claro_11",
        "product_id": "claro_10",
        "phone_number": "5511999999999",
        "value": 10.00
    }
]
```

Obs.: Os demais metodos não deverão ser permitidos para este recurso.


##Como enviar sua sua solução
Para participar você deverá fazer um fork deste repositório e submeter as alterações apenas para a sua cópia. Não faça um PR para este repositório, apenas envie um link para o avaliador que está em contato com você.

O que **queremos** ver
- Python 3.
- Testes bem escritos e com uma boa cobertura.
- Legibilidade e manutenabilidade de código.
- Código em inglês.
- Segurança de dados e acesso.
- Tratamento de erros.

O que **gostariamos** de ver
- Documentação fácil e bem escrita.
- Utilização de docker.
- Cache de dados.
- Deploy automatizado.
- Amigavel com Google Cloud.
- Segurança de dados.


##Leituras recomendadas
- [Small acts manifesto](http://smallactsmanifesto.org/) sobre comportamento humano e social.
- [The Twelve-Factor App](https://12factor.net/pt_br/) é manifesto sobre o desenvolvimento e boas práticas para facilitar a manutenção de softwares.
- [Design Patterns for Humans](https://github.com/kamranahmedse/design-patterns-for-humans) texto excelente explicando e mostrando exemplos de uso de padrões de projetos.
- [Python Patterns](https://github.com/faif/python-patterns) é um repostiório com exemplos de padrões de projetos implementados em python.
- [Continuous integration vs. continuous delivery vs. continuous deployment](https://www.atlassian.com/continuous-delivery/principles/continuous-integration-vs-delivery-vs-deployment)
- [OpenAPI Specification](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md#operation-object)