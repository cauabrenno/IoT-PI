import requests
import json 

# --- CONFIGURAÇÕES ---
# URL do nosso servidor Flask local
SERVER_URL = "http://127.0.0.1:5000/dados"
# -------------------

print("--- Ponte Tinkercad para Servidor Local ---")
print("Iniciado. Copie uma linha de dados do Monitor Serial e cole aqui.")

while True:
    try:
        linha_de_dados = input("\nCole os dados e pressione Enter (ou CTRL+C para sair): ")

        partes = linha_de_dados.split(',')
        
        valor_umidade = int(partes[0].split(':')[1])
        valor_vibracao = int(partes[1].split(':')[1])
        valor_botao = int(partes[2].split(':')[1])

        print(f"Dados processados -> Umidade: {valor_umidade}, Vibração: {valor_vibracao}, Botão: {valor_botao}")

        # Monta o payload como um dicionário Python
        payload = {
            'field1': valor_umidade,
            'field2': valor_vibracao,
            'field3': valor_botao
        }

        # Envia os dados usando uma requisição POST com JSON
        response = requests.post(SERVER_URL, json=payload)

        if response.status_code == 200:
            print(">>> Sucesso! Dados enviados para o servidor local.")
        else:
            print(f"*** Erro! Falha ao enviar dados. Código: {response.status_code}")
            print(f"Resposta do servidor: {response.text}")

    except Exception as e:
        print(f"!!! Ocorreu um erro ao processar os dados: {e}")