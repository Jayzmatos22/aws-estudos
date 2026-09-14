

import json
import re
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass

"""'url montada ''"""
VIACEP_URL = "https://viacep.com.br/ws/{cep}/json/"
TIMEOUT_SEGUNDOS = 5

JSON_HEADERS = {"Content-Type": "application/json; charset=utf-8"}


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
    def from_viacep(cls, data: dict) -> "CEPData":
        return cls(
            cep=data.get("cep", ""),
            logradouro=data.get("logradouro", ""),
            complemento=data.get("complemento", ""),
            bairro=data.get("bairro", ""),
            localidade=data.get("localidade", ""),
            uf=data.get("uf", ""),
            ibge=data.get("ibge", ""),
            gia=data.get("gia", ""),
        )


def _resposta(status_code: int, corpo: dict) -> dict:
    """Monta a resposta no formato que o API Gateway (proxy integration) espera."""
    return {
        "statusCode": status_code,
        "headers": JSON_HEADERS,
        "body": json.dumps(corpo, ensure_ascii=False),
    }


def _erro(status_code: int, mensagem: str) -> dict:
    return _resposta(status_code, {"error": mensagem})


def _extrair_cep(event: dict) -> str | None:
    """
    Lê o CEP do evento.

    """
    query_params = event.get("queryStringParameters") or {}
    return query_params.get("cep")


def _consultar_viacep(cep: str) -> dict | None:
    """
    Consulta o ViaCEP. Retorna o dict da resposta, ou None se o serviço
    falhou (rede, timeout, HTTP != 200, JSON malformado).
    """
    url = VIACEP_URL.format(cep=cep)
    requisicao = urllib.request.Request(
        url,
        headers={"User-Agent": "lambda-consulta-cep"},
    )

    try:
        with urllib.request.urlopen(requisicao, timeout=TIMEOUT_SEGUNDOS) as resposta:
            if resposta.status != 200:
                print(f"ViaCEP retornou status inesperado: {resposta.status}")
                return None
            corpo = resposta.read().decode("utf-8")
        return json.loads(corpo)
    except urllib.error.HTTPError as exc:
        print(f"ViaCEP respondeu com erro HTTP {exc.code}")
        return None
    except urllib.error.URLError as exc:
        # Cobre timeout, DNS e falha de conexão.
        print(f"Falha ao alcançar o ViaCEP: {exc.reason}")
        return None
    except json.JSONDecodeError:
        print("ViaCEP retornou um corpo que não é JSON válido")
        return None


def handler_lambda(event, context):
    cep_bruto = _extrair_cep(event)

    if not cep_bruto:
        return _erro(400, "Parâmetro 'cep' é obrigatório.")

    cep_limpo = re.sub(r"\D", "", str(cep_bruto))

    if len(cep_limpo) != 8:
        return _erro(400, "CEP inválido. Deve conter 8 dígitos numéricos.")

    data = _consultar_viacep(cep_limpo)

    if data is None:
        return _erro(502, "Serviço de consulta de CEP indisponível no momento.")

    if data.get("erro"):
        return _erro(404, "CEP não encontrado.")

    cep_data = CEPData.from_viacep(data)
    return _resposta(200, asdict(cep_data))


