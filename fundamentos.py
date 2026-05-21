nome = "Gustavo Souza"
idade = 43
altura = 1.65
estudante = False
hora = 19

cidades = ["Marechal Deodoro", "Maceió", "Arapiraca", "Palmeira dos índios"]

def calcular_imc(peso, altura):
    imc = peso / altura ** 2
    
    if imc < 18.5:
        classificacao = "Abaixo do peso"
    elif imc < 25:
        classificacao = "Peso normal"
    elif imc < 30:
        classificacao = "Sobrepeso"
    else:
        classificacao = "Obesidade"

    return round(imc, 2), classificacao
    

def salvar_numero(nome, idade, imc):
    with open("resumo.txt", "w", encoding="utf-8") as arquivo:
        arquivo.write(f'Meu nome é {nome}\n')
        arquivo.write(f'Tenho {idade} anos\n')
        arquivo.write(f'Meu IMC é {imc}\n')


def ler_resumo():

        try:
            with open("resumo.txt", "r", encoding="utf-8") as arquivo:
                conteudo = arquivo.read()
                print(conteudo)
        except FileNotFoundError:
            print("Arquivo não encontrado.")

print(f'Meu nome é {nome}, tenho {idade} anos, minha altura é {altura} e sou estudante? {"Sim" if estudante else "Não"}')

if idade >= 18:
    print("Maior de idade")
elif idade >= 13:
    print("Adolescente")
else:
    print("Criança")


if hora < 12:
    print ("Bom dia!")
elif hora >= 12 and hora < 18:
    print ("Boa tarde!")
else:
    print ("Boa noite!")

for i, cidade in enumerate(cidades):
    print(f"Cidade {i+1}: {cidade}")

print(calcular_imc(65, 1.65))

salvar_numero("Gustavo Souza", 43, calcular_imc(65, 1.65))

ler_resumo()