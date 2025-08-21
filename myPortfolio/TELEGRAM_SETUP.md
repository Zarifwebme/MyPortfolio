# 🤖 Telegram Bot Setup for Contact Form

This guide will help you set up the Telegram bot to receive contact form messages from your portfolio website.

## 📋 Prerequisites

- Python 3.7+
- Flask application running
- Telegram account
- Bot token (already configured: `8383855041:AAH_EMuvVGBFIzFNde8sd0N5CCJ3ebxzQ-Y`)

## 🚀 Setup Steps

### 1. Get Your Chat ID

1. **Start a chat with your bot:**
   - Open Telegram
   - Search for your bot username
   - Click "Start" or send `/start`

2. **Send a message to the bot:**
   - Type any message (e.g., "Hello")
   - Send it to the bot

3. **Run the setup script:**
   ```bash
   cd myPortfolio
   python setup_telegram.py
   ```

4. **Note your Chat ID:**
   - The script will display your Chat ID
   - It's usually a number like `123456789`

### 2. Set Environment Variable

Set the `TELEGRAM_CHAT_ID` environment variable:

**Option A: Create a .env file (recommended for development)**
```bash
# Create .env file in your project root
echo "TELEGRAM_CHAT_ID=YOUR_CHAT_ID_HERE" > .env
```

**Option B: Set system environment variable**
```bash
# Windows (PowerShell)
$env:TELEGRAM_CHAT_ID="YOUR_CHAT_ID_HERE"

# Windows (Command Prompt)
set TELEGRAM_CHAT_ID=YOUR_CHAT_ID_HERE

# Linux/Mac
export TELEGRAM_CHAT_ID="YOUR_CHAT_ID_HERE"
```

**Option C: Set in production environment**
- Set the environment variable in your hosting platform
- For Heroku: `heroku config:set TELEGRAM_CHAT_ID=YOUR_CHAT_ID_HERE`

### 3. Test the Setup

1. **Run the setup script again:**
   ```bash
   python setup_telegram.py
   ```

2. **Enter your Chat ID when prompted**
3. **Check Telegram for the test message**

## 🔧 How It Works

### Contact Form Fields
The contact form now includes:
- **First Name** (required)
- **Last Name** (required)  
- **Phone Number** (required)
- **Message** (required)

### Message Flow
1. User fills out contact form
2. Form data is sent to `/api/contact` endpoint
3. Backend validates the data
4. Message is formatted and sent to Telegram
5. Contact is saved to database (if available)
6. User receives success confirmation

### Telegram Message Format
```
📧 New Contact Form Submission

👤 Name: John Doe
📱 Phone: +1234567890
💬 Message:

Hello, I'm interested in your services...

---
Sent from your portfolio website
```

## 🐛 Troubleshooting

### Bot Not Responding
- Check if bot token is correct
- Verify bot is not blocked
- Ensure bot has permission to send messages

### Chat ID Not Found
- Make sure you've sent a message to the bot
- Run the setup script after sending a message
- Check if the bot is active

### Messages Not Received
- Verify `TELEGRAM_CHAT_ID` is set correctly
- Check application logs for errors
- Ensure the bot is not muted in Telegram

### Database Errors
- The system will continue working even if database save fails
- Check database connection and models
- Verify Contact model has correct fields

## 📱 Testing the Contact Form

1. **Fill out the contact form on your website**
2. **Submit the form**
3. **Check Telegram for the message**
4. **Verify the message format and content**

## 🔒 Security Notes

- Bot token is stored in code (consider moving to environment variables)
- Chat ID should be kept private
- Form validation prevents malicious input
- Rate limiting can be added if needed

## 📞 Support

If you encounter issues:
1. Check the application logs
2. Verify environment variables
3. Test bot connection with setup script
4. Ensure all dependencies are installed

## 🎯 Next Steps

After setup:
1. Test the contact form thoroughly
2. Customize the message format if needed
3. Add additional validation rules
4. Consider adding rate limiting
5. Monitor bot usage and performance

---

**Happy coding! 🚀**
