import os
import logging
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import pandas as pd

# Ensure logs folder exists
os.makedirs("../log", exist_ok=True)  # Create log directory if it doesn't exist

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("../log/database_setup.log", encoding='utf-8'),  # Log to file with UTF-8 encoding
        logging.StreamHandler()  # Log to console
    ]
)

# Load environment variables
load_dotenv('../.env')  # Load .env file from the project root

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")

def get_db_connection():
    """Create and return a database connection."""
    try:
        DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        engine = create_engine(DATABASE_URL)
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))  # Test connection
        logging.info("[SUCCESS] Successfully connected to the PostgreSQL database.")
        return engine
    except Exception as e:
        logging.error(f"[ERROR] Database connection failed: {e}")
        raise

def create_table(engine):
    """Create the telegram_messages table if it doesn't exist."""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS telegram_messages (
        id SERIAL PRIMARY KEY,
        channel_title TEXT,
        channel_username TEXT,
        message_id BIGINT UNIQUE,
        message TEXT,
        message_date TIMESTAMP,
        media_path TEXT
    );
    """
    try:
        with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as connection:
            connection.execute(text(create_table_query))
        logging.info("[SUCCESS] Table 'telegram_messages' created successfully.")
    except Exception as e:
        logging.error(f"[ERROR] Error creating table: {e}")
        raise

def clean_data(df):
    """Clean and transform the scraped data."""
    try:
        # Verify that the required columns exist
        required_columns = ['Channel Title', 'Channel Username', 'ID', 'Message', 'Date', 'Media Path']
        for column in required_columns:
            if column not in df.columns:
                raise KeyError(f"Missing required column: {column}")

        # Rename columns to match the database schema
        df = df.rename(columns={
            'Channel Title': 'channel_title',
            'Channel Username': 'channel_username',
            'ID': 'message_id',
            'Message': 'message',
            'Date': 'message_date',
            'Media Path': 'media_path'
        })

        # Remove duplicates based on message_id
        df = df.drop_duplicates(subset=['message_id'], keep='first')

        # Handle missing values
        df['message'] = df['message'].fillna('')  # Replace missing messages with empty string
        df['media_path'] = df['media_path'].fillna('')  # Replace missing media paths with empty string

        # Standardize date format (if needed)
        df['message_date'] = pd.to_datetime(df['message_date'], errors='coerce')  # Convert to datetime

        logging.info("[SUCCESS] Data cleaning and transformation completed.")
        return df
    except Exception as e:
        logging.error(f"[ERROR] Error cleaning data: {e}")
        raise

def insert_data(engine, cleaned_df):
    """Insert cleaned Telegram data into the PostgreSQL database."""
    try:
        # Convert NaT timestamps to None (NULL in SQL)
        cleaned_df["message_date"] = cleaned_df["message_date"].apply(lambda x: None if pd.isna(x) else str(x))

        insert_query = """
        INSERT INTO telegram_messages 
        (channel_title, channel_username, message_id, message, message_date, media_path) 
        VALUES (:channel_title, :channel_username, :message_id, :message, :message_date, :media_path)
        ON CONFLICT (message_id) DO NOTHING;
        """

        with engine.begin() as connection:  # Auto-commit enabled
            for _, row in cleaned_df.iterrows():
                logging.info(f"Inserting: {row['message_id']} - {row['message_date']}")
                connection.execute(
                    text(insert_query),
                    {
                        "channel_title": row["channel_title"],
                        "channel_username": row["channel_username"],
                        "message_id": row["message_id"],
                        "message": row["message"],
                        "message_date": row["message_date"],
                        "media_path": row["media_path"]
                    }
                )

        logging.info(f"[SUCCESS] {len(cleaned_df)} records inserted into PostgreSQL database.")
    except Exception as e:
        logging.error(f"[ERROR] Error inserting data: {e}")
        raise

if __name__ == "__main__":
    # Connect to the database
    engine = get_db_connection()

    # Create the telegram_messages table
    create_table(engine)

    # Load scraped data from CSV
    scraped_data_path = "../data/scraped_data.csv"  # Path to scraped data
    try:
        scraped_data = pd.read_csv(scraped_data_path)
        logging.info(f"[SUCCESS] Loaded scraped data from {scraped_data_path}.")
    except Exception as e:
        logging.error(f"[ERROR] Error loading scraped data: {e}")
        raise

    # Clean and transform the data
    cleaned_data = clean_data(scraped_data)

    # Insert data into the database
    insert_data(engine, cleaned_data)