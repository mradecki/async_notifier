import asyncio
import aio_pika
import asyncpg

DB_URI = "postgresql://username:password@postgres:5432/mydatabase"
RABBITMQ_URI = "amqp://guest:guest@rabbitmq:5672/"
PG_CHANNEL = "channel"
EXCHANGE_NAME = "exchange"  # Update with your exchange name
ROUTING_KEY = "routing_key"  # Update with your routing key



async def send_to_rabbitmq(message):
    connection = await aio_pika.connect(RABBITMQ_URI)
    try:
        channel = await connection.channel()
        exchange = await channel.declare_exchange(EXCHANGE_NAME, aio_pika.ExchangeType.FANOUT)
        await exchange.publish(aio_pika.Message(body=message), routing_key=ROUTING_KEY)
        print(f"Sent message to RabbitMQ: {message}")
    finally:
        await connection.close()

async def listen_to_pg_notifications():
    pg_conn = await asyncpg.connect(DB_URI)
    try:
        await pg_conn.add_listener(PG_CHANNEL, handle_pg_notification)
        while True:
            await asyncio.sleep(10)
    finally:
        await pg_conn.close()

async def handle_pg_notification(conn, pid, channel, payload):
    message = f"PostgreSQL Notification: {payload}"
    await send_to_rabbitmq(message.encode("utf-8"))

async def main():
    await listen_to_pg_notifications()

if __name__ == "__main__":
    asyncio.run(main())