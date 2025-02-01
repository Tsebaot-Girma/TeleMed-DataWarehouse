import logging
from telethon import TelegramClient
import csv
import os
import json
from dotenv import load_dotenv

# Set up logging
os.makedirs("../log", exist_ok=True)  # Create log directory if it doesn't exist
logging.basicConfig(
    filename='../log/scraping.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Load environment variables
load_dotenv('../.env')  # Load .env file from the project root
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
phone = os.getenv('PHONE_NUMBER')

# Function to read channels from a JSON file
def load_channels_from_json(file_path):
    """Load the list of Telegram channels to scrape from a JSON file."""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            return data.get('channels', []), data.get('comments', [])
    except Exception as e:
        logging.error(f"Error reading channels from JSON: {e}")
        return [], []

# Function to scrape data from a single channel
async def scrape_channel(client, channel_username, writer, media_dir):
    """Scrape all messages and media from a Telegram channel."""
    try:
        entity = await client.get_entity(channel_username)
        channel_title = entity.title
        
        message_count = 0
        async for message in client.iter_messages(entity):
            media_path = None
            if message.media:
                # Generate a unique filename for the media file
                filename = f"{channel_username}_{message.id}.{message.media.document.mime_type.split('/')[-1]}" if hasattr(message.media, 'document') else f"{channel_username}_{message.id}.jpg"
                media_path = os.path.join(media_dir, filename)
                await client.download_media(message.media, media_path)
                logging.info(f"Downloaded media for message ID {message.id}.")
            
            # Write message details to CSV
            writer.writerow([channel_title, channel_username, message.id, message.message, message.date, media_path])
            logging.info(f"Processed message ID {message.id} from {channel_username}.")
            
            message_count += 1

        if message_count == 0:
            logging.info(f"No messages found for {channel_username}.")
        else:
            logging.info(f"Scraped {message_count} messages from {channel_username}.")

    except Exception as e:
        logging.error(f"Error while scraping {channel_username}: {e}")

# Initialize the Telegram client
client = TelegramClient('scraping_session', api_id, api_hash)

async def main():
    """Main function to scrape data from multiple Telegram channels."""
    try:
        await client.start(phone)
        logging.info("Client started successfully.")
        
        # Create data directory if it doesn't exist
        data_dir = '../data'
        os.makedirs(data_dir, exist_ok=True)
        
        # Directory to store downloaded media files
        media_dir = os.path.join(data_dir, 'photos')
        os.makedirs(media_dir, exist_ok=True)

        # Open CSV file to store scraped data
        csv_file_path = os.path.join(data_dir, 'scraped_data.csv')
        with open(csv_file_path, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Write header row if the file is empty
            if file.tell() == 0:
                writer.writerow(['Channel Title', 'Channel Username', 'ID', 'Message', 'Date', 'Media Path'])
            
            # Load channels from JSON file
            channels, comments = load_channels_from_json('channels.json')
            
            # Scrape data from each channel
            for channel in channels:
                await scrape_channel(client, channel, writer, media_dir)
                logging.info(f"Finished scraping data from {channel}.")

        # Log commented channels if needed
        if comments:
            logging.info(f"Commented channels: {', '.join(comments)}")

    except Exception as e:
        logging.error(f"Error in main function: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())