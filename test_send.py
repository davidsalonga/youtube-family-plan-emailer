#!/usr/bin/env python3
"""
Test script - Send email only to salongadaviid@gmail.com for testing
"""

import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class TestEmailSender:
    def __init__(self):
        # Email configuration from environment variables
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.sender_email = os.getenv('SENDER_EMAIL')
        self.sender_password = os.getenv('SENDER_PASSWORD')

        # Test recipient
        self.test_recipients = [
            'salongadaviid@gmail.com'
        ]

        # Email subject
        self.subject = "TEST - YouTube Family Plan - Monthly Payment Due ({date})"

    def get_breakdown_content(self):
        """Get the formatted YouTube Family Plan breakdown"""
        return """📋 Monthly Plan Details

Total Monthly Cost: ₱379
Per Person Share: ₱95

👥 Members
---------------------------------
Sophia
David
Coach John
Rollen  

💳 Payment Method
GCash
Francis David Salonga
📱 0998 850 2851

💡 Note:
Individual YouTube Premium costs around ₱189/month.
This family plan keeps your cost lower at just ₱95 👍"""

    def create_test_email_message(self, recipient):
        """Create test email message for a recipient"""
        current_date = datetime.now().strftime("%B %Y")
        breakdown_content = self.get_breakdown_content()

        message = MIMEMultipart()
        from email.utils import formataddr
        message["From"] = formataddr(("David Salonga", self.sender_email))
        message["To"] = recipient
        message["Subject"] = self.subject.format(date=current_date)
        message["Reply-To"] = f"David Salonga <{self.sender_email}>"

        html_body = f"""
<html>
<body style="font-family: Arial, sans-serif;">
    <p>Hello David,</p>

    <p><strong>*** THIS IS A TEST EMAIL ***</strong></p>

    <p>This is your monthly reminder for the YouTube Family Plan payment due on the 20th of {current_date}.</p>

    <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; font-family: monospace;">
        <pre style="margin: 0; font-family: monospace; white-space: pre-wrap;">{breakdown_content}</pre>
    </div>

    <p><strong>After sending payment, kindly send a screenshot via reply to this email or through messenger as confirmation.</strong></p>

    <p>Thank you!</p>

    <p>Best regards,<br>
    YouTube Family Plan Manager</p>

    <p><strong>*** END TEST EMAIL ***</strong></p>
</body>
</html>
"""

        message.attach(MIMEText(html_body, "html"))
        return message

    def send_test_emails(self):
        """Send test emails to test recipients"""
        if not self.sender_email or not self.sender_password:
            logging.error("Email credentials not found in environment variables")
            return False

        current_date = datetime.now()
        logging.info(f"Sending TEST emails for {current_date.strftime('%B %Y')}")

        success_count = 0

        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)

            for recipient in self.test_recipients:
                try:
                    message = self.create_test_email_message(recipient)
                    server.send_message(message)
                    logging.info(f"✅ Sent to {recipient}")
                    success_count += 1
                except Exception as e:
                    logging.error(f"❌ Failed {recipient}: {str(e)}")

            server.quit()
            return success_count == len(self.test_recipients)

        except Exception as e:
            logging.error(f"SMTP error: {str(e)}")
            return False


def main():
    print("=== YouTube Family Plan Email Test ===")
    print("Sending test email to: salongadaviid@gmail.com\n")

    sender = TestEmailSender()
    success = sender.send_test_emails()

    if success:
        print("\n✅ Test email sent successfully!")
    else:
        print("\n❌ Failed to send test email")
        exit(1)


if __name__ == "__main__":
    main()
``
