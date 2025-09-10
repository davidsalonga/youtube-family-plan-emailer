# GitHub Actions Setup Instructions

Follow these steps to deploy your YouTube Family Plan email sender to GitHub Actions for automatic monthly execution.

## Step 1: Create a GitHub Repository

1. Go to [GitHub.com](https://github.com) and sign in
2. Click "New repository" (green button)
3. Name it: `youtube-family-plan-emailer`
4. Make it **Private** (recommended for email scripts)
5. Click "Create repository"

## Step 2: Upload Your Files

### Option A: Using GitHub Web Interface
1. Click "uploading an existing file"
2. Drag and drop all files from your `Email Distribution` folder:
   - `github_email_sender.py`
   - `YouTube Family Plan Breakdown.txt`
   - `requirements.txt`
   - `.github/workflows/monthly-email.yml`
3. Commit the files

### Option B: Using Git Commands
```bash
git init
git add .
git commit -m "Initial commit: YouTube Family Plan email sender"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/youtube-family-plan-emailer.git
git push -u origin main
```

## Step 3: Set Up Email Credentials (GitHub Secrets)

1. In your GitHub repository, go to **Settings** tab
2. Click **Secrets and variables** → **Actions**
3. Click **New repository secret** and add these secrets:

   | Secret Name | Value | Example |
   |-------------|-------|---------|
   | `SMTP_SERVER` | `smtp.gmail.com` | For Gmail |
   | `SMTP_PORT` | `587` | For Gmail TLS |
   | `SENDER_EMAIL` | Your email address | `your.email@gmail.com` |
   | `SENDER_PASSWORD` | Your app password | See instructions below |

### Getting Gmail App Password:
1. Enable 2-Factor Authentication on your Google account
2. Go to [Google App Passwords](https://myaccount.google.com/apppasswords)
3. Select "Mail" and your device
4. Copy the generated 16-character password
5. Use this as your `SENDER_PASSWORD` secret

## Step 4: Test the Setup

1. Go to **Actions** tab in your repository
2. Click on "Monthly YouTube Family Plan Email"
3. Click "Run workflow" → "Run workflow" (green button)
4. Check if emails are sent successfully

## Step 5: Verify Schedule

The workflow is set to run automatically:
- **When**: 20th of every month at 9:00 AM UTC
- **Cron**: `0 9 20 * *`

### To change the time:
Edit `.github/workflows/monthly-email.yml` and modify the cron expression:
- `0 1 20 * *` = 1:00 AM UTC
- `0 17 20 * *` = 5:00 PM UTC (1:00 PM Philippine Time)

## Troubleshooting

### If emails fail to send:
1. Check **Actions** tab for error logs
2. Verify your GitHub Secrets are correct
3. Ensure Gmail App Password is valid
4. Check if Gmail account has 2FA enabled

### If workflow doesn't run:
1. Repository must have at least one commit
2. Workflow file must be in `.github/workflows/`
3. YAML syntax must be correct

### To run immediately (for testing):
1. Go to **Actions** tab
2. Select the workflow
3. Click "Run workflow" manually

## Monthly Execution

Once set up, GitHub Actions will:
- Run automatically on the 20th of each month at 9 AM UTC
- Send emails to all 4 recipients
- Include the current breakdown from your text file
- Log all activities (viewable in Actions tab)

## Free Usage Limits

GitHub Actions provides:
- 2,000 minutes/month for private repositories
- Unlimited for public repositories
- Your script uses ~1 minute per month = well within limits

## Security Notes

- Keep your repository **private** to protect email addresses
- Never commit passwords directly to code
- Use GitHub Secrets for all sensitive information
- App passwords are safer than regular passwords

Your email sender is now fully automated and will run every month without needing your computer!
