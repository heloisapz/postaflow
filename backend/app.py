import os
import json
import pika
from flask import Flask, request, jsonify
from kazoo.client import KazooClient

app = Flask(__name__)

ZK_HOST = os.environ.get('ZOOKEEPER_HOST', 'zookeeper:2181')
DEFAULT_RABBIT_HOST = os.environ.get('RABBITMQ_HOST', 'rabbitmq')

def get_rabbitmq_config():
    """
    Consulta o ZooKeeper para obter o host do RabbitMQ.
    Implementa fallback para variáveis de ambiente caso o ZooKeeper falhe. 
    """
    zk = KazooClient(hosts=ZK_HOST)
    try:
        zk.start(timeout=5)
        
        if zk.exists("/config/rabbitmq/host"):
            data, stat = zk.get("/config/rabbitmq/host")
            rabbit_host = data.decode("utf-8")
            print(f"[*] Configuração lida do ZooKeeper: {rabbit_host}")
        else:
            rabbit_host = DEFAULT_RABBIT_HOST
            print("[!] Chave não encontrada no ZooKeeper. Usando padrão.")
            
        zk.stop()
        return rabbit_host
    except Exception as e:
        print(f"[!] Erro ao conectar ao ZooKeeper: {e}. Aplicando fallback.")
        return DEFAULT_RABBIT_HOST

@app.route('/api/enviar', methods=['POST'])
def despachar_email():
    """
    Recebe os dados do frontend e publica na fila do RabbitMQ. 
    """
    dados = request.get_json()
    
    if not dados or not all(k in dados for k in ("destinatario", "assunto", "mensagem")):
        return jsonify({"erro": "Dados incompletos"}), 400

    rabbit_host = get_rabbitmq_config()

    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=rabbit_host, port=5672)
        )
        channel = connection.channel()

        channel.queue_declare(queue='email_queue', durable=True)

        message = json.dumps(dados)
        channel.basic_publish(
            exchange='',
            routing_key='email_queue',
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2, 
                content_type='application/json'
            )
        )

        connection.close()
        print(f" [x] Tarefa enviada para a fila: {dados['destinatario']}")
        
        return jsonify({
            "status": "Sucesso", 
            "mensagem": "E-mail enfileirado para processamento assíncrono.",
            "broker_usado": rabbit_host
        }), 200

    except Exception as e:
        print(f"[!] Erro ao publicar no RabbitMQ: {e}")
        return jsonify({"erro": "Falha na mensageria", "detalhes": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)