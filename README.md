# SeedBot2000
## About
This silly little robot rolls random flagsets for FF6WC, as well as some other fun little extra things. You can see SeedBot in action on the [FF6WC Discord](https://discord.gg/5MPeng5). You can also invite SeedBot to your own server by [clicking here](https://discord.com/api/oauth2/authorize?client_id=892560638969278484&permissions=1494917180496&scope=bot).

This repository contains the unified source code for the SeedBot Discord bot and its companion Django web application.

## Project Overview

This project provides a friendly front-end for the Final Fantasy VI: Worlds Collide randomizer. It consists of three main components running in a unified environment:

1.  **Django Web App:** A web interface for creating, sharing, and rolling game presets. It features a user authentication system, allowing users to register and manage their own presets.
2.  **Discord Bot:** The `seedbot2000` bot, which provides seed rolling and other functionality directly within Discord. It also has capabilities to integrate with Google Sheets for data tracking and other tasks.
3.  **Celery Worker:** A background process that handles long-running tasks like local seed generation.

The project uses a single SQLite database (`seeDBot.sqlite`) that is shared between the web app and the bot.

## Development Setup

These instructions are for setting up a local development environment on Windows.

### Prerequisites
* Python 3.10
* Git
* SQLite Command-Line Tools (must be added to your system's PATH)
* Redis (The recommended way to run Redis on Windows is via WSL)

### 1. Clone the Repository
Clone this repository and its submodules to your local machine.
```
git clone --recurse-submodules https://github.com/your-username/seedbot2000.git seedbot-project
cd seedbot-project
```

### 2. Create the Virtual Environment
Create and activate a Python 3.10 virtual environment.
```
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
Install all required Python packages from the `requirements.txt` file.
```
pip install -r requirements.txt
```

### 4. Create Your `.env` File
Create a file named `.env` in the project root. This file holds your secret keys and should never be committed to Git.

```
SECRET_KEY='your-django-secret-key'
new_api_key='your-wc-api-key'
dev_api_key='your-dev-wc-api-key'
DISCORD_TOKEN='your-discord-bot-token'
ENVIRONMENT='dev'
```

### 5. Set Up the Database
Run the Django migrations to create all the necessary tables in your `seeDBot.sqlite` database.
```
python manage.py migrate
```

### 6. Running the Project
To run the full application for development, you need to have **four** separate terminals open and running simultaneously.

* **Terminal 1: Start Redis**
```
redis-server
```

* **Terminal 2: Start the Celery Worker**
(Make sure your `.venv` is active)
```
celery -A seedbot_project worker -l info --pool=gevent
```

* **Terminal 3: Start the Discord Bot**
(Make sure your `.venv` is active)
```
python manage.py run_bot
```

* **Terminal 4: Start the Django Web Server**
(Make sure your `.venv` is active)
```
python manage.py runserver
```

Once all services are running, you can access the web app at `http://127.0.0.1:8000/`.

## Production Environment

The production environment runs on a Linux (Ubuntu) server.
* The web application is served by **Apache** with `mod_wsgi`.
* The Celery worker and Discord bot are managed as background services using **systemd**.
* All components run from this single, unified repository.

## Bot-Only Development Setup

If you are a contributor working only on the Discord bot, you can use this streamlined setup process. This avoids the need to run the full Django web server and Celery worker.

### Prerequisites
* Python 3.10
* Git

### 1. Clone the Repository
Clone this repository and its submodules to your local machine.
```
git clone --recurse-submodules https://github.com/your-username/seedbot2000.git seedbot-project
cd seedbot-project
```

### 2. Create the Virtual Environment
Create and activate a Python 3.10 virtual environment.
```
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
Install all required Python packages from the `requirements.txt` file.
```
pip install -r requirements.txt
```

### 4. Create Your `.env` File
Create a file named `.env` in the project root. This file holds your secret keys and should never be committed to Git. You only need the `DISCORD_TOKEN` for the bot to run, but the other keys are required by the Django settings.

```
SECRET_KEY='your-django-secret-key'
new_api_key='your-wc-api-key'
dev_api_key='your-dev-wc-api-key'
DISCORD_TOKEN='your-discord-bot-token'
ENVIRONMENT='dev'
```

### 5. Set Up the Database
Run the Django migrations to create all the necessary tables in your `seeDBot.sqlite` database. The bot requires the database to be set up.
```
python manage.py migrate
```

### 6. Running the Bot
You can now run the bot with a single command.
(Make sure your `.venv` is active)
```
python manage.py run_bot
```
The bot should now be online and connected to Discord.
