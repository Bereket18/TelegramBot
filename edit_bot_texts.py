#!/usr/bin/env python3
"""
Telegram Bot Text Editor
This tool allows you to easily edit all the texts in your Telegram bot
"""

import json
import os
import re

def load_current_texts():
    """Load current texts from server.py"""
    with open('/app/backend/server.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract LANGUAGES dictionary
    pattern = r'LANGUAGES = ({.*?})'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        # This is a simple extraction - in a real scenario you'd want proper parsing
        languages_str = match.group(1)
        print("Current language texts found!")
    else:
        print("Could not find LANGUAGES dictionary")
        return None
    
    return content

def show_editable_texts():
    """Show all editable texts"""
    print("\n🔧 TELEGRAM BOT TEXT EDITOR")
    print("=" * 50)
    
    texts_to_edit = {
        "1": {
            "name": "Welcome Message (Amharic)",
            "current": """🕌 ኣስላም ዐላይኹም ወ ረሕመቱላሒ ወ በረካቱ

እንኮዋን ወደ የቁርአን ትምህርት ቦት ደህና መጡ!

በዚህ ቦት ላይ የሚያገኟቸው አገልግሎቶች:
✅ ቃኢዳ (መሠረታዊ አረብኛ እና ቁርኣን ንባብ)
✅ ተጅዊድ (ተከክለኛው የቁርአን አነባበብ መማር)
✅ ሂፍዝ (ቁርአንን በቅርበት መዘከር)
✅ ነዝር (ጥራት ያለው የቁርኣን ንባብ)

ለመጀመር ከታች ያለውን ቁልፍ ይጫኑ 👇""",
            "path": "welcome_text"
        },
        "2": {
            "name": "Channel URL",
            "current": "https://t.me/channelname",
            "path": "channel_url"
        },
        "3": {
            "name": "Admin URL", 
            "current": "https://t.me/adminusername",
            "path": "admin_url"
        },
        "4": {
            "name": "Education Program Cost",
            "current": "1500 Ethiopian Birr",
            "path": "education_cost"
        },
        "5": {
            "name": "Education Program Duration",
            "current": "30 minutes per day",
            "path": "education_duration"
        },
        "6": {
            "name": "Education Program Days",
            "current": "7 days a week",
            "path": "education_days"
        }
    }
    
    print("Available texts to edit:")
    for key, value in texts_to_edit.items():
        print(f"{key}. {value['name']}")
        print(f"   Current: {value['current'][:50]}{'...' if len(value['current']) > 50 else ''}")
        print()
    
    return texts_to_edit

def edit_text(choice, texts):
    """Edit a specific text"""
    if choice not in texts:
        print("Invalid choice!")
        return False
    
    text_info = texts[choice]
    print(f"\n📝 Editing: {text_info['name']}")
    print(f"Current text:\n{text_info['current']}")
    print("\nEnter new text (press Enter twice to finish):")
    
    lines = []
    while True:
        line = input()
        if line == "" and lines and lines[-1] == "":
            break
        lines.append(line)
    
    new_text = "\n".join(lines[:-1])  # Remove the last empty line
    
    if new_text.strip():
        print(f"\nNew text will be:\n{new_text}")
        confirm = input("Save this change? (y/n): ")
        if confirm.lower() == 'y':
            update_server_file(text_info['path'], new_text)
            print("✅ Text updated successfully!")
            return True
    
    print("❌ No changes made.")
    return False

def update_server_file(path, new_text):
    """Update the server.py file with new text"""
    with open('/app/backend/server.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Define replacement patterns based on path
    replacements = {
        "welcome_text": (
            r'welcome_text = """.*?"""',
            f'welcome_text = """{new_text}"""'
        ),
        "channel_url": (
            r'channel_url = "https://t\.me/channelname"',
            f'channel_url = "{new_text}"'
        ),
        "admin_url": (
            r'admin_url = "https://t\.me/adminusername"',
            f'admin_url = "{new_text}"'
        ),
        "education_cost": (
            r'💰 Cost: 1500 Ethiopian Birr',
            f'💰 Cost: {new_text}'
        ),
        "education_duration": (
            r'⏰ Duration: 30 minutes per day',
            f'⏰ Duration: {new_text}'
        ),
        "education_days": (
            r'📅 Days: 7 days a week',
            f'📅 Days: {new_text}'
        )
    }
    
    if path in replacements:
        pattern, replacement = replacements[path]
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        with open('/app/backend/server.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("📁 File updated. You may need to restart the backend server.")

def main():
    """Main function"""
    while True:
        texts = show_editable_texts()
        
        print("Choose option:")
        print("1-6: Edit text")
        print("0: Exit")
        print("r: Restart backend server")
        
        choice = input("\nEnter your choice: ").strip()
        
        if choice == "0":
            print("👋 Goodbye!")
            break
        elif choice == "r":
            print("🔄 Restarting backend server...")
            os.system("sudo supervisorctl restart backend")
            print("✅ Backend restarted!")
        elif choice in texts:
            edit_text(choice, texts)
        else:
            print("❌ Invalid choice!")

if __name__ == "__main__":
    main()
