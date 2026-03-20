# Redis-PubSub-Chat

A real-time, terminal-based chat application built with Python. This project demonstrates distributed system design principles by utilizing **Redis** as a centralized message broker and implementing the **Publisher/Subscriber (Pub/Sub)** messaging paradigm.

## System Architecture & Design

This application avoids peer-to-peer complexity by relying on a central, in-memory data store to route messages to multiple connected clients instantly. 

### Core Concepts Applied
* **The Pub/Sub Pattern:** Senders (Publishers) are decoupled from receivers (Subscribers). Publishers simply push data to a "channel," and the broker handles routing that data to anyone actively listening to that channel.
* **Cloud-Native Infrastructure:** Configured to connect to a managed Cloud Redis database rather than `localhost`. This solves the "Localhost Trap," allowing users on entirely different networks to communicate globally.
* **Asynchronous I/O via Threading:** Terminal interfaces face a "Blocking I/O" problem—waiting for user keyboard input halts the execution of the program, preventing the app from receiving incoming network messages. This system solves that by utilizing Python's `threading` module:
    * **Main Thread (Publisher):** Handles the blocking user input and publishes payloads to Redis.
    * **Daemon Thread (Subscriber):** Runs completely in the background, maintaining an open TCP socket to listen for incoming Redis broadcasts without interrupting the user's typing.


## Prerequisites

Before you begin, ensure you have the following:
1. **Python 3.x** installed on your machine.
2. **Git** installed for version control.
3. **A Redis Database URL**. You can run Redis locally via Docker, but for global multiplayer chat, a free cloud database is recommended (see Step 1 below).

---

## Installation & Setup

### Step 1: Claim a Free Cloud Redis Database
If you do not already have a Redis server running:
1. Go to [Upstash](https://upstash.com/) and create a free account.
2. Click **Create Database** (Name it `redis-chat`, choose a region near you).
3. Scroll down to the **Connect** section and copy your **Endpoint**, **Port**, and **Password**.

### Step 2: Clone the Repository
Open your terminal and pull down the code:
```bash
git clone https://github.com/YOUR_USERNAME/redis-pubsub-chat.git
cd redis-pubsub-chat
```

### Step 3: Set Up the Virtual Environment
It is highly recommended to run this inside an isolated virtual environment.

**For Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```
*(Note for Ubuntu/Linux Mint users: If the command above fails or creates an empty folder, run `sudo apt update && sudo apt install python3-venv` first, delete the broken `venv` folder, and try again).*

**For Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

### Step 4: Install Dependencies
With your virtual environment active `(venv)`, install the required Python libraries:
```bash
pip install -r requirements.txt
```

### Step 5: Configure Security and Credentials
You must securely provide your database credentials to the application without hardcoding them into the scripts.

1. Create a file named exactly `.env` in the root folder.
2. Add your Upstash (or local Redis) credentials to the file in this format:

```env
REDIS_HOST=your-upstash-endpoint.upstash.io
REDIS_PORT=your-port-number
REDIS_PASSWORD=your-secure-password
```
*(Note: Ensure `.env` is listed in your `.gitignore` file so you do not accidentally publish your password to the internet!)*

---

## Usage

1. Ensure your virtual environment is active.
2. Run the main client script:
```bash
python src/chat_client.py
```
3. Enter your desired **username**.
4. Enter the **channel** you wish to join (e.g., `general`, `gaming`, `dev-talk`).
5. **Chat!** Anyone else running this script connected to the same database can