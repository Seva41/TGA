# Telegram Bot for The Game Awards Predictions

This project is a Telegram bot that allows users to predict winners for each category of The Game Awards. When the show goes live, the admin can select the winners and reward points to each user based on their correct predictions.

## Features

- Allows users to vote for nominees in various categories of The Game Awards.
- Administrators can input the actual winners and calculate points for correct predictions.
- Users can see their selected choices with a visual confirmation.

## Setup

### Prerequisites

- Python 3.x
- `python-telegram-bot` library
- `python-dotenv` library for environment variable management

### Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/Seva41/TGA_bot
   cd TGA_bot

   ```

2. **Install Required Packages:**

   ```bash
   pip install python-telegram-bot python-dotenv

   ```

3. **Setting Up the Telegram Bot:**

   - Create a bot in Telegram using BotFather and get the bot token.
   - Add the bot token to your .env file as TELEGRAM_TOKEN=your_bot_token.

4. **Initialize the Database:**

   - The bot uses SQLite to manage data. Ensure that the SQLite database is set up as per the script.

5. **Running the Bot:**
   ```bash
   python bot_tga.py
   ```

### Usage

After starting the bot, users can interact with it to make their predictions for each category. The bot will guide through each category sequentially.

### Contributing

Contributions to this project are welcome. Please fork the repository and submit a pull request with your changes.

### License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.
