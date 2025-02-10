# Kaffuchino Gemini Telegram Bot

This Python Telegram bot, powered by the Kaffuchino framework, leverages Google's Gemini AI to provide intelligent conversational capabilities, task automation, and seamless access to information within Telegram.

**Key Features:**

*   **Gemini AI Integration:** Utilizes Google's Gemini AI for advanced natural language understanding and generation.
*   **Intelligent Responses:** Provides context-aware and engaging responses to user input.
*   **Task Automation:** Enables automation of various tasks within Telegram.
*   **Information Access:** Offers easy access to information directly within chats.
*   **Multi-Modal Support:** Processes images with captions to generate relevant responses.
*   **User Authentication** Secure your bot by configuring `AUTHORIZED_USERS` in the `.env` file.
*   **Easy to Use:** Simple commands like `/start` and `/help` provide access to core functionalities.

## Requirements

*   Python 3.11+
*   Telegram Bot API token (obtained from [@BotFather](https://t.me/BotFather))
*   Google Gemini API key (obtained from [Google AI Studio](https://makersuite.google.com/))
*   `python-dotenv` package for environment variables

**Setup Instructions:**

1.  **Clone the repository:**

    ```bash
    git clone [https://github.com/LoboGuardian/kaffuchino-gemini-telegram-bot.git](https://www.google.com/search?q=https://github.com/LoboGuardian/kaffuchino-gemini-telegram-bot.git)  # Replace with your repo URL
    cd kaffuchino-gemini-telegram-bot
    ```

2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Create a `.env` file:**  Copy the example `.env_example` file or create a new one in the project root and add the following environment variables:

    ```
    # Telegram bot token from BotFather (https://t.me/botfather)
    BOT_TOKEN=1224567:xxxxxxxxxxxxxxxxxxxxxxxx (YOUR_TELEGRAM_BOT_TOKEN)

    # Google Gemini API key https://makersuite.google.com/ (free)
    GOOGLE_API_KEY=xxxxxxxxxxxxxxxxxx (YOUR_GOOGLE_GEMINI_API_KEY)
    
    # Authorized Users: Comma seperated values of either Telegram username or user id. To restrict public access of the bot
    AUTHORIZED_USERS=comma_separated_user_ids_or_usernames
    # e.g., 1234567890,anotheruser

    ```

4.  **Run the bot:**

    ```bash
    python bot.py
    ```

## Getting Started

1.  Run the bot using the command above.
2.  Open your Telegram app and search for your bot's username.
3.  Send a message to the bot to start interacting.

## Bot Commands

| Command | Description                               |
| ------- | ----------------------------------------- |
| `/start` | Greet the bot and get started.          |
| `/help`  | Get information about the bot's capabilities. |
| `/new`   | Start a new chat session (if implemented). |

## Project Structure

```
kaffuchino-gemini-telegram-bot/
├── gemini/                # Main bot module
│   ├── init.py
│   ├── bot.py             # Main bot logic
│   ├── api.py             # Gemini API interaction
│   ├── filters.py         # Message filters and middleware
│   ├── handlers.py        # Command and event handlers
│   ├── parser.py          # Text processing
│   ├── config.py          # Configuration and environment variables
├── .env                   # Environment variables (BOT_TOKEN, API_KEY, etc.)
├── .gitignore             # Git ignore file
├── logs/                  # Log files
│   ├── app.log
├── data/                  # Data storage (if needed)
├── requirements.txt       # Project dependencies
├── Dockerfile             # Dockerfile (for containerization)
├── LICENSE                # License file
├── README.md              # This file
```
## Docker Support

You can containerize and run the bot using Docker.

1.  **Build the image:**

    ```bash
    docker build -t kaffuchino .
    ```

2.  **Run the container:**

    ```bash
    docker run -d --name kaffuchino kaffuchino
    ```

3.  **View logs:**

    ```bash
    docker logs -f kaffuchino
    ```

4.  **Stop and remove the container:**

    ```bash
    docker stop kaffuchino
    docker rm kaffuchino
    ```

## Troubleshooting Docker

*   **Verify container status:** `docker ps`
*   **Force execution (for testing):**  `docker exec -it kaffuchino bash` then `python main.py` inside the container.
*   **Rebuild image without cache:** `docker build --no-cache -t kaffuchino .`

## Contributions

Contributions are welcome! Please fork the repository and submit pull requests.

## Disclaimer

This bot is still under development.  Responses may sometimes be inaccurate or inappropriate. Use responsibly.

### Star History

<a href="https://star-history.com/#LoboGuardian/kaffuchino-gemini-telegram-bot&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=LoboGuardian/kaffuchino-gemini-telegram-bot&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=LoboGuardian/kaffuchino-gemini-telegram-bot&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=LoboGuardian/kaffuchino-gemini-telegram-bot&type=Date" />
  </picture>
</a>