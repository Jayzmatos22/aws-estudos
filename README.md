# 🧪 estudos-aws

Registro dos meus estudos práticos de AWS — preparação para entrevista de estágio (Itaú), com foco em Lambda, S3, Glue e Python.

<p align="left">
  <img src="https://img.shields.io/badge/AWS-Lambda-FF9900?style=for-the-badge&logo=awslambda&logoColor=white" />
  <img src="https://img.shields.io/badge/AWS-S3-569A31?style=for-the-badge&logo=amazons3&logoColor=white" />
  <img src="https://img.shields.io/badge/AWS-Glue-3B48CC?style=for-the-badge&logo=amazonaws&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white" />
</p>

<p align="left">
  <img src="https://img.shields.io/badge/status-em%20andamento-yellow?style=flat-square" />
  <img src="https://img.shields.io/badge/objetivo-est%C3%A1gio%20Ita%C3%BA-orange?style=flat-square" />
  <img src="https://img.shields.io/github/last-commit/Jayzmatos22/estudos-aws?style=flat-square" />
</p>

## 📌 Sobre

Este repositório é meu diário de bordo estudando AWS para uma semana de preparação intensiva antes de uma entrevista de estágio. Cada pasta é um experimento isolado, com o mínimo de código necessário para entender o serviço na prática — sem enrolação, sem tutorial copiado sem entender.

## 🗂️ Estrutura

```
estudos-aws/
├── lambda-aws/
│   └── lambda_function.py    # Function URL + consumo da API do BCB
└── README.md
```

## ⚡ Lambda + API do BCB

Função Python rodando em **AWS Lambda**, exposta via **Function URL**, que consome a API pública do Banco Central (série de câmbio USD/BRL) e retorna o resultado em JSON.

```python
import json
import urllib.request

def lambda_handler(event, context):
    url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados/ultimos/5?formato=json"
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read())
    return {
        'statusCode': 200,
        'body': json.dumps(data)
    }
```

**Conceitos praticados:**
- Serverless — código sob demanda, sem servidor gerenciado
- Function URL — endpoint HTTP público direto para a função
- `lambda_handler(event, context)` — assinatura padrão de invocação
- Consumo de API externa com `urllib.request` (sem dependências externas)

## 🎯 Próximos passos

- [ ] Pipeline S3 → Lambda → S3 (trigger por evento)
- [ ] AWS Glue: crawler + Data Catalog
- [ ] Angular: fundamentos e comparação com React

---

<p align="left">
  <img src="https://img.shields.io/badge/feito%20por-Jailton%20Santos%20de%20Matos-blueviolet?style=flat-square" />
</p>