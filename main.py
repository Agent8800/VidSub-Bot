import asyncio
import os
import tempfile
import time
import math
from pathlib import Path
from pyrogram import Client
from pyrogram.types import Message
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

# Initialize the Pyrogram client with your bot token, API ID, and hash
app = Client(
    "bot",
    bot_token="6449794069:AAEDnBQ2aNhFkNSz1g2zi52nhkDkoLu3soU",
    api_id=7391573,  # Your API ID
    api_hash="1f20df54dfd91bcee05278d3b01da2c7"
)

# Define the progress_for_burning_subtitles function
async def progress_for_burning_subtitles(current, total, message, start):
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)

        progress = "[{0}{1}] \n".format(
            ''.join(["●" for i in range(math.floor(percentage / 5))]),
            ''.join(["○" for i in range(20 - math.floor(percentage / 5))])
        )

        tmp = progress + PROGRESS.format(
            round(percentage, 2),
            humanbytes(current),
            humanbytes(total),
            humanbytes(speed),
            estimated_total_time if estimated_total_time != '' else "0 s"
        )
        try:
            await message.edit(
                text="**Burning subtitles**\n\n {}".format(
                    tmp
                ),
                parse_mode='markdown'
            )
        except:
            pass

# Define the handle_subtitle_video function
async def handle_subtitle_video(message: Message):
    user = message.from_user
    chat_id = user.id

    # Get the video and subtitle text from the message
    video_file = message.video
    video_path = video_file.file_id
    subtitle_text = message.text.split(" ", maxsplit=1)[1]

    # Download the video file
    video_file_path = await app.download_media(video_path)

    # Define optional parameters
    font_path = None
    font_size = 30
    color = "white"
    start_time = 0
    duration = None

    # Burn subtitles into the video
    output_path = Path(tempfile.gettempdir()) / f"processed_{video_file.file_id}.mp4"
    
    clip = VideoFileClip(str(video_file_path))
    txt_clip = TextClip(subtitle_text, fontsize=font_size, color=color, font=font_path).set_position(('center', 'bottom')).set_duration(clip.duration)
    final_clip = CompositeVideoClip([clip, txt_clip])
    final_clip.write_videofile(str(output_path))

    # Send the processed video back to the user
    await app.send_video(chat_id=chat_id, video=str(output_path), caption="Processed video")

    # Remove the temporary files
    os.remove(video_file_path)
    os.remove(output_path)

# Register the handle_subtitle_video function as a message handler
app.on_message(handle_subtitle_video)

# Start the Pyrogram client
app.run()
