import requests

def consultar_cep(cep):
    cep = cep.replace("-", "").replace(" ", "")
    
    if len(cep) != 8:
        return None, "CEP inválido — deve ter 8 dígitos."
    
    try:
        resposta = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
        dados = resposta.json()
        
        if "erro" in dados:
            return None, "CEP não encontrado."
        
        return dados, None
    
    except Exception:
        return None, "Erro de conexão. Verifique sua internet."
    

def exibir_endereco(dados):
    print("\n--- Endereço encontrado ---")
    print(f"CEP:      {dados['cep']}")
    print(f"Rua:      {dados['logradouro']}")
    print(f"Bairro:   {dados['bairro']}")
    print(f"Cidade:   {dados['localidade']} - {dados['uf']}")
    print(f"Região:   {dados['regiao']}")
    print(f"DDD:      {dados['ddd']}")
    print("---------------------------\n")


def salvar_historico(dados):
    with open("historico.txt", "a", encoding="utf-8") as arquivo:
        arquivo.write(f"{dados['cep']} - {dados['logradouro']}, {dados['bairro']}, {dados['localidade']} - {dados['uf']}\n")


def main():
    print("=== Consultador de CEP ===")
    print("Digite 'sair' para encerrar.\n")
    
    while True:
        cep = input("Digite o CEP: ")
        
        if cep.lower() == "sair":
            print("Encerrando. Até mais!")
            break
        
        dados, erro = consultar_cep(cep)
        
        if erro:
            print(f"\n⚠ {erro}\n")
        else:
            exibir_endereco(dados)
            salvar_historico(dados)
            print("Consulta salva no histórico.\n")

# main()

if __name__ == "__main__":
    main()