"""
Email Digest Service - Daily Recommendations
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import get_settings

settings = get_settings()


def send_daily_digest(user_email: str, user_name: str, message: str, products: list):
    """Send daily recommendation email"""
    
    smtp_host = getattr(settings, 'smtp_host', None) or "smtp.gmail.com"
    smtp_port = int(getattr(settings, 'smtp_port', None) or 587)
    smtp_user = getattr(settings, 'smtp_user', None)
    smtp_password = getattr(settings, 'smtp_password', None)
    
    if not smtp_user or not smtp_password:
        print("⚠️ Email not configured - skipping")
        return False
    
    try:
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = user_email
        msg['Subject'] = "📚 Your Daily SmartReco AI Recommendations"
        
        product_html = ""
        for p in products[:3]:
            product_html += f"""
            <tr><td style="padding:10px;border-bottom:1px solid #eee;">
            <strong>{p['title']}</strong><br>
            <small>{p['category']} | {p['difficulty']} | ${p['price']}</small>
            </td></tr>"""
        
        body = f"""
        <html><body style="font-family:Arial;max-width:600px;margin:0 auto;padding:20px;">
        <h2>👋 Hi {user_name}!</h2>
        <p>{message}</p>
        <h3>📚 Today's Top Picks:</h3>
        <table style="width:100%;">{product_html}</table>
        <hr><p style="color:#666;font-size:12px;">Sent by SmartReco AI</p>
        </body></html>"""
        
        msg.attach(MIMEText(body, 'html'))
        
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
        
        print(f"✅ Digest sent to {user_email}")
        return True
        
    except Exception as e:
        print(f"❌ Email failed: {e}")
        return False