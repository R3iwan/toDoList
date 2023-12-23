import telebot, os
from telebot import types
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

tasks = {}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "Welcome to the To-Do List Bot!\n"
        "You can add tasks to your to-do list by typing /add <task>\n"
        "To view your tasks, type /list\n"
        "To remove a task, type /remove <task_number>"
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(commands=['add'])
def add_task(message):
    try:
        task = message.text.split("/add ")[1]
        user_id = message.from_user.id

        if user_id not in tasks:
            tasks[user_id] = []

        tasks[user_id].append(task)
        bot.reply_to(message, f'Task "{task}" added to your to-do list.')

    except IndexError:
        bot.reply_to(message, 'Please provide a task to add.')

@bot.message_handler(commands=['list'])
def list_tasks(message):
    user_id = message.from_user.id

    if user_id in tasks and tasks[user_id]:
        task_list = "\n".join([f"{i+1}. {task}" for i, task in enumerate(tasks[user_id])])
        bot.reply_to(message, f'Your to-do list:\n{task_list}')
    else:
        bot.reply_to(message, 'Your to-do list is empty.')

@bot.message_handler(commands=['remove'])
def remove_task(message):
    try:
        task_number = int(message.text.split("/remove ")[1]) - 1
        user_id = message.from_user.id

        if user_id in tasks and 0 <= task_number < len(tasks[user_id]):
            removed_task = tasks[user_id].pop(task_number)
            bot.reply_to(message, f'Task "{removed_task}" removed from your to-do list.')
        else:
            bot.reply_to(message, 'Invalid task number. Please check your to-do list using /list.')

    except (IndexError, ValueError):
        bot.reply_to(message, 'Please provide a valid task number to remove.')

if __name__ == "__main__":
    bot.polling(none_stop=True)
