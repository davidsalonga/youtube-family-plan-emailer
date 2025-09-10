#!/usr/bin/env python3
"""
Test script for GitHub Email Sender - YouTube Family Plan
Tests the email functionality without actually sending emails
"""

import unittest
from unittest.mock import Mock, patch, mock_open
import os
import sys
from io import StringIO
from github_email_sender import GitHubEmailSender

class TestGitHubEmailSender(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment"""
        # Mock environment variables
        self.env_vars = {
            'SMTP_SERVER': 'smtp.gmail.com',
            'SMTP_PORT': '587',
            'SENDER_EMAIL': 'test@example.com',
            'SENDER_PASSWORD': 'test_password'
        }
        
        # Create sender instance with mocked environment
        with patch.dict(os.environ, self.env_vars):
            self.sender = GitHubEmailSender()
    
    def test_initialization(self):
        """Test proper initialization of GitHubEmailSender"""
        with patch.dict(os.environ, self.env_vars):
            sender = GitHubEmailSender()
            
            self.assertEqual(sender.smtp_server, 'smtp.gmail.com')
            self.assertEqual(sender.smtp_port, 587)
            self.assertEqual(sender.sender_email, 'test@example.com')
            self.assertEqual(sender.sender_password, 'test_password')
            
            # Test recipients are loaded
            expected_recipients = [
                'sophiaypa@gmail.com',
                'jeff.rosarito@gmail.com', 
                'azorlanac@gmail.com',
                'salongadaviid@gmail.com'
            ]
            self.assertEqual(sender.recipients, expected_recipients)
    
    def test_read_breakdown_content_success(self):
        """Test successful reading of breakdown file"""
        test_content = "Test YouTube Family Plan Breakdown Content"
        
        with patch('builtins.open', mock_open(read_data=test_content)):
            content = self.sender.read_breakdown_content()
            self.assertEqual(content, test_content)
    
    def test_read_breakdown_content_file_not_found(self):
        """Test handling of missing breakdown file"""
        with patch('builtins.open', side_effect=FileNotFoundError()):
            with patch('logging.error') as mock_logging:
                content = self.sender.read_breakdown_content()
                self.assertEqual(content, "YouTube Family Plan Breakdown file not found.")
                mock_logging.assert_called_once()
    
    def test_create_email_message(self):
        """Test email message creation"""
        test_content = "Test breakdown content"
        recipient = "test@example.com"
        
        with patch.object(self.sender, 'read_breakdown_content', return_value=test_content):
            message = self.sender.create_email_message(recipient)
            
            self.assertEqual(message["From"], self.sender.sender_email)
            self.assertEqual(message["To"], recipient)
            self.assertIn("YouTube Family Plan", message["Subject"])
            
            # Check message body contains expected content
            body = message.get_payload()[0].get_payload()
            self.assertIn(test_content, body)
            self.assertIn("₱94.75", body)
    
    @patch('github_email_sender.smtplib.SMTP')
    def test_send_email_success(self, mock_smtp_class):
        """Test successful email sending"""
        mock_smtp = Mock()
        mock_smtp_class.return_value.__enter__.return_value = mock_smtp
        
        recipient = "test@example.com"
        message = Mock()
        
        result = self.sender.send_email(recipient, message)
        
        self.assertTrue(result)
        mock_smtp.starttls.assert_called_once()
        mock_smtp.login.assert_called_once_with(
            self.sender.sender_email, 
            self.sender.sender_password
        )
        mock_smtp.send_message.assert_called_once_with(message)
    
    @patch('github_email_sender.smtplib.SMTP')
    def test_send_email_failure(self, mock_smtp_class):
        """Test email sending failure handling"""
        mock_smtp_class.return_value.__enter__.side_effect = Exception("SMTP Error")
        
        recipient = "test@example.com"
        message = Mock()
        
        with patch('logging.error') as mock_logging:
            result = self.sender.send_email(recipient, message)
            
            self.assertFalse(result)
            mock_logging.assert_called_once()
    
    def test_send_monthly_emails_missing_credentials(self):
        """Test handling of missing email credentials"""
        with patch.dict(os.environ, {}, clear=True):
            sender = GitHubEmailSender()
            
            with patch('logging.error') as mock_logging:
                result = sender.send_monthly_emails()
                
                self.assertFalse(result)
                mock_logging.assert_called()
    
    @patch.object(GitHubEmailSender, 'send_email')
    @patch.object(GitHubEmailSender, 'create_email_message')
    def test_send_monthly_emails_all_success(self, mock_create_message, mock_send_email):
        """Test successful sending to all recipients"""
        mock_create_message.return_value = Mock()
        mock_send_email.return_value = True
        
        with patch('logging.info') as mock_logging:
            result = self.sender.send_monthly_emails()
            
            self.assertTrue(result)
            # Should call create_email_message for each recipient
            self.assertEqual(mock_create_message.call_count, len(self.sender.recipients))
            # Should call send_email for each recipient
            self.assertEqual(mock_send_email.call_count, len(self.sender.recipients))
    
    @patch.object(GitHubEmailSender, 'send_email')
    @patch.object(GitHubEmailSender, 'create_email_message')
    def test_send_monthly_emails_partial_failure(self, mock_create_message, mock_send_email):
        """Test partial failure when sending emails"""
        mock_create_message.return_value = Mock()
        # First two succeed, last two fail
        mock_send_email.side_effect = [True, True, False, False]
        
        with patch('logging.info') as mock_logging:
            result = self.sender.send_monthly_emails()
            
            self.assertFalse(result)  # Should return False if not all succeeded
            self.assertEqual(mock_send_email.call_count, len(self.sender.recipients))

class TestDryRun(unittest.TestCase):
    """Integration-style test that simulates the full process without sending emails"""
    
    def test_full_dry_run(self):
        """Test the complete email sending process without actually sending"""
        env_vars = {
            'SMTP_SERVER': 'smtp.gmail.com',
            'SMTP_PORT': '587',
            'SENDER_EMAIL': 'test@example.com',
            'SENDER_PASSWORD': 'test_password'
        }
        
        breakdown_content = """YouTube Family Plan Breakdown:
        Total Cost: ₱379
        Per Person: ₱94.75
        Payment Due: 20th of each month"""
        
        with patch.dict(os.environ, env_vars):
            with patch('builtins.open', mock_open(read_data=breakdown_content)):
                with patch('github_email_sender.smtplib.SMTP') as mock_smtp:
                    # Mock successful SMTP operations
                    mock_smtp.return_value.__enter__.return_value.starttls.return_value = None
                    mock_smtp.return_value.__enter__.return_value.login.return_value = None
                    mock_smtp.return_value.__enter__.return_value.send_message.return_value = None
                    
                    sender = GitHubEmailSender()
                    
                    # Capture logging output
                    with patch('sys.stdout', new=StringIO()) as fake_out:
                        result = sender.send_monthly_emails()
                        
                        self.assertTrue(result)
                        # Verify SMTP was called for each recipient
                        self.assertEqual(mock_smtp.call_count, len(sender.recipients))

def run_manual_test():
    """Manual test function to verify email creation without sending"""
    print("=== Manual Test: Email Creation ===")
    
    # Set up test environment
    os.environ.update({
        'SMTP_SERVER': 'smtp.gmail.com',
        'SMTP_PORT': '587', 
        'SENDER_EMAIL': 'test@example.com',
        'SENDER_PASSWORD': 'test_password'
    })
    
    sender = GitHubEmailSender()
    
    # Test breakdown file reading
    print("Testing breakdown file reading...")
    content = sender.read_breakdown_content()
    print(f"Breakdown content: {content[:50]}...")
    
    # Test email message creation
    print("\nTesting email message creation...")
    test_recipient = "test@example.com"
    message = sender.create_email_message(test_recipient)
    
    print(f"Subject: {message['Subject']}")
    print(f"From: {message['From']}")
    print(f"To: {message['To']}")
    print("\nEmail Body Preview:")
    print("-" * 50)
    body = message.get_payload()[0].get_payload()
    print(body)
    print("-" * 50)
    
    print(f"\nRecipients to send to: {len(sender.recipients)}")
    for i, recipient in enumerate(sender.recipients, 1):
        print(f"{i}. {recipient}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test the GitHub Email Sender")
    parser.add_argument("--manual", action="store_true", 
                       help="Run manual test to preview email content")
    parser.add_argument("--unittest", action="store_true", 
                       help="Run automated unit tests")
    
    args = parser.parse_args()
    
    if args.manual:
        run_manual_test()
    elif args.unittest or len(sys.argv) == 1:
        # Run unit tests by default
        unittest.main(argv=[''], exit=False, verbosity=2)
    
    if not args.manual and not args.unittest:
        print("\nTo run specific tests:")
        print("  python test_email_sender.py --manual    # Preview email content")
        print("  python test_email_sender.py --unittest  # Run automated tests")