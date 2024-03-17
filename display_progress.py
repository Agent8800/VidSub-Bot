import asyncio
import os
import sys
import telegram
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.handlers import MessageHandler

# Add the progress_for_pyrogram function from the provided code

async def start_bot():
    global bot
    bot = Client("Burner")

    @bot.on_message(filters.command("progress"))
    async def progress_command(client, message):
        await progress_handler(client, message)

    await bot.start()
    print("Bot started")
    bot.idle()


async def progress_handler(client, message):
    # Define the total size of the task (in bytes)
    total = 1000000

    # Initialize the progress bar
    current = 0
    start = time.time()
    await progress_for_pyrogram(current, total, "Downloading", message, start)

    # Simulate a downloading task
    for i in range(total):
        current = i
        await asyncio.sleep(0.001)

        # Update the progress bar
        await progress_for_pyrogram(current, total, "Downloading", message, start)

    # Task completed
    await message.edit(
        text="**Downloading**\n\n" + PROGRESS.format(
            100,
            humanbytes(total),
            humanbytes(total),
            "0 B/s",
            "0 s"
        ),
        parse_mode='markdown'
    )


if __name__ == "__main__":
    asyncio.run(start_bot()
