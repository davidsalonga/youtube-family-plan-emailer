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
        
        # Path to the YouTube Family Plan breakdown file
        self.breakdown_file = 'YouTube Family Plan Breakdown.txt'
        
        # Email content
        self.subject = "TEST - YouTube Family Plan - Monthly Payment Due ({date})"
    
    def read_breakdown_content(self):
        """Read the YouTube Family Plan breakdown from file"""
        try:
            with open(self.breakdown_file, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            logging.error(f"Breakdown file '{self.breakdown_file}' not found")
            return "YouTube Family Plan Breakdown file not found."
        except Exception as e:
            logging.error(f"Error reading breakdown file: {str(e)}")
            return "Error reading YouTube Family Plan breakdown."
    
    def create_test_email_message(self):
        """Create test email message"""
        current_date = datetime.now().strftime("%B %Y")
        breakdown_content = self.read_breakdown_content()
        
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = self.test_recipient
        message["Subject"] = self.subject.format(date=current_date)
        
        body = f"""Hello David,

*** THIS IS A TEST EMAIL ***

This is your monthly reminder for the YouTube Family Plan payment due on the 20th of {current_date}.

{breakdown_content}

Please send your share of ₱94.75 to complete the monthly payment.

Thank you!

Best regards,
YouTube Family Plan Manager

*** END TEST EMAIL ***"""
        
        message.attach(MIMEText(body, "plain"))
        
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
        
        try:
            message = self.create_test_email_message()
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
            
            logging.info(f"TEST email sent successfully to {self.test_recipient}")
            return True
            
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