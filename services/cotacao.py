import requests
from models.moeda import Moeda

ENDPOINT = "https://economia.awesomeapi.com.br/json/last"

def buscar_cotacoes(moedas: list[Moeda]):
    codigos = ",".join([f"{m.codigo}-BRL" for m in moedas])
    url = f"{ENDPOINT}/{codigos}"

    try:
        resposta = requests.get(url, timeout=5)
        resposta.raise_for_status()
        dados = resposta.json()

        for moeda in moedas:
            chave = f"{moeda.codigo}BRL"
            if chave in dados:
                novo_valor = float(dados[chave]["bid"])
                moeda.atualizar(novo_valor)

    except requests.exceptions.Timeout:
        raise ConnectionError("Servidor demorou demais para responder.")
    except requests.exceptions.HTTPError as e:
        raise ConnectionError(f"Erro HTTP: {e}")
    except requests.exceptions.ConnectionError:
        raise ConnectionError("Sem conexão com a internet.")