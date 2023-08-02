from winreg import QueryInfoKey
import pika

credentials = pika.PlainCredentials()
parameters = pika.ConnectionParameters()
connection = pika.BlockingConnection(parameters)
channel = connection.channel()


# def callback(ch, method, properties, body):
#     print(" [x] Received %r" % body)
#     ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
# channel.basic_consume(on_message_callback=callback, queue='teste.fila1')

print(f"esperando e processando mensagem")
# channel.start_consuming()
for method, properties, body in channel.consume(queue="teste.fila1", inactivity_timeout=1):
    if not body:
        channel.cancel()
    else:
        print(" [x] Received %r" % body)
        channel.basic_ack(delivery_tag=method.delivery_tag)
