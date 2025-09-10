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
        
        # Test recipient - only your email
        self.test_recipient = 'salongadaviid@gmail.com'
        
        
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
    
    def create_test_email_message(self):
        """Create test email message"""
        current_date = datetime.now().strftime("%B %Y")
        breakdown_content = self.get_breakdown_content()
        
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = self.test_recipient
        message["Subject"] = self.subject.format(date=current_date)
        
        # Plain text version
        text_body = f"""Hello David,

*** THIS IS A TEST EMAIL ***

This is your monthly reminder for the YouTube Family Plan payment due on the 20th of {current_date}.

{breakdown_content}

Please send your share of ₱94.75 to complete the monthly payment.

Thank you!

Best regards,
YouTube Family Plan Manager

*** END TEST EMAIL ***"""

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
    
    <p>Please send your share of <strong>₱94.75</strong> to complete the monthly payment.</p>
    
    <p>Thank you!</p>
    
    <p>Best regards,<br>
    YouTube Family Plan Manager</p>
    
    <p><strong>*** END TEST EMAIL ***</strong></p>
</body>
</html>"""
        
        message.attach(MIMEText(text_body, "plain"))
        message.attach(MIMEText(html_body, "html"))
        
        return message
    
    def send_test_email(self):
        """Send test email to salongadaviid@gmail.com"""
        # Check if email credentials are available
        if not self.sender_email or not self.sender_password:
            logging.error("Email credentials not found in environment variables")
            logging.error("Please set SENDER_EMAIL and SENDER_PASSWORD environment variables")
            return False
        
        current_date = datetime.now()
        logging.info(f"Sending TEST email for {current_date.strftime('%B %Y')}")
        logging.info(f"Test recipient: {self.test_recipient}")
        logging.info(f"SMTP Server: {self.smtp_server}:{self.smtp_port}")
        logging.info(f"Sender Email: {self.sender_email}")
        
        try:
            message = self.create_test_email_message()
            
            # Create SMTP connection with more detailed error handling
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            logging.info("SMTP connection established")
            
            server.set_debuglevel(1)  # Enable SMTP debug output
            server.starttls()
            logging.info("TLS started")
            
            server.login(self.sender_email, self.sender_password)
            logging.info("Login successful")
            
            server.send_message(message)
            logging.info("Message sent")
            
            server.quit()
            logging.info(f"TEST email sent successfully to {self.test_recipient}")
            return True
            
        except smtplib.SMTPAuthenticationError as e:
            logging.error(f"SMTP Authentication failed: {str(e)}")
            logging.error("Make sure you're using a Gmail App Password, not your regular password")
            return False
        except smtplib.SMTPException as e:
            logging.error(f"SMTP error occurred: {str(e)}")
            return False
        except Exception as e:
            logging.error(f"Failed to send TEST email to {self.test_recipient}: {str(e)}")
            return False

def main():
    """Main function to run the test email sender"""
    print("=== YouTube Family Plan Email Test ===")
    print("This will send a TEST email ONLY to: salongadaviid@gmail.com")
    print("Running in GitHub Actions - no confirmation needed")
    print()
    
    sender = TestEmailSender()
    
    # Send test email
    success = sender.send_test_email()
    
    if success:
        print("\n✅ Test email sent successfully!")
        print("Check your inbox at salongadaviid@gmail.com")
    else:
        print("\n❌ Failed to send test email")
        print("Please check your email credentials and connection")
        exit(1)

if __name__ == "__main__":
    main()