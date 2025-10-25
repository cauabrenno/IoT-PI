from flask import Flask, request, jsonify, render_template
import psycopg2
import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env (se ele existir)
# O Render não usa .env, ele injeta as variáveis direto
load_dotenv() 

app = Flask(__name__)   

def get_db_connection():
    # Esta é a variável de ambiente que o Render cria
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    try:
        if DATABASE_URL:
            # 1. Se estiver no Render, usa a URL de conexão
            conn = psycopg2.connect(DATABASE_URL)
        else:
            # 2. Se estiver rodando local (teste), usa as variáveis locais
            conn = psycopg2.connect(
                dbname="sensor_deslizamento",
                user="postgres",
                password="caua", # Sua senha local que você definiu
                host="localhost"
            )
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao PostgreSQL: {e}")
        return None

def init_db():
    conn = get_db_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS leituras (
                    id SERIAL PRIMARY KEY,
                    umidade INTEGER,
                    vibracao INTEGER,
                    botao INTEGER,
                    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                )
            ''')
        conn.commit()
        conn.close()
        # Não imprimimos a mensagem de sucesso se estivermos no Render (para não poluir o log)
        if not os.getenv("DATABASE_URL"):
            print("Tabela 'leituras' verificada/criada com sucesso (Local).")

@app.route('/dados', methods=['POST'])
def receber_dados():
    dados = request.json
    umidade = dados.get('field1')
    vibracao = dados.get('field2')
    botao = dados.get('field3')

    conn = get_db_connection()
    if not conn:
        return jsonify({"status": "erro", "mensagem": "Falha na conexão com o banco"}), 500

    sql = "INSERT INTO leituras (umidade, vibracao, botao) VALUES (%s, %s, %s)"
    
    with conn.cursor() as cur:
        cur.execute(sql, (umidade, vibracao, botao))
    conn.commit()
    conn.close()

    print(f"Dados salvos no PostgreSQL: Umidade={umidade}, Vibração={vibracao}, Botão={botao}")
    return jsonify({"status": "sucesso"}), 200

@app.route('/api/ultimos_dados')
def fornecer_ultimos_dados():
    conn = get_db_connection()
    if not conn:
        return jsonify({})

    with conn.cursor() as cur:
        cur.execute("SELECT umidade, vibracao, botao, timestamp FROM leituras ORDER BY id DESC LIMIT 1")
        leitura = cur.fetchone()
    conn.close()
    
    if leitura:
        dados = {
            "umidade": leitura[0],
            "vibracao": leitura[1],
            "botao": leitura[2],
            "timestamp": leitura[3].isoformat()
        }
        return jsonify(dados)
    else:
        return jsonify({})

@app.route('/api/historico')
def fornecer_historico():
    conn = get_db_connection()
    if not conn:
        return jsonify([]) 

    with conn.cursor() as cur:
        cur.execute("SELECT umidade, vibracao, botao, timestamp FROM leituras ORDER BY id DESC LIMIT 10")
        resultados = cur.fetchall() 
    conn.close()
    
    historico = []
    for leitura in resultados:
        historico.append({
            "umidade": leitura[0],
            "vibracao": leitura[1],
            "botao": leitura[2],
            "timestamp": leitura[3].isoformat()
        })
    
    return jsonify(historico) 

@app.route('/')
def dashboard():
    return render_template('index.html')

if __name__ == '__main__':
    # Esta parte só roda quando você executa 'python servidor.py'
    # O Render ignora esta parte e usa o comando Gunicorn
    print("Iniciando servidor localmente em http://0.0.0.0:5000")
    init_db()
    app.run(host='0.0.0.0', debug=True)