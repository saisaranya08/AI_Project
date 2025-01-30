# Telegram Bot with Gemini AI and Web Search Integration

This project is a Telegram bot that integrates with Gemini AI for generating responses, analyzing images/documents, and performing web searches. The bot also interacts with MongoDB to store user data, chat history, and uploaded files. It supports basic user registration, phone number collection, file uploads (images/documents), and web search, leveraging AI for dynamic responses.

## Features

- *User registration*: The bot stores basic user information (first name, username, and phone number).
- *AI-generated responses*: The bot communicates with the Gemini AI to provide intelligent responses based on user input.
- *File uploads*: The bot accepts images and documents from users, analyzes them using Gemini AI, and provides a description of the content.
- *Web search*: The bot can perform web searches based on user input and return search results.
- *MongoDB integration*: All user data, chat history, and file uploads are saved in MongoDB for persistence.

## Prerequisites

Before running the bot, ensure you have the following:

- *Python 3.x*: The bot is developed using Python 3.8+.
- *Telegram Bot Token*: Create a bot on Telegram and get your bot token.
- *MongoDB Atlas Account*: You will need a MongoDB account and URI for storing data.
- *Gemini AI API Key*: Get your Gemini API key for interacting with Gemini AI.
- *Google Custom Search Engine (CSE) API Key and CSE ID*: Get your API key from Google Cloud and your search engine ID from Google Custom Search Engine.

## Setup Instructions

1. *Clone the Repository*:
   ```bash
   git clone <repository-url>
   cd <project-directory>

2. *Install Dependencies*: Install the required Python libraries by running the following command
   pip install -r requirements.txt

3. *Create .env File*: Create a .env file in the root directory of project and add the following environment variables
   TELEGRAM_BOT_TOKEN=<your-telegram-bot-token>
   MONGODB_URI=<your-mongodb-uri>
   GEMINI_API_KEY=<your-gemini-api-key>
   CSE_API_KEY=<your-google-cse-api-key>
   CSE_ID=<your-google-cse-id>

   *Replace <your-telegram-bot-token> with the token you received from the BotFather.
   *Replace <your-mongodb-uri> with the MongoDB URI you obtained from MongoDB Atlas.
   *Replace <your-gemini-api-key> with the Gemini AI API key.
   *Replace <your-google-cse-api-key> with the API key for Google Custom Search Engine.
   *Replace <your-google-cse-id> with the search engine ID from Google Custom Search Engine.

4.  Run the Bot: Start the bot by running:
    Python bot.py

5.  Interacting with the Bot:

Send /start to register a new user.
Share a phone number (via the contact button in Telegram).
Send messages, images, or documents to interact with the bot and receive AI-generated responses and file analysis.
Send a query to perform a web search and receive search results.

## Web Search Feature
The bot can perform a web search using the Google Custom Search Engine API. When a user sends a query (e.g., a question or a keyword), the bot will return the top search results from the web.

**How it Works:
The bot takes user input and sends a request to Google Custom Search Engine.
It uses the API key and CSE ID to retrieve search results.
The bot processes the results and sends a summary to the user.

## Contributing
Feel free to fork this repository and create a pull request with your improvements or fixes.