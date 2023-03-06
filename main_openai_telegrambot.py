import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import openai

openai.api_key = ""

class Conversation:
    def __init__(self):
        self.history = []
        self.current_prompt = ""

    def add_message(self, message):
        self.history.append(message)

    def get_prompt(self):
        prompt = "Conversation with a user:\n"
        for i, message in enumerate(self.history):
            prompt += f"User {i+1}: {message}\nAI {i+1}:"
        self.current_prompt = prompt
        return prompt

def generate_answer(conversation):
    prompt = conversation.get_prompt()
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=1,
        max_tokens=2048,
        n=1,
        stop=None,
    )
    message = response.choices[0].text.strip()
    return message

def handle_message(update, context):
    user_text = update.message.text
    chat_id = update.effective_chat.id
    if chat_id not in context.chat_data:
        context.chat_data[chat_id] = Conversation()
    conversation = context.chat_data[chat_id]
    conversation.add_message(user_text)
    response_text = generate_answer(conversation)
    for i in range(0, len(response_text), 4096):
        bot.send_message(chat_id=chat_id, text=response_text[i:i+4096])
        

if __name__ == '__main__':
    telegram_bot_token = ''
    bot = telegram.Bot(token=telegram_bot_token)
    updater = Updater(token=telegram_bot_token, use_context=True)
    dispatcher = updater.dispatcher
    message_handler = MessageHandler(Filters.text, handle_message, pass_chat_data=True)
    dispatcher.add_handler(message_handler)
    updater.start_polling()
    updater.idle()
