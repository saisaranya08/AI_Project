import os
from dotenv import load_dotenv
from pymongo import MongoClient
import telebot
import google.generativeai as genai
import signal
import sys
import requests

# Load environment variables
load_dotenv()


# Get MongoDB URI
MONGODB_URI = os.getenv("MONGODB_URI")

# Connect to MongoDB
client = MongoClient(MONGODB_URI)
db = client["telegram_bot_db"]  # Create a new database
users_collection = db["users"]  # Create a collection for users
chats_collection = db["chats"]

# Test: Insert a sample document
users_collection.insert_one({"name": "Test User", "username": "testuser"})

print("MongoDB Connected! Data inserted successfully.")

bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
# print(f"Bot Token: {bot_token}")
bot = telebot.TeleBot(bot_token)

#Initialize Gemini AI
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

#custom search API configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
CSE_ID = os.getenv("CSE_ID")

# register new user
@bot.message_handler(commands=['start'])
def start(message):
    # Check if the user already exists
    user = users_collection.find_one({"chat_id": message.chat.id})

    if not user:
        # New user - save their information
        users_collection.insert_one({
            "first_name": message.from_user.first_name,
            "username": message.from_user.username,
            "chat_id": message.chat.id,
            "phone_number": None,  # Placeholder for phone number
        })
        print(f"New user registered: {message.from_user.first_name} ({message.from_user.username})")
        bot.reply_to(message, "Welcome, new user! Please share your phone number using the contact button.")

    else:
        print(f"User already exists: {message.from_user.first_name} ({message.from_user.username})")
        bot.reply_to(message, "Welcome back!")

# Request phone number
@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    # Update user with phone number
    user = users_collection.find_one({"chat_id": message.chat.id})
    
    if user:
        users_collection.update_one(
            {"chat_id": message.chat.id},
            {"$set": {"phone_number": message.contact.phone_number}}
        )
        print(f"Phone number saved for {message.from_user.first_name}: {message.contact.phone_number}")
        bot.reply_to(message, "Phone number saved successfully!")
# Gemini AI Chat Handler
@bot.message_handler(func=lambda message: True)
def chat_with_gemini(message):
    user_input = message.text  # User's message
    chat_id = message.chat.id

    # Send typing action
    bot.send_chat_action(chat_id, 'typing')

    # Use Gemini AI to generate a response
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(user_input).text  # Get AI response
    except Exception as e:
        response = "Sorry, I couldn't process your request right now."
    # Send AI response back to user
    bot.reply_to(message, response)

  
@bot.message_handler(content_types=['photo', 'document'])
def handle_file_upload(message):
    """Handles user-uploaded images and documents, saving metadata in MongoDB and analyzing them with Gemini AI."""
    
    # Get file info and download the file
    file_info = bot.get_file(message.photo[-1].file_id) if message.content_type == 'photo' else bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    # Determine file name and type
    file_name = message.photo[-1].file_id + ".jpg" if message.content_type == 'photo' else message.document.file_name

    # Save file locally (optional)
    with open(file_name, 'wb') as file:
        file.write(downloaded_file)

    # Call the Gemini AI model with image data and a text parameter
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")  # Use the updated model
        
        # Preparing the data in the expected format
        request_data = [
            {
                "mime_type": "image/jpeg",  # Adjust based on the image type
                "data": downloaded_file  # Image data (binary)
            },
            {
                "text": "Please analyze the contents of this image"  # Adding text description
            }
        ]
        
        # Send the request to Gemini AI with both image and text
        response = model.generate_content(request_data)
        
        # Extract AI-generated description
        gemini_description = response.text if response else "Could not analyze the file."

    except Exception as e:
        gemini_description = f"Error processing the file: {str(e)}"

    # Store file metadata in MongoDB
    users_collection.update_one(
        {"chat_id": message.chat.id},
        {"$push": {"files": {"file_name": file_name, "description": gemini_description}}}
    )

    print(f"File received: {file_name}, Description: {gemini_description}")
    bot.reply_to(message, f"File received!\n*Gemini AI Analysis:* {gemini_description}")

# Web Search Handler
def perform_web_search(query):
    search_url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={GOOGLE_API_KEY}&cx={CSE_ID}"
    
    try:
        response = requests.get(search_url)
        search_results = response.json()

        if 'items' in search_results:
            results = ""
            for item in search_results['items'][:5]:  # Limit to top 5 results
                title = item.get('title')
                link = item.get('link')
                snippet = item.get('snippet')
                results += f"• {title}\n{snippet}\n{link}\n\n"
            return results if results else "No relevant results found."
        else:
            return "No results found."

    except requests.exceptions.RequestException as e:
        return f"Error fetching search results: {e}"
#start the bit
# bot.polling()
def shutdown_handler(sig, frame):
    print("shutting down bot gracefully..,")
    sys.exit(0)
signal.signal(signal.SIGINT, shutdown_handler)
bot.polling()





       






