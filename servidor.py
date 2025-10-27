from flask import Flask, request, jsonify, render_template
import psycopg2
import os

DB_NAME = "sensor_deslizamento"
DB_USER = "postgres"
DB_HOST = "localhost"
DB_PASS = "caua" 

app = Flask(__name__)   

def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST
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
        print("Tabela 'leituras' verificada/criada com sucesso no PostgreSQL.")

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
    init_db()
    app.run(host='0.0.0.0', debug=True)