import os
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import openai

def start(update, context):
    """
    Send a welcome message when the '/start' command is issued.
    """
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi there, I'm Mishi. I am a ChatGpt bot made by Hemcker Mufid. How may I assist you?", reply_markup=telegram.ReplyKeyboardRemove())

def handle_message(update, context):
    """
    Generate a response to user message using OpenAI's GPT-4.
    """
    message = update.message.text

    # Generate a response using OpenAI's GPT-4 API
    response = openai.Completion.create(
        engine="davinci-instruct-beta",
        prompt=message,
        max_tokens=8000,
        temperature=0.7,
        top_p=0.9,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    # Send the response to the user
    response_text = response.choices[0].text
    context.bot.send_message(chat_id=update.effective_chat.id, text=response_text)


def handle_group_message(update, context):
    """
    Generate a response to group message using OpenAI's GPT-4.
    """
    message = update.message.text

    # Generate a response using OpenAI's GPT-4 API
    response = openai.Completion.create(
        engine="davinci-instruct-beta",
        prompt=message,
        max_tokens=8000,
        temperature=0.7,
        top_p=0.9,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    # Send the response to the group
    response_text = response.choices[0].text
    context.bot.send_message(chat_id=update.message.chat_id, text=response_text)

# Define command handler for '/chat'
def chat(update, context):
    """
    Enable bot to chat with users in Telegram groups.
    """
    context.bot.send_message(chat_id=update.effective_chat.id, text="I am now chatting in this group! Say hi to me :)")

# Define command handler for '/image'
def image(update, context):
    """
    Generate an image based on user prompt.
    """
    prompt = update.message.text.replace('/image','').strip()
    response = openai.Image.create(
        prompt=prompt,
        size='512x512',
        response_format='url'
    )
    response_url = response['url']

    context.bot.send_photo(chat_id=update.effective_chat.id, photo=response_url)

def main():
    """
    Main function to start the Telegram bot.
    """
    updater = Updater(token=os.getenv("TELEGRAM_API_TOKEN"), use_context=True)
    dp = updater.dispatcher

    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Register command handler for '/start'
    dp.add_handler(CommandHandler("start", start))

    # Register message handlers for user and group messages
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command & Filters.private, handle_message))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command & Filters.group, handle_group_message))

    # Register command handlers for '/chat' and '/image'
    dp.add_handler(CommandHandler("chat", chat))
    dp.add_handler(CommandHandler("image", image))

    # Start the bot
    updater.start_polling()
   
    updater.idle()

if __name__ == '__main__':
    print('Starting Mishi...')
    main()

print('Mishi is now offline.')
