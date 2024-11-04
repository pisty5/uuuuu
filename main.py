from telethon import TelegramClient, events
import requests
import os

# إعدادات بوت تيليجرام
API_ID = 20061780
API_HASH = "702f62811bfacc405fe497f6f4e78db5"
BOT_TOKEN = "7765417105:AAERz6X9ARg99jI-epPoQIZhcESetx4jQZs"

# إنشاء كائن العميل بدون استدعاء .start() هنا
client = TelegramClient('bot', API_ID, API_HASH)

async def download_video(url, file_name, event):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    downloaded_size = 0
    progress_percent = 0

    if response.status_code == 200:
        with open(file_name, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
                downloaded_size += len(chunk)
                
                # حساب نسبة التقدم
                new_progress = int((downloaded_size / total_size) * 100)
                if new_progress >= progress_percent + 5:
                    progress_percent = new_progress
                    await event.reply(f"جارٍ التحميل... {progress_percent}%")
        
        return file_name
    else:
        return None

async def send_video(event, video_path):
    await client.send_file(event.sender_id, video_path, caption="Here's your video!")
    os.remove(video_path)  # حذف الملف بعد الإرسال

@client.on(events.NewMessage(pattern='/download'))
async def handler(event):
    # الحصول على رابط الفيديو من الرسالة
    command = event.message.text.split()
    if len(command) < 2:
        await event.reply("يرجى توفير رابط الفيديو.")
        return
    
    video_url = command[1]
    video_path = 'downloaded_video.mp4'
    
    # تحميل الفيديو
    await event.reply("جارٍ تحميل الفيديو...")
    video_file = await download_video(video_url, video_path, event)
    
    if video_file:
        await event.reply("تم التحميل، جارٍ إرسال الفيديو...")
        await send_video(event, video_file)
    else:
        await event.reply("فشل في تحميل الفيديو. تأكد من الرابط وحاول مرة أخرى.")

# بدء البوت بعد التهيئة
client.start(bot_token=BOT_TOKEN)
client.run_until_disconnected()
