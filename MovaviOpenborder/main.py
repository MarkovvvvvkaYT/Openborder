from telebot import types, telebot
import sqlite3
from config import TOKEN, ADMINS
from user import User, create_table

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    create_table()
    keyboard = telebot.types.InlineKeyboardMarkup()
    User.add_user(message.chat.id)
    if User.get_role_by_id(message.chat.id) != 'teacher' and User.get_role_by_id(message.chat.id) != 'tutor' and User.get_role_by_id(message.chat.id) == None:
        tutor = telebot.types.InlineKeyboardButton('Я куратор', callback_data="tutor")
        teacher = telebot.types.InlineKeyboardButton('Я преподаватель', callback_data="teacher")
        keyboard.add(tutor, teacher)
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!\nКто вы?', reply_markup=keyboard)
    else:
        if User.get_role_by_id(message.chat.id) == 'teacher':

            partners = telebot.types.InlineKeyboardButton('Партнеры', callback_data="partners_teacher")
            motivation = telebot.types.InlineKeyboardButton('Мотивация', callback_data="motivation") 
            course_card = telebot.types.InlineKeyboardButton('Карта курсов', callback_data="course_card")

            about_us = telebot.types.InlineKeyboardButton('О компании', url='https://youtu.be/dQw4w9WgXcQ?si=SvqZnOWFu5bQp9h9')
            methods = telebot.types.InlineKeyboardButton('Метод работа', url='https://youtu.be/dQw4w9WgXcQ?si=SvqZnOWFu5bQp9h9')
            structure = telebot.types.InlineKeyboardButton('Структура (Кто? Где? Когда?)', url='https://youtu.be/dQw4w9WgXcQ?si=SvqZnOWFu5bQp9h9')

            keyboard.add(partners, motivation, course_card, about_us, methods, structure)
            bot.send_message(message.chat.id, '⬇️ Выберите действие', reply_markup=keyboard)
        elif User.get_role_by_id(message.chat.id) == 'tutor':

            instructions_and_regulations = telebot.types.InlineKeyboardButton('Инструкции и регламенты', callback_data="instructions_and_regulations")
            сourse_card = telebot.types.InlineKeyboardButton('Карта курсов', callback_data="сourse_card")
            partners = telebot.types.InlineKeyboardButton('Партнеры', callback_data="partners_tutor")
            motivation = telebot.types.InlineKeyboardButton('Мотивация', callback_data="motivation")
            axo = telebot.types.InlineKeyboardButton('АХО', callback_data="axo")

            structure_question = telebot.types.InlineKeyboardButton('Инструкции и регламенты', url='https://youtu.be/dQw4w9WgXcQ?si=SvqZnOWFu5bQp9h9')
            about_company = telebot.types.InlineKeyboardButton('О компании', url='https://youtu.be/dQw4w9WgXcQ?si=SvqZnOWFu5bQp9h9')

            keyboard.add(about_company, instructions_and_regulations, сourse_card, motivation)
            bot.send_message(message.chat.id, '⬇️ Выберите действие', reply_markup=keyboard)
        
@bot.callback_query_handler(func=lambda callback: True)
def handle_callback(callback):
    if callback.data == 'teacher' or callback.data == 'tutor':
        User.add_role_to_user(callback.message.chat.id, callback.data)
        keyboard = telebot.types.InlineKeyboardMarkup()
        if User.get_role_by_id(callback.message.chat.id) == 'teacher':
            partners = telebot.types.InlineKeyboardButton('Партнеры', callback_data="partners_teacher")
            motivation = telebot.types.InlineKeyboardButton('Мотивация', callback_data="motivation") 
            course_card = telebot.types.InlineKeyboardButton('Карта курсов', callback_data="course_card")

            about_us = telebot.types.InlineKeyboardButton('О компании', url='https://youtu.be/dQw4w9WgXcQ?si=SvqZnOWFu5bQp9h9')
            methods = telebot.types.InlineKeyboardButton('Метод работа', url='https://youtu.be/dQw4w9WgXcQ?si=SvqZnOWFu5bQp9h9')
            structure = telebot.types.InlineKeyboardButton('Структура (Кто? Где? Когда?)', url='https://youtu.be/dQw4w9WgXcQ?si=SvqZnOWFu5bQp9h9')
                    
            keyboard.add(partners, motivation, course_card, about_us, methods, structure)
            bot.edit_message_text('⬇️ Выберите действие', callback.message.chat.id, callback.message.id, reply_markup=keyboard)
        elif User.get_role_by_id(callback.message.chat.id) == 'tutor':

            instructions_and_regulations = telebot.types.InlineKeyboardButton('Инструкции и регламенты', callback_data="instructions_and_regulations")
            сourse_card = telebot.types.InlineKeyboardButton('Карта курсов', callback_data="сourse_card")
            partners = telebot.types.InlineKeyboardButton('Партнеры', callback_data="partners_tutor")
            motivation = telebot.types.InlineKeyboardButton('Мотивация', callback_data="motivation")
            axo = telebot.types.InlineKeyboardButton('АХО', callback_data="axo")

            structure_question = telebot.types.InlineKeyboardButton('Инструкции и регламенты', url='https://youtu.be/dQw4w9WgXcQ?si=SvqZnOWFu5bQp9h9')
            about_company = telebot.types.InlineKeyboardButton('О компании', url='https://youtu.be/dQw4w9WgXcQ?si=SvqZnOWFu5bQp9h9')

            keyboard.add(instructions_and_regulations, сourse_card, motivation, axo, structure_question, about_company)
            bot.edit_message_text('⬇️ Выберите действие', callback.message.chat.id, callback.message.id, reply_markup=keyboard)


if __name__ == "__main__":
    print("Bot is running...")
    bot.polling(none_stop=True)