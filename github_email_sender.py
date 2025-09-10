#!/usr/bin/env python3
"""
GitHub Actions version - Monthly Email Sender for YouTube Family Plan
Simplified version that runs once per execution (no continuous scheduling needed)
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

class GitHubEmailSender:
    def __init__(self):
        # Email configuration from environment variables (GitHub Secrets)
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.sender_email = os.getenv('SENDER_EMAIL')
        self.sender_password = os.getenv('SENDER_PASSWORD')
        
        # YouTube Family Plan recipients
        self.recipients = [
            'sophiaypa@gmail.com',          # Sophia Aguilar
            'jeff.rosarito@gmail.com',      # Jeffrey Rosarito
            'azorlanac@gmail.com',          # Azor Lanac
            'salongadaviid@gmail.com'       # David Salonga
        ]
        
        # Path to the YouTube Family Plan breakdown file
        self.breakdown_file = 'YouTube Family Plan Breakdown.txt'
        
        # Email content
        self.subject = "YouTube Family Plan - Monthly Payment Due ({date})"
    
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
    
    def create_email_message(self, recipient):
        """Create email message for a recipient"""
        current_date = datetime.now().strftime("%B %Y")
        breakdown_content = self.read_breakdown_content()
        
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = recipient
        message["Subject"] = self.subject.format(date=current_date)
        
        body = f"""Hello,

This is your monthly reminder for the YouTube Family Plan payment due on the 20th of {current_date}.

{breakdown_content}

Please send your share of ₱94.75 to complete the monthly payment.

Thank you!

Best regards,
YouTube Family Plan Manager"""
        
        message.attach(MIMEText(body, "plain"))
        
        return message
    
    def send_email(self, recipient, message):
        """Send email to a specific recipient"""
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
            
            logging.info(f"Email sent successfully to {recipient}")
            return True
        except Exception as e:
            logging.error(f"Failed to send email to {recipient}: {str(e)}")
            return False
    
    def send_monthly_emails(self):
        """Send emails to all recipients"""
        current_date = datetime.now()
        
        logging.info(f"Starting monthly email send for {current_date.strftime('%B %Y')}")
        logging.info(f"Today is the {current_date.day}th of the month")
        
        # Check if email credentials are available
        if not self.sender_email or not self.sender_password:
            logging.error("Email credentials not found in environment variables")
            return False
        
        success_count = 0
        total_recipients = len(self.recipients)
        
        for recipient in self.recipients:
            message = self.create_email_message(recipient)
            if self.send_email(recipient, message):
                success_count += 1
        
        logging.info(f"Email send complete. Successfully sent to {success_count}/{total_recipients} recipients")
        return success_count == total_recipients

def main():
    """Main function to run the email sender"""
    sender = GitHubEmailSender()
    
    # Send emails (GitHub Actions will handle the scheduling)
    success = sender.send_monthly_emails()
    
    if not success:
        exit(1)  # Exit with error code if sending failed

if __name__ == "__main__":
    main()