from flask import Flask, request, jsonify, render_template
import psycopg2
import os
from dotenv import load_dotenv
from flask_cors import CORS 

load_dotenv() 

app = Flask(__name__)   
CORS(app) # <--- 2. Adicione isso (Libera geral)

def get_db_connection():
    DATABASE_URL = os.getenv("DATABASE_URL")
    try:
        if DATABASE_URL:
            conn = psycopg2.connect(DATABASE_URL)
        else:
            conn = psycopg2.connect(
                dbname="sensor_deslizamento",
                user="postgres",
                password="caua", 
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
            # MUDANÇA: Adicionamos 'sensor_id' na tabela
            cur.execute('''
                CREATE TABLE IF NOT EXISTS leituras (
                    id SERIAL PRIMARY KEY,
                    sensor_id INTEGER, 
                    umidade INTEGER,
                    vibracao INTEGER,
                    botao INTEGER,
                    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                )
            ''')
        conn.commit()
        conn.close()
        print("Tabela 'leituras' (nova versão) verificada/criada.")

# Rota para receber dados (Atualizada para sensor_id)
@app.route('/dados', methods=['POST'])
def receber_dados():
    dados = request.json
    sensor_id = dados.get('sensor_id') # NOVO
    umidade = dados.get('field1')
    vibracao = dados.get('field2')
    botao = dados.get('field3')

    conn = get_db_connection()
    if not conn:
        return jsonify({"status": "erro", "mensagem": "Falha BD"}), 500

    sql = "INSERT INTO leituras (sensor_id, umidade, vibracao, botao) VALUES (%s, %s, %s, %s)"
    
    with conn.cursor() as cur:
        cur.execute(sql, (sensor_id, umidade, vibracao, botao))
    conn.commit()
    conn.close()

    print(f"Salvo - Sensor {sensor_id}: Umid={umidade}, Vib={vibracao}, Btn={botao}")
    return jsonify({"status": "sucesso"}), 200

# --- NOVA ROTA PODEROSA: RESUMO DOS SENSORES ---
# Retorna o ÚLTIMO dado de CADA sensor que existe no banco.
# Ideal para criar os cards do dashboard automaticamente.
@app.route('/api/todos_sensores_ultimos_dados')
def resumo_sensores():
    conn = get_db_connection()
    if not conn: return jsonify([])

    with conn.cursor() as cur:
        # Esta query mágica pega a última leitura de cada sensor_id distinto
        query = """
            SELECT DISTINCT ON (sensor_id) 
            sensor_id, umidade, vibracao, botao, timestamp 
            FROM leituras 
            ORDER BY sensor_id, timestamp DESC
        """
        cur.execute(query)
        resultados = cur.fetchall()
    conn.close()
    
    lista_sensores = []
    for r in resultados:
        lista_sensores.append({
            "sensor_id": r[0],
            "umidade": r[1],
            "vibracao": r[2],
            "botao": r[3],
            "timestamp": r[4].isoformat()
        })
    return jsonify(lista_sensores)

# Rota de histórico (Pode filtrar por ID se quiser no futuro)
# --- ROTA DE HISTÓRICO INTELIGENTE ---
# Agora aceita um ID opcional. Ex: /api/historico/1 (Só do sensor 1)
@app.route('/api/historico')
@app.route('/api/historico/<int:sensor_id>') 
def fornecer_historico(sensor_id=None):
    conn = get_db_connection()
    if not conn: return jsonify([]) 

    with conn.cursor() as cur:
        if sensor_id is not None:
            # SE TIVER ID: Pega os últimos 20 APENAS daquele sensor
            cur.execute("""
                SELECT sensor_id, umidade, vibracao, botao, timestamp 
                FROM leituras 
                WHERE sensor_id = %s 
                ORDER BY id DESC LIMIT 100
            """, (sensor_id,))
        else:
            # SE NÃO TIVER ID: Pega os últimos 20 gerais (comportamento antigo)
            cur.execute("""
                SELECT sensor_id, umidade, vibracao, botao, timestamp 
                FROM leituras 
                ORDER BY id DESC LIMIT 20
            """)
            
        resultados = cur.fetchall() 
    conn.close()
    
    historico = []
    for r in resultados:
        historico.append({
            "sensor_id": r[0],
            "umidade": r[1],
            "vibracao": r[2],
            "botao": r[3],
            "timestamp": r[4].isoformat()
        })
    return jsonify(historico)

@app.route('/')
def dashboard():
    return render_template('index.html')

if __name__ == '__main__':
    # Executa init_db() para garantir que a tabela nova seja criada
    with app.app_context():
        init_db()
    app.run(host='0.0.0.0', debug=True)