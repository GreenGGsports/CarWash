import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import current_app
from flask_login import current_user
import re
def send_confirm_email(reservation):
    # Get config values from Flask app context
    SMTP_SERVER = current_app.config["SMTP_SERVER"]
    SMTP_PORT = current_app.config["SMTP_PORT"]
    SMTP_LOGIN = current_app.config["SMTP_LOGIN"]
    SMTP_PASSWORD = current_app.config["SMTP_PASSWORD"]
    FROM_EMAIL = current_app.config["SMTP_FROM_EMAIL"]
    if current_user.is_authenticated and re.match(r"^[^@]+@[^@]+\.[^@]+$", current_user.user_name):
        user_email = current_user.user_name
        subject = "Test Email via Brevo SMTP"
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; color: #333;">
            <h2 style="color: #4CAF50;">Sikeres foglalás!</h2>
            <p>Kedves {reservation.customer.forname} {reservation.customer.lastname },</p>
            
            <p>Köszönjük, hogy bennünket választott! A foglalását sikeresen rögzítettük az alábbi adatokkal:</p>
            
            <ul>
            <li><strong>Autó típusa:</strong> {reservation.car.car_brand} {reservation.car.car_model}</li>
            <li><strong>Rendszám:</strong> {reservation.car.license_plate}</li>
            <li><strong>Időpont:</strong> {reservation.reservation_date.strftime('%Y.%m.%d')} {reservation.slot.start_time.strftime('%H:%M')}</li>
            <li><strong>Szolgáltatás:</strong> {reservation.service.service_name}</li>
            <li><strong>Helyszín:</strong> {reservation.carwash.carwash_name} - {reservation.carwash.location}</li>
            <li><strong>Végösszeg:</strong> {reservation.final_price} Ft</li>
            </ul>

            <p>Amennyiben módosítani szeretné foglalását, kérjük, vegye fel velünk a kapcsolatot.</p>
            <li><strong>Tel:</strong> {reservation.carwash.contact}</li>
            <li><strong>Email:</strong> info@automoso.eu</li>
            <p>Üdvözlettel,<br><strong>Eliteshine Autómosó csapata</strong></p>
        </body>
        </html>
        """
        msg = MIMEMultipart()
        msg["From"] = FROM_EMAIL
        msg["To"] =  user_email
        msg["Subject"] = subject
        msg.attach(MIMEText(html_content, "html"))

        try:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(SMTP_LOGIN, SMTP_PASSWORD)
                server.send_message(msg)
            print("✅ Email sent successfully.")
        except Exception as e:
            print("❌ Failed to send email:", str(e))
