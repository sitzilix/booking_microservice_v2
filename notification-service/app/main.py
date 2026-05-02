import asyncio
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from aiokafka import AIOKafkaConsumer
import os

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

def send_email(receiver_email, book_title):
    message = MIMEMultipart()
    message["From"] = SENDER_EMAIL
    message["To"] = receiver_email
    message["Subject"] = "Подтверждения бронирования книги"
    
    body = f"Здравствуйте! Книга '{book_title}' успешно забронирована за вами."
    message.attach(MIMEText(body, "plain"))
    
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, receiver_email, message.as_string())
        return True
    except Exception as e:
        print(f"Ошибка при отправке почты: {e}")
        return False
    
async def consume_notification():
    print("⏳ Начинаю настройку консьюмера...", flush=True)
    
    consumer = AIOKafkaConsumer(
        "booking_created",
        bootstrap_servers='kafka:9092', # <-- Если зависнет после настройки, значит ошибка в этом имени!
        group_id="notification-group",
        auto_offset_reset='earliest',
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )
    
    print("⏳ Пытаюсь подключиться к Kafka (await consumer.start())...", flush=True)
    await consumer.start()
    
    print("🚀 Консьюмер успешно подключился и ждет сообщений!", flush=True)
    
    try:
        async for msg in consumer:
            data = msg.value
            print(f"📥 Получены данные из Kafka: {data}", flush=True)
            
            email = data.get('email')
            title = data.get('book_title', 'string')
            
            print(f"📧 Пытаюсь отправить письмо на {email}...", flush=True)
            
            loop = asyncio.get_event_loop()
            success = await loop.run_in_executor(None, send_email, email, title)
            
            if success:
                print(f'✅ Письмо успешно ушло на {email}', flush=True)
            else:
                print(f'❌ Ошибка при отправке на {email}', flush=True)
    finally:
        await consumer.stop()
        print("🛑 Консьюмер остановлен.", flush=True)
        
if __name__ == "__main__":
    asyncio.run(consume_notification())