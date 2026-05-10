import os
import json
import pika
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST', 'rabbitmq')
MAILHOG_HOST = os.environ.get('MAILHOG_HOST', 'mailhog')
MAILHOG_PORT = int(os.environ.get('MAILHOG_PORT', 1025))

def enviar_email(destinatario, assunto, mensagem_corpo):
    """
    Monta e envia o e-mail em formato HTML usando a biblioteca nativa smtplib.
    """
    msg = MIMEMultipart("alternative")
    msg['Subject'] = assunto
    msg['From'] = "sistema@postaflow.com.br"
    msg['To'] = destinatario

    html = f"""
    <html>
      <body style="font-family: Arial, sans-serif; color: #333;">
        <h2>Você tem uma nova mensagem!</h2>
        <hr>
        <p><strong>Assunto:</strong> {assunto}</p>
        <p><strong>Mensagem:</strong></p>
        <div style="background-color: #f9f9f9; padding: 15px; border-radius: 5px;">
            {mensagem_corpo}
        </div>
        <br>
        <p style="font-size: 12px; color: #888;">Enviado via PostaFlow (Microsserviços)</p>
      </body>
    </html>
    """
    
    parte_html = MIMEText(html, 'html')
    msg.attach(parte_html)

    try:
        server = smtplib.SMTP(MAILHOG_HOST, MAILHOG_PORT)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"[!] Erro ao enviar e-mail via SMTP: {e}")
        return False

def callback(ch, method, properties, body):
    """
    Função acionada automaticamente toda vez que uma mensagem chega na fila.
    """
    print(f"[*] Mensagem recebida. Processando...")
    try:
        dados = json.loads(body.decode('utf-8'))
        destinatario = dados.get('destinatario')
        assunto = dados.get('assunto')
        mensagem = dados.get('mensagem')

        sucesso = enviar_email(destinatario, assunto, mensagem)

        if sucesso:
            print(f" [x] E-mail enviado com sucesso para {destinatario}")
            ch.basic_ack(delivery_tag=method.delivery_tag)
        else:
            print(" [!] Falha no envio. Devolvendo mensagem para a fila.")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

    except Exception as e:
        print(f"[!] Erro ao processar mensagem da fila: {e}")
        ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)

def iniciar_consumidor():
    """
    Estabelece a conexão com o RabbitMQ e inicia a escuta ativa.
    """
    conectado = False
    tentativas = 0
    
    while not conectado and tentativas < 5:
        try:
            print(f"[*] Tentando conectar ao RabbitMQ ({RABBITMQ_HOST})...")
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=RABBITMQ_HOST, port=5672)
            )
            channel = connection.channel()
            
            channel.queue_declare(queue='email_queue', durable=True)
            
            channel.basic_qos(prefetch_count=1)
            
            channel.basic_consume(
                queue='email_queue', 
                on_message_callback=callback
            )
            
            print(" [*] Conectado! Aguardando mensagens na fila 'email_queue'. Para sair, pressione CTRL+C")
            conectado = True
            channel.start_consuming()
            
        except pika.exceptions.AMQPConnectionError:
            tentativas += 1
            print(f"[!] RabbitMQ indisponível. Tentando novamente em 5 segundos... ({tentativas}/5)")
            time.sleep(5)

if __name__ == '__main__':
    iniciar_consumidor()