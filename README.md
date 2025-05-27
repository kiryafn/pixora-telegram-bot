# 🚀 Pixora — Telegram Job Search Bot

## 📌 Project Overview
**Pixora** is an intelligent Telegram bot designed to simplify job hunting. It automates vacancy searches, filters results based on user preferences, and supports multiple languages for a seamless experience.

### 🔥 Key Features
- **Smart Job Search**: Fetches vacancies from platforms like Pracuj.pl via API/parsing.
- **Custom Filters**: Users set preferences (salary, location, job type).
- **Multi-Language Support**: Ready for EN/PL/UA/RU (easily extendable).
- **User-Friendly**: Inline keyboards, quick actions, and saved searches.

---

## 🧭 Project Structure
```bash
pixora-telegram-bot/
├── bot/                  # Core bot functionality
│   ├── callbacks/        # Callback query handlers
│   ├── configuration/    # Bot configuration files
│   ├── core/             # Core application logic
│   ├── dialogs/          # Conversation handlers
│   ├── exceptions/       # Custom exceptions
│   ├── handlers/         # Message and command handlers
│   ├── keyboards/        # Inline and reply keyboards
│   ├── middlewares/      # Custom middleware stack
│   ├── models/           # Pydantic models and DTOs
│   ├── repositories/     # Database repository pattern
│   ├── scheduler/        # Background tasks and notifications
│   ├── scrapers/         # Job platform scrapers
│   ├── services/         # Business logic layer
│   ├── ui/               # User interface components
│   ├── utils/            # Utility functions
│   └── main.py           # Bot entry point
│
├── data/                 # Data storage
│   ├── img/              # Images
│   └── sql/              # Sql files
│
└── locales/              # Localization files
    ├── en.json           # English translations
    ├── pl.json           # Polish translations
    └── ...               # Other languages          
```
---

## 🧪 Quick Start
### Prerequisites
- Python 3.10+
- PostgreSQL 14+

### Installation
```bash
git clone https://github.com/kiryafn/pixora-telegram-bot.git
cd pixora-telegram-bot
pip install -r requirements.txt


### Environment Variables (`.env`)
```ini
BOT_TOKEN=your_telegram_bot_token
DB_URL=postgresql+asyncpg://user:password@address:port
PROXY_API_KEY=optional_proxy_key
```


---

## ⚙️ Tech Stack
| Category       | Technologies                      |
|----------------|-----------------------------------|
| **Backend**    | Python 3.10, Aiogram 3, AsyncIO   |
| **Scraping**   | Scrapy   |
| **Database**   | PostgreSQL, SQLAlchemy 2.0,       |
| **Architecture** | Finite State Machine, CallbackQuery |

---

## 🌍 Multi-Language Support
- **Add New Language**:  
  Add a JSON file in `locales/` (e.g., `de.json`) with translated keys.
- **Structure Example**:
  ```json
  {
    "welcome": "Willkommen bei Pixora!",
    "search_button": "Jobs suchen"
  }
  ```

---

## 💬 Contribute
- **Pull Requests**: Fork → Branch → Submit PR with a clear description.
- **Issues**: Report bugs/features via GitHub Issues.
---

## 🪪 License
Apache License 2.0. See [LICENSE](LICENSE) for details.
