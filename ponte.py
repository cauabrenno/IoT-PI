import requests
import time

# --- CONFIGURAÇÕES ---
API_KEY = "AG1LTDH0X6S5ZM0M" 
# -------------------

THINGSPEAK_URL = "https://api.thingspeak.com/update"

print("--- Ponte Tinkercad para ThingSpeak ---")
print("Iniciado. Copie uma linha de dados do Monitor Serial do Tinkercad e cole aqui.")

while True:
    try:
        linha_de_dados = input("\nCole os dados e pressione Enter (ou CTRL+C para sair): ")

        # Exemplo de dado esperado: "umidade:543,vibracao:0,botao:1"

        partes = linha_de_dados.split(',')

        valor_umidade = partes[0].split(':')[1]
        valor_vibracao = partes[1].split(':')[1]
        valor_botao = partes[2].split(':')[1]  

        print(f"Dados processados -> Umidade: {valor_umidade}, Vibração: {valor_vibracao}, Botão: {valor_botao}")

        # Monta o payload com os três campos
        payload = {
            'api_key': API_KEY,
            'field1': valor_umidade,
            'field2': valor_vibracao,
            'field3': valor_botao # NOVO: Adiciona o field3
        }

        response = requests.get(THINGSPEAK_URL, params=payload)

        if response.status_code == 200:
            print(">>> Sucesso! Dados enviados para o ThingSpeak.")
        else:
            print(f"*** Erro! Falha ao enviar dados. Código: {response.status_code}")
            print(f"Resposta do servidor: {response.text}")

    except Exception as e:
        print(f"!!! Ocorreu um erro ao processar os dados: {e}")
        print("Verifique se você colou a linha no formato correto (ex: 'umidade:543,vibracao:0,botao:1')")