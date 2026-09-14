import json
import requests
from dataclasses import dataclass, asdict
import re

@dataclass
class CEPData:
    cep: str
    logradouro: str
    complemento: str
    bairro: str
    localidade: str
    uf: str
    ibge: str
    gia: str

    @classmethod
    def from_viacep(cls, data: dict):
        return cls(
            cep=data.get('cep', ''),
            logradouro=data.get('logradouro', ''),
            complemento=data.get('complemento', ''),
            bairro=data.get('bairro', ''),
            localidade=data.get('localidade', ''),
            uf=data.get('uf', ''),
            ibge=data.get('ibge', ''),
            gia=data.get('gia', '')
        )

def handler_lambda(event, context):


    query_params = event.get('queryStringParams') or {}
    cep_sujo = query_params.get('cep', "04.742-000")
    cep_limpo = re.sub(r'\D', '', str(cep_sujo))

    if len(cep_limpo) != 8:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'CEP inválido. Deve conter 8 dígitos numéricos.'})
        }
    
    #  Monta a URL com o CEP sanitizado
    url = f"https://viacep.com.br/ws/{cep_limpo}/json/"
    response = requests.get(url)
    response.encoding = 'utf-8'
    data = response.json()

    if data.get('erro') == True or data.get('erro') is True:
        return {
            'statusCode': 404,
            'headers': {'Content-Type': 'application/json; charset=utf-8'},
            'body': json.dumps({'error': 'CEP não encontrado.'})
        }

    cep_data = CEPData.from_viacep(data)

    return{
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json; charset=utf-8'},
        'body': json.dumps(asdict(cep_data), ensure_ascii=False, indent=4)
    }



evento_com_cep = {
    "queryStringParams": {
        "cep": "04.742-000"
    }
}
res1 = handler_lambda(evento_com_cep, None)
print("=== Resposta Sucesso ===")
print(res1['body'])

# Teste 2: Enviando CEP incompleto (?cep=123)
evento_invalido = {
    "queryStringParams": {
        "cep": "123"
    }
}
res2 = handler_lambda(evento_invalido, None)
print("\n=== Resposta Erro 400 ===")
print(res2['body'])