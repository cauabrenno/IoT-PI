from flask import Flask, request, jsonify, render_template
import psycopg2 # <--- MUDANÇA: Importamos a nova biblioteca
import os       # Usado para pegar a senha de forma segura

# --- CONFIGURAÇÃO DA CONEXÃO COM O POSTGRESQL ---
# É uma ótima prática não colocar senhas diretamente no código.
# Vamos configurar uma "Variável de Ambiente" para a senha.
DB_NAME = "sensor_deslizamento" # O nome do banco que você criou
DB_USER = "postgres"            # O usuário padrão do PostgreSQL
DB_HOST = "localhost"           # O servidor está rodando na sua máquina
DB_PASS = ("caua") # Pega a senha 

# --- FIM DA CONFIGURAÇÃO ---

app = Flask(__name__)

# Função para criar uma conexão com o banco de dados
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

# Função para inicializar o banco de dados (criar a tabela se não existir)
def init_db():
    conn = get_db_connection()
    if conn:
        with conn.cursor() as cur:
            # MUDANÇA: A sintaxe para auto-incremento é "SERIAL PRIMARY KEY"
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

# Endpoint para RECEBER dados
@app.route('/dados', methods=['POST'])
def receber_dados():
    dados = request.json
    umidade = dados.get('field1')
    vibracao = dados.get('field2')
    botao = dados.get('field3')

    conn = get_db_connection()
    if not conn:
        return jsonify({"status": "erro", "mensagem": "Falha na conexão com o banco"}), 500

    # MUDANÇA: Usamos a sintaxe com %s para passar parâmetros no psycopg2
    sql = "INSERT INTO leituras (umidade, vibracao, botao) VALUES (%s, %s, %s)"
    
    with conn.cursor() as cur:
        cur.execute(sql, (umidade, vibracao, botao))
    conn.commit()
    conn.close()

    print(f"Dados salvos no PostgreSQL: Umidade={umidade}, Vibração={vibracao}, Botão={botao}")
    return jsonify({"status": "sucesso"}), 200

# Endpoint para FORNECER os últimos dados
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
            "timestamp": leitura[3].isoformat() # Usamos .isoformat() para datas
        }
        return jsonify(dados)
    else:
        return jsonify({})

# Endpoint para MOSTRAR o dashboard
@app.route('/')
def dashboard():
    return render_template('index.html')

if __name__ == '__main__':
    if not DB_PASS:
        print("!!! ERRO: A variável de ambiente DB_PASSWORD não está definida.")
    else:
        init_db()
        app.run(debug=True)