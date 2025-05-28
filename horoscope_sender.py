#!/usr/bin/env python3
"""
Daily Horoscope Sender
Fetches Spanish horoscopes for Cancer and Aquarius and sends via email/SMS
"""
import asyncio
import os
import smtplib
import requests
import schedule
import time
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from twilio.rest import Client
from datetime import datetime
from googletrans import Translator

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class HoroscopeService:
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.email_user = os.getenv('EMAIL_USER')
        self.email_password = os.getenv('EMAIL_PASSWORD')
        self.recipient_email = os.getenv('RECIPIENT_EMAIL')
        
        self.twilio_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.twilio_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.twilio_phone = os.getenv('TWILIO_PHONE_NUMBER')
        self.recipient_phone = os.getenv('RECIPIENT_PHONE')
        
        self.rapidapi_key = os.getenv('RAPIDAPI_KEY')
        self.rapidapi_host = 'horoscope-astrology.p.rapidapi.com'
        
        if self.twilio_sid and self.twilio_token:
            self.twilio_client = Client(self.twilio_sid, self.twilio_token)
        else:
            self.twilio_client = None
            logger.warning("Twilio credentials not provided - SMS disabled")

    async def get_horoscope(self, sign):
        """Fetch horoscope for a given sign using RapidAPI and translate to Spanish"""
        try:
            url = f"https://horoscope-astrology.p.rapidapi.com/horoscope"
            
            headers = {
                'x-rapidapi-host': self.rapidapi_host,
                'x-rapidapi-key': self.rapidapi_key
            }
            
            params = {
                'day': 'today',
                'sunsign': sign.lower()
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            horoscope_text = data.get('horoscope', 'No horoscope available')
            
            spanish_horoscope = await self.translate_to_spanish(horoscope_text, sign)
            
            logger.info(f"Successfully fetched and translated horoscope for {sign}")
            return spanish_horoscope
            
        except requests.RequestException as e:
            logger.error(f"Error fetching horoscope for {sign}: {e}")
            return self.get_fallback_horoscope(sign)
        except Exception as e:
            logger.error(f"Unexpected error getting horoscope: {e}")
            return self.get_fallback_horoscope(sign)

    async def translate_to_spanish(self, text, sign):
        """Translate horoscope to Spanish using Google Translate API"""
        try:
            async with Translator() as translator:
                result = await translator.translate(text, dest='es', src='en')
                translated_text = result.text
                
                spanish_enhancements = {
                    'cancer': [
                        f"🦀 Querida Cáncer: {translated_text}",
                        f"🦀 Para ti, Cáncer: {translated_text}",
                        f"🦀 Cáncer, mi amor: {translated_text}",
                    ],
                    'aquarius': [
                        f"🏺 Hermoso Acuario: {translated_text}",
                        f"🏺 Para ti, Acuario: {translated_text}",
                        f"🏺 Acuario, mi cielo: {translated_text}",
                    ]
                }
                
                import random
                sign_formats = spanish_enhancements.get(sign.lower(), [f"✨ {translated_text}"])
                final_message = random.choice(sign_formats)
                
                logger.info(f"Successfully translated horoscope for {sign}")
                return final_message
                
        except Exception as e:
            logger.error(f"Error translating horoscope for {sign}: {e}")
            return self.get_spanish_fallback(text, sign)
    
    def get_spanish_fallback(self, original_text, sign):
        """Fallback Spanish messages if Google Translate fails"""
        fallback_messages = {
            'cancer': [
                "🦀 Querida Cáncer: Hoy tu sensibilidad será tu mayor fortaleza. Las energías lunares te favorecen especialmente en el amor y la familia. ✨",
                "🦀 Para ti, Cáncer: Tu intuición maternal te guiará hacia decisiones acertadas. Es un día perfecto para nutrir tus relaciones más cercanas. 💕",
                "🦀 Cáncer, mi amor: Las emociones fluyen positivamente hoy. Confía en tu corazón para tomar las mejores decisiones. 🌙"
            ],
            'aquarius': [
                "🏺 Hermoso Acuario: Tu espíritu innovador brillará con fuerza especial hoy. Las amistades y conexiones sociales traerán sorpresas maravillosas. ✨",
                "🏺 Para ti, Acuario: Tu originalidad será reconocida y admirada por otros. Es momento de abrazar tu autenticidad completamente. 💫",
                "🏺 Acuario, mi cielo: Las ideas creativas fluyen libremente. Tu visión única del mundo inspirará a quienes te rodean. 🦋"
            ]
        }
        
        import random
        messages = fallback_messages.get(sign.lower(), ["✨ Hoy será un día especial lleno de buenas energías para ti. ✨"])
        return random.choice(messages)

    def get_fallback_horoscope(self, sign):
        """Return a fallback horoscope if API fails"""
        fallbacks = {
            'cancer': "Hoy es un día para cuidar de ti misma y de quienes amas, querida Cáncer. ✨",
            'aquarius': "Tu espíritu innovador brilla especialmente hoy, Acuario. ¡Deja que tu creatividad fluya! ✨"
        }
        return fallbacks.get(sign.lower(), "Hoy será un día especial lleno de buenas energías. ✨")

    def send_email(self, subject, body):
        """Send email with horoscopes"""
        try:
            if not all([self.email_user, self.email_password, self.recipient_email]):
                logger.warning("Email credentials incomplete - skipping email")
                return False

            msg = MIMEMultipart()
            msg['From'] = self.email_user
            msg['To'] = self.recipient_email
            msg['Subject'] = subject

            msg.attach(MIMEText(body, 'plain', 'utf-8'))

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_user, self.email_password)
                server.send_message(msg)

            logger.info("Email sent successfully")
            return True

        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return False

    def send_sms(self, message):
        """Send SMS with horoscopes to both recipients"""
        success_count = 0
        
        try:
            if not self.twilio_client:
                logger.warning("SMS configuration incomplete - skipping SMS")
                return False

            recipients = []
            if self.recipient_phone:
                recipients.append(('girlfriend', self.recipient_phone))
            
            if not recipients:
                logger.warning("No phone numbers configured - skipping SMS")
                return False

            for recipient_name, phone_number in recipients:
                try:
                    message_obj = self.twilio_client.messages.create(
                        body=message,
                        from_=self.twilio_phone,
                        to=phone_number
                    )
                    logger.info(f"SMS sent successfully to {recipient_name} ({phone_number}) - SID: {message_obj.sid}")
                    success_count += 1
                except Exception as e:
                    logger.error(f"Error sending SMS to {recipient_name} ({phone_number}): {e}")

            return success_count > 0

        except Exception as e:
            logger.error(f"General error sending SMS: {e}")
            return False

    async def send_daily_horoscopes(self):
        """Main function to fetch and send daily horoscopes"""
        logger.info("Starting daily horoscope delivery...")
        
        try:
            cancer_horoscope = await self.get_horoscope('cancer')
            aquarius_horoscope = await self.get_horoscope('aquarius')
            
            today = datetime.now().strftime('%d de %B, %Y')
            
            email_body = f"""¡Buenos días, mi amor! 💖

Aquí tienes tus horóscopos del día - {today}

{cancer_horoscope}

{aquarius_horoscope}

¡Que tengas un día maravilloso lleno de amor y buenas energías! ✨

Con todo mi amor 💕"""

            sms_body = f"🌟 Horóscopos de hoy - {today} 🌟\n\n{cancer_horoscope}\n\n{aquarius_horoscope}\n\n¡Te amo! 💕"

            email_subject = f"✨ Tus horóscopos del {today} ✨"
            email_sent = self.send_email(email_subject, email_body)
            
            sms_sent = self.send_sms(sms_body)
            
            status = f"Email: {'✅' if email_sent else '❌'}, SMS: {'✅' if sms_sent else '❌'}"
            logger.info(f"Daily horoscope delivery completed - {status}")
            
        except Exception as e:
            logger.error(f"Error in daily horoscope delivery: {e}")

def main():
    """Main application loop"""
    logger.info("🌟 Starting Horoscope Sender Application 🌟")
    
    service = HoroscopeService()
    
    if os.getenv('ENABLE_HEALTH_CHECK', 'true').lower() == 'true':
        from healthcheck import start_health_server
        import threading
        health_thread = threading.Thread(target=start_health_server, daemon=True)
        health_thread.start()
        logger.info("Health check server started on port 8080")
    
    async def scheduled_task():
        await service.send_daily_horoscopes()
    
    schedule.every().day.at("08:00").do(lambda: asyncio.run(scheduled_task()))
    
    if os.getenv('SEND_ON_STARTUP', 'false').lower() == 'true':
        logger.info("Sending test horoscope on startup...")
        asyncio.run(scheduled_task())
    
    logger.info("Scheduler started - horoscopes will be sent daily at 8:00 AM")
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()