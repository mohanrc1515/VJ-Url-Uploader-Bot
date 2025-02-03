import os
     import logging
     from telegram import Update
     from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
     import ffmpeg

     # Set up logging
     logging.basicConfig(level=logging.INFO)

     # Telegram bot token (replace with your bot token)
     TOKEN = "7696984863:AAEiUA76NTYiQ2dYlCzxEAaymT_FMnnkKpM"

     async def start(update: Update, context):
         await update.message.reply_text("Welcome! Send me a file, and I'll convert it to a video.")

     async def handle_file(update: Update, context):
         file = await update.message.document.get_file()
         file_path = f"downloads/{update.message.document.file_name}"
         await file.download_to_drive(file_path)

         # Convert file to video
         output_path = f"outputs/{update.message.document.file_name}.mp4"
         (
             ffmpeg
             .input(file_path)
             .output(output_path)
             .run()
         )

         # Send the converted video back to the user
         await update.message.reply_video(video=open(output_path, "rb"))

         # Clean up files
         os.remove(file_path)
         os.remove(output_path)

     if __name__ == "__main__":
         # Create directories if they don't exist
         os.makedirs("downloads", exist_ok=True)
         os.makedirs("outputs", exist_ok=True)

         # Set up the bot
         application = ApplicationBuilder().token(TOKEN).build()

         # Add handlers
         application.add_handler(CommandHandler("start", start))
         application.add_handler(MessageHandler(filters.Document.ALL, handle_file))

         # Start the bot
         application.run_polling()
