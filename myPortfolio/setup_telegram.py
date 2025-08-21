#!/usr/bin/env python3
"""
Telegram Bot Setup Script
This script helps you get your Telegram chat ID and test the bot connection.
"""

import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get bot token from environment variable
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not BOT_TOKEN:
    print("❌ ERROR: TELEGRAM_BOT_TOKEN not found in environment variables!")
    print("Please set TELEGRAM_BOT_TOKEN in your .env file")
    print("Example: TELEGRAM_BOT_TOKEN=your_bot_token_here")
    print("\nTo create .env file:")
    print("1. Copy env_template.txt to .env")
    print("2. Update TELEGRAM_BOT_TOKEN with your new bot token")
    print("3. Make sure to regenerate your bot token first!")
    exit(1)

def get_updates():
    """Get recent updates from the bot to find your chat ID"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if data['ok'] and data['result']:
            print("Recent updates found:")
            for update in data['result']:
                if 'message' in update:
                    chat = update['message']['chat']
                    print(f"Chat ID: {chat['id']}")
                    print(f"Chat Type: {chat['type']}")
                    if 'username' in chat:
                        print(f"Username: @{chat['username']}")
                    if 'first_name' in chat:
                        print(f"First Name: {chat['first_name']}")
                    print(f"Message: {update['message'].get('text', 'No text')}")
                    print("-" * 50)
        else:
            print("No recent updates found.")
            print("Try sending a message to your bot first.")
            
    except Exception as e:
        print(f"Error getting updates: {e}")

def test_bot():
    """Test if the bot is working"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getMe"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if data['ok']:
            bot_info = data['result']
            print("✅ Bot is working!")
            print(f"Bot Name: {bot_info['first_name']}")
            print(f"Bot Username: @{bot_info['username']}")
            print(f"Bot ID: {bot_info['id']}")
        else:
            print("❌ Bot is not working properly")
            
    except Exception as e:
        print(f"❌ Error testing bot: {e}")

def send_test_message(chat_id):
    """Send a test message to verify the bot can send messages"""
    if not chat_id:
        print("❌ No chat ID provided")
        return
        
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": "🎉 Hello! This is a test message from your portfolio contact form bot.",
        "parse_mode": "HTML"
    }
    
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        result = response.json()
        
        if result['ok']:
            print("✅ Test message sent successfully!")
        else:
            print(f"❌ Failed to send message: {result}")
            
    except Exception as e:
        print(f"❌ Error sending test message: {e}")

def main():
    print("🤖 Telegram Bot Setup Script")
    print("=" * 40)
    print(f"Bot Token: {BOT_TOKEN[:10]}...{BOT_TOKEN[-10:]} (truncated for security)")
    
    # Test bot connection
    print("\n1. Testing bot connection...")
    test_bot()
    
    # Get recent updates
    print("\n2. Getting recent updates...")
    get_updates()
    
    # Instructions
    print("\n📋 Instructions:")
    print("1. Start a chat with your bot on Telegram")
    print("2. Send any message to the bot")
    print("3. Run this script again to get your chat ID")
    print("4. Set the TELEGRAM_CHAT_ID environment variable")
    
    # Ask for chat ID to test
    print("\n3. Test message sending...")
    chat_id = input("Enter your chat ID to send a test message (or press Enter to skip): ").strip()
    
    if chat_id:
        try:
            chat_id = int(chat_id)
            send_test_message(chat_id)
        except ValueError:
            print("❌ Invalid chat ID. Please enter a number.")
    
    print("\n✨ Setup complete!")
    print("Remember to set TELEGRAM_CHAT_ID in your environment variables.")

if __name__ == "__main__":
    main()
