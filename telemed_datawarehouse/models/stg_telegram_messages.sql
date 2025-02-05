-- models/stg_telegram_messages.sql
WITH raw_data AS (
    SELECT
        channel_title,
        channel_username,
        message_id,
        message,
        message_date,
        media_path
    FROM raw.telegram_messages
)
SELECT
    channel_title,
    channel_username,
    message_id,
    TRIM(message) AS cleaned_message,  -- Remove leading/trailing spaces
    message_date,
    media_path
FROM raw_data
WHERE message IS NOT NULL  -- Remove rows with null messages