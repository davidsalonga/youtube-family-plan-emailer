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
            'azorlanac@gmail.com',          # Azor Lanac
            'salongadaviid@gmail.com'       # David Salonga
        ]
        
        
        # Email content
        self.subject = "YouTube Family Plan - Monthly Payment Due ({date})"
    
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
    
    def create_email_message(self, recipient):
        """Create email message for a recipient"""
        current_date = datetime.now().strftime("%B %Y")
        breakdown_content = self.get_breakdown_content()
        
        message = MIMEMultipart()
        from email.utils import formataddr
        message["From"] = formataddr(("David Salonga", self.sender_email))
        message["To"] = recipient
        message["Subject"] = self.subject.format(date=current_date)
        message["Reply-To"] = f"YouTube Family Plan Manager <{self.sender_email}>"
        
        # HTML version with proper formatting
        html_body = f"""
<html>
<body style="font-family: Arial, sans-serif;">
    <p>Hello,</p>
    
    <p>This is your monthly reminder for the YouTube Family Plan payment due on the 20th of {current_date}.</p>
    
    <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; font-family: monospace;">
        <pre style="margin: 0; font-family: monospace; white-space: pre-wrap;">{breakdown_content}</pre>
    </div>
    
    <p><strong>After sending payment, kindly send a screenshot via reply to this email or through messenger as confirmation.</strong></p>
    
    <p>Thank you!</p>
    
    <p>Best regards,<br>
    YouTube Family Plan Manager</p>
</body>
</html>"""
        
        message.attach(MIMEText(html_body, "html"))
        
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
        
        logging.info(f"Recipients to send to: {self.recipients}")
        
        for recipient in self.recipients:
            logging.info(f"Preparing email for: {recipient}")
            message = self.create_email_message(recipient)
            if self.send_email(recipient, message):
                success_count += 1
                logging.info(f"✅ Successfully sent to: {recipient}")
            else:
                logging.error(f"❌ Failed to send to: {recipient}")
        
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