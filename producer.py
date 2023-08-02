import pika

credentials = pika.PlainCredentials()
parameters = pika.ConnectionParameters()
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.exchange_declare(exchange='teste.exchange1', exchange_type='direct', durable=True)
# channel.exchange_declare(exchange='teste.exchange2', exchange_type='direct', durable=True)

channel.queue_declare(
    queue='teste.fila1',
    durable=True,
    arguments={
        'x-dead-letter-exchange': 'teste.exchange1',
        'x-dead-letter-routing-key': 'teste.fila1',
    }
)
# channel.queue_declare(
#     queue='teste.fila2',
#     durable=True,
#     arguments={
#         'x-dead-letter-exchange': 'teste.exchange2',
#         'x-dead-letter-routing-key': 'teste.fila1',
#     }
# )


channel.queue_bind(
    exchange='teste.exchange1',
    routing_key='teste.fila1',  # x-dead-letter-routing-key
    queue='teste.fila1'
)
# channel.queue_bind(
#     exchange='teste.exchange1',
#     routing_key='teste.fila2',  # x-dead-letter-routing-key
#     queue='teste.fila2'
# )

message = "Olá mundo"

for i in range(2):
    message = f"Olá mundo {i}"
    channel.basic_publish(
        exchange='',
        routing_key='teste.fila1',
        body=message,
        properties=pika.BasicProperties(delivery_mode=2, message_id="teste2")
    )

print(f"Enviando mensagem {message}")

connection.close()
