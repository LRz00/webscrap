![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Selenium](https://img.shields.io/badge/-selenium-%43B02A?style=for-the-badge&logo=selenium&logoColor=white) ![Apache Kafka](https://img.shields.io/badge/Apache%20Kafka-000?style=for-the-badge&logo=apachekafka) ![Discord](https://img.shields.io/badge/Discord-%235865F2.svg?style=for-the-badge&logo=discord&logoColor=white) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)

# Amazon Wishlist Tracker

A **web scraper + Kafka messaging pipeline** that monitors a **public Amazon wishlist** and sends price data to a Kafka topic, enabling **price fluctuation alerts** via Discord.

<img width="601" height="610" alt="python alert drawio" src="https://github.com/user-attachments/assets/e2e366ce-d031-4338-8d15-053583d62a21" />

## Features

- 🕷️ **Web Scraping** — Uses Selenium + BeautifulSoup to extract product names and prices from Amazon wishlists
- 📨 **Kafka Pipeline** — Publishes scraped data to a Kafka topic for real-time processing
- 💾 **Price History** — Stores prices in PostgreSQL to track changes over time
- 🔔 **Discord Alerts** — Sends notifications when prices change by more than 5%
- 🐳 **Docker Ready** — Full Docker Compose setup with Kafka, Zookeeper, Kafdrop, and PostgreSQL

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Scraper   │────▶│    Kafka    │────▶│  Consumer   │────▶│   Discord   │
│  (Selenium) │     │   Topic     │     │  + Postgres │     │    Bot      │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

## Prerequisites

- Python 3.12+
- Docker & Docker Compose
- Chrome/Chromium (for Selenium)
- Discord Bot Token

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/LRz00/webscrap.git
cd webscrap
```

### 2. Create and activate virtual environment

```bash
python -m venv env
source env/bin/activate  # Linux/macOS
# or: env\Scripts\activate  # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the application

Copy the example config and fill in your values:

```bash
cp src/configs/config\ _example.py src/configs/config.py
```

Edit `src/configs/config.py`:

```python
config = {
    "wishlist_url": "https://www.amazon.com.br/hz/wishlist/ls/YOUR_WISHLIST_ID",
    "kafka_broker": "kafka:9092",
    "kafka_topic": "wishlist_prices",
    "redis_port": 6379,
    "redis_host": "localhost",
    "discord_token": "YOUR_DISCORD_BOT_TOKEN",
    "discord_server": YOUR_DISCORD_CHANNEL_ID,
    "database_url": "postgresql://appuser:apppassword@localhost:5432/appdb"
}
```

### 5. Start infrastructure with Docker

```bash
docker-compose up -d
```

This starts:
- **Zookeeper** — Kafka coordination
- **Kafka** — Message broker (port 9092)
- **Kafdrop** — Kafka UI (http://localhost:19000)
- **PostgreSQL** — Price history database (port 5432)

## Usage

### Run the scraper (producer)

```bash
python -m src.main
```

This scrapes the wishlist and publishes data to the Kafka topic.

### Run the consumer

```bash
python -m src.kafka.consumer
```

This listens for messages, stores prices in PostgreSQL, and sends Discord alerts when prices change significantly.

## Project Structure

```
webscrap/
├── src/
│   ├── main.py                 # Entry point - runs scraper + producer
│   ├── configs/
│   │   ├── config.py           # Configuration (gitignored)
│   │   └── config _example.py  # Example configuration
│   ├── db/
│   │   └── db.py               # SQLAlchemy database engine
│   ├── kafka/
│   │   ├── producer.py         # Publishes to Kafka topic
│   │   └── consumer.py         # Consumes and processes messages
│   ├── notifier/
│   │   └── discord_notifier_bot.py  # Discord notifications
│   └── scrapper/
│       └── wishlist_scrapper.py     # Selenium scraper
├── tests/                      # Unit tests
├── docker-compose.yml          # Infrastructure setup
├── init.sql                    # Database schema
└── requirements.txt            # Python dependencies
```

## Database Schema

```sql
CREATE TABLE price_history (
    id SERIAL PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Running Tests

```bash
pytest tests/ -v
```

## Configuration Options

| Key | Description |
|-----|-------------|
| `wishlist_url` | Public Amazon wishlist URL |
| `kafka_broker` | Kafka bootstrap server |
| `kafka_topic` | Topic name for price updates |
| `discord_token` | Discord bot authentication token |
| `discord_server` | Discord channel ID for alerts |
| `database_url` | PostgreSQL connection string |

## Discord Bot Setup

1. Create a bot at [Discord Developer Portal](https://discord.com/developers/applications)
2. Enable required intents and get the bot token
3. Invite the bot to your server with message permissions
4. Copy the channel ID where alerts should be sent

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
