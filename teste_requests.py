import requests

resposta = requests.get("https://viacep.com.br/ws/57022120/json/")
dados = resposta.json()

print(f"CEP: {dados['cep']}")
print(f"Rua: {dados['logradouro']}")
print(f"Bairro: {dados['bairro']}")
print(f"Cidade: {dados['localidade']} - {dados['uf']}")
print(f"DDD: {dados['ddd']}")