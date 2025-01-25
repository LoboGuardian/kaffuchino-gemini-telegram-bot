# kaffuchino-gemini-telegram-bot

This is a Python Telegram bot powered by the Kaffuchino framework, enhanced with Google's Gemini AI. This bot provides intelligent conversational capabilities, task automation, and seamless access to information within the Telegram app.

**Key Features:**

*   Leverages Google's Gemini AI for advanced natural language understanding.
*   Offers intelligent and context-aware responses.
*   Enables task automation and streamlined workflows.
*   Provides easy access to information directly from your chats.
* Easy to use with simple commands:
    * `/start`: Greet the bot and get started.
    * `/help`: Get information about the bot's capabilities.
* Send any text message to trigger the generation process.
* Send any image with captions to generate responses based on the image. (Multi-modal support)
* User authentication to prevent unauthorized access by setting `AUTHORIZED_USERS` in the `.env` file (optional).

**Requirements:**
* Python 3.10+
* Telegram Bot API token
* Google `gemini` API key
* dotenv (for environment variables)

**Setup Instructions:**

1. Clone this repository.
2. Install the required dependencies:
    * `pipenv install` (if using pipenv)
    * `pip install -r requirements.txt` (if not using pipenv)
3. Create a `.env` file and add the following environment variables:
    * `BOT_TOKEN`: Your Telegram Bot API token. You can get one by talking to [@BotFather](https://t.me/BotFather).
    * `GOOGLE_API_KEY`: Your Google Bard API key. You can get one from [Google AI Studio](https://makersuite.google.com/).
    * `AUTHORIZED_USERS`: A comma-separated list of Telegram usernames or user IDs that are authorized to access the bot. (optional) Example value: `1234567890, 1234567890`
4. Run the bot:
    * `pipenv run python main.py` (if using pipenv)
    * `python main.py` (if not using pipenv)

**Getting Started:**

1. Start the bot by running the script.
   ```shell
   pipenv run python main.py
   ```
   or
   ```shell
   python main.py
   ```
2. Open the bot in your Telegram chat.
3. Send any text message to the bot.
4. The bot will generate creative text formats based on your input and stream the results back to you.
5. If you want to restrict public access to the bot, you can set `AUTHORIZED_USERS` in the `.env` file to a comma-separated list of Telegram user IDs. Only these users will be able to access the bot.
    Example:
    ```shell
    AUTHORIZED_USERS=1234567890, 1234567890
    ```

### Bot Commands

| Command | Description |
| ------- | ----------- |
| `/start` | Greet the bot and get started. |
| `/help` | Get information about the bot's capabilities. |
| `/new` | Start a new chat session. |

### Star History

<a href="https://star-history.com/#LoboGuardian/kaffuchino-gemini-telegram-bot&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=LoboGuardian/kaffuchino-gemini-telegram-bot&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=LoboGuardian/kaffuchino-gemini-telegram-bot&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=LoboGuardian/kaffuchino-gemini-telegram-bot&type=Date" />
  </picture>
</a>

**Contributions:**

We welcome contributions to this project. Please feel free to fork the repository and submit pull requests.

### Disclaimer

This bot is still under development and may sometimes provide nonsensical or inappropriate responses. Use it responsibly and have fun!

### License

This project is released under the **MIT License**. See the LICENSE file for more details.
