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
        
        # Test recipients
        self.test_recipients = [
            'azorlanac@gmail.com',      # Azor Lanac
            'salongadaviid@gmail.com'   # David Salonga
        ]
        
        
        # Email content
        self.subject = "TEST - YouTube Family Plan - Monthly Payment Due ({date})"
    
    def get_breakdown_content(self):
        """Get the formatted YouTube Family Plan breakdown"""
        return """📋 Monthly Expense Breakdown

Total Monthly Cost: ₱379
Number of Members: 4
Per Person Share: ₱94.75

👥 Members & Shares
---------------------------------
Name                 Share (₱)
---------------------------------
Sophia Aguilar       94.75
Jeffrey Rosarito     94.75
Azor Lanac           94.75
David (Dab) Salonga  94.75

💳 Payment Method
GCash
Francis David Salonga
📱 0998 850 2851"""
    
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
        
        # HTML version with proper formatting
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
</html>"""
        
        message.attach(MIMEText(html_body, "html"))
        
        return message
    
    def send_test_emails(self):
        """Send test emails to test recipients"""
        # Check if email credentials are available
        if not self.sender_email or not self.sender_password:
            logging.error("Email credentials not found in environment variables")
            logging.error("Please set SENDER_EMAIL and SENDER_PASSWORD environment variables")
            return False
        
        current_date = datetime.now()
        logging.info(f"Sending TEST emails for {current_date.strftime('%B %Y')}")
        logging.info(f"Test recipients: {self.test_recipients}")
        logging.info(f"SMTP Server: {self.smtp_server}:{self.smtp_port}")
        logging.info(f"Sender Email: {self.sender_email}")
        
        success_count = 0
        
        try:
            # Create SMTP connection once for all emails
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            logging.info("SMTP connection established")
            
            server.starttls()
            logging.info("TLS started")
            
            server.login(self.sender_email, self.sender_password)
            logging.info("Login successful")
            
            # Send to each recipient
            for recipient in self.test_recipients:
                try:
                    message = self.create_test_email_message(recipient)
                    server.send_message(message)
                    logging.info(f"TEST email sent successfully to {recipient}")
                    success_count += 1
                except Exception as e:
                    logging.error(f"Failed to send TEST email to {recipient}: {str(e)}")
            
            server.quit()
            logging.info(f"Email send complete. Successfully sent to {success_count}/{len(self.test_recipients)} recipients")
            return success_count == len(self.test_recipients)
            
        except smtplib.SMTPAuthenticationError as e:
            logging.error(f"SMTP Authentication failed: {str(e)}")
            logging.error("Make sure you're using a Gmail App Password, not your regular password")
            return False
        except smtplib.SMTPException as e:
            logging.error(f"SMTP error occurred: {str(e)}")
            return False
        except Exception as e:
            logging.error(f"Failed to send TEST emails: {str(e)}")
            return False

def main():
    """Main function to run the test email sender"""
    print("=== YouTube Family Plan Email Test ===")
    print("This will send TEST emails to:")
    print("- azorlanac@gmail.com")
    print("- salongadaviid@gmail.com")
    print("Running in GitHub Actions - no confirmation needed")
    print()
    
    sender = TestEmailSender()
    
    # Send test emails
    success = sender.send_test_emails()
    
    if success:
        print("\n✅ Test emails sent successfully!")
        print("Check inboxes at both test recipients")
    else:
        print("\n❌ Failed to send test email")
        print("Please check your email credentials and connection")
        exit(1)

if __name__ == "__main__":
    main()