from telebot import types, TeleBot
import sqlite3
from config import TOKEN, ADMINS
from user import User, create_table

bot = TeleBot(TOKEN)

def teacher_menu():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    buttons = [
        types.InlineKeyboardButton('Партнеры 🤝🏻', callback_data="partners_teacher"),
        types.InlineKeyboardButton('Мотивация 📈', callback_data="motivation"),
        types.InlineKeyboardButton('Карта курсов 📚', callback_data="course_card"),
        types.InlineKeyboardButton('О компании 🏢', url='https://movavi.ru/about'),
        types.InlineKeyboardButton('Метод работа 👨🏻‍💻', url='https://movavi.ru/methods'),
        types.InlineKeyboardButton('Структура (Кто? Где? Когда?) ❔', url='https://movavi.ru/structure')
    ]
    
    keyboard.add(*buttons)
    return keyboard


def tutor_menu():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    buttons = [
        types.InlineKeyboardButton('Инструкции и регламенты 📄', callback_data="instructions_and_regulations"),
        types.InlineKeyboardButton('АХО ❔', callback_data="axo"),
        types.InlineKeyboardButton('Партнеры 🤝🏻', callback_data="partners_tutor"),
        types.InlineKeyboardButton('Мотивация 📈', callback_data="motivation"),
        types.InlineKeyboardButton('Карта курсов 📚', callback_data="course_card"),
        types.InlineKeyboardButton('О компании 🏢', url='https://movavi.ru/about'),
        types.InlineKeyboardButton('Структура (Кто? Где? Когда?) ❔', url='https://movavi.ru/structure')
    ]
    
    keyboard.add(*buttons)
    return keyboard


@bot.message_handler(commands=['start'])
def start(message):
    create_table()
    User.add_user(message.chat.id)
    user_role = User.get_role_by_id(message.chat.id)
    
    if not user_role:
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        tutor = types.InlineKeyboardButton('Я куратор 👨🏻‍💻', callback_data="tutor")
        teacher = types.InlineKeyboardButton('Я преподаватель 👨🏻‍🏫', callback_data="teacher")
        keyboard.add(tutor, teacher)
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!\nКто вы?', reply_markup=keyboard)
    elif user_role == 'teacher':
        bot.send_message(message.chat.id, '⬇️ Выберите действие', reply_markup=teacher_menu())
    elif user_role == 'tutor':
        bot.send_message(message.chat.id, '⬇️ Выберите действие', reply_markup=tutor_menu())


@bot.callback_query_handler(func=lambda callback: True)
def handle_callback(callback):
    if callback.data in ('teacher', 'tutor'):
        User.add_role_to_user(callback.message.chat.id, callback.data)
        bot.answer_callback_query(callback.id, f"Вы выбрали роль {callback.data}")

        if callback.data == 'teacher' or callback.data == "main_menu" and User.get_role_by_id(callback.message.chat.id) == 'teacher':
            bot.edit_message_text('⬇️ Выберите действие', callback.message.chat.id, callback.message.id, reply_markup=teacher_menu())

        elif callback.data == 'tutor' or callback.data == "main_menu" and User.get_role_by_id(callback.message.chat.id) == 'tutor':
            bot.edit_message_text('⬇️ Выберите действие', callback.message.chat.id, callback.message.id, reply_markup=tutor_menu())   

    elif callback.data == "instructions_and_regulations":
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        buttons = [
            types.InlineKeyboardButton('Документооборот 📄', url='https://movavi.ru/documents'),
            types.InlineKeyboardButton('Касса 💱', url='https://movavi.ru/cashier'),
            types.InlineKeyboardButton('Пожарная эвакуация 🚒', url='https://movavi.ru/fire_evacuation'),
            types.InlineKeyboardButton('Работа с контрагентами 🤝🏻', url='https://movavi.ru/working_with_contractors'),
            types.InlineKeyboardButton('Первая помощь 🚑', url='https://movavi.ru/first_aid'),
            types.InlineKeyboardButton('CPM 💼', callback_data="CPM"),
            types.InlineKeyboardButton('Назад 🔙', callback_data="main_menu"),
            types.InlineKeyboardButton('В главное меню 🔚', callback_data="main_menu")
        ]

        keyboard.add(*buttons)
        bot.edit_message_text('⬇️ Выберите действие', callback.message.chat.id, callback.message.id, reply_markup=keyboard)

    elif callback.data == "CPM":
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        buttons = [
            types.InlineKeyboardButton('Как создать договор 📄', url='https://movavi.ru/how_create_contract'),
            types.InlineKeyboardButton('Как провести оплату 💰', url='https://movavi.ru/how_make_payment'),
            types.InlineKeyboardButton('Назад 🔙', callback_data="main_menu"),
            types.InlineKeyboardButton('В главное меню 🔚', callback_data="main_menu")
        ]

        keyboard.add(*buttons)
        bot.edit_message_text('⬇️ Выберите действие', callback.message.chat.id, callback.message.id, reply_markup=keyboard)

    elif callback.data == "course_card":
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        buttons = [
            types.InlineKeyboardButton('Летняя школа 👨🏻‍🏫', url='https://movavi.ru/summer_school'),
            types.InlineKeyboardButton('Основные курсы 📚', url='https://movavi.ru/main_course'),
            types.InlineKeyboardButton('Краткосрочные группы 👨🏻‍🤝‍👨🏻', url='https://movavi.ru/shorttime_courses'),
            types.InlineKeyboardButton('Назад 🔙', callback_data="main_menu"),
            types.InlineKeyboardButton('В главное меню 🔚', callback_data="main_menu")
        ]

        keyboard.add(*buttons)
        bot.edit_message_text('⬇️ Выберите действие', callback.message.chat.id, callback.message.id, reply_markup=keyboard)

    elif callback.data == "motivation":
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        buttons = [
            types.InlineKeyboardButton('Обратная связь ☎', url='https://movavi.ru/call_back'),
            types.InlineKeyboardButton('Мовави Буст инструкция/пароли 📃', url='https://movavi.ru/movavi_boost'),
            types.InlineKeyboardButton('Назад 🔙', callback_data="main_menu"),
            types.InlineKeyboardButton('В главное меню 🔚', callback_data="main_menu")
        ]

        keyboard.add(*buttons)
        bot.edit_message_text('⬇️ Выберите действие', callback.message.chat.id, callback.message.id, reply_markup=keyboard)

    elif callback.data == "partners_tutor":
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        buttons = [
            types.InlineKeyboardButton('Рост 📈', callback_data="rise_tutor"),
            types.InlineKeyboardButton('Проскул 🏢', callback_data='proskul_tutor'),
            types.InlineKeyboardButton('10ая гимназия 🏫', callback_data='10gymnasiums_tutor'),
            types.InlineKeyboardButton('Назад 🔙', callback_data="main_menu"),
            types.InlineKeyboardButton('В главное меню 🔚', callback_data="main_menu")
        ]

        keyboard.add(*buttons)
        bot.edit_message_text('⬇️ Выберите действие', callback.message.chat.id, callback.message.id, reply_markup=keyboard)

    elif callback.data == "partners_teacher":
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        buttons = [
            types.InlineKeyboardButton('Рост 📈', callback_data="rise_teacher"),
            types.InlineKeyboardButton('Проскул 🏢', callback_data='proskul_teacher'),
            types.InlineKeyboardButton('10ая гимназия 🏫', callback_data='10gymnasiums_teacher'),
            types.InlineKeyboardButton('Назад 🔙', callback_data="main_menu"),
            types.InlineKeyboardButton('В главное меню 🔚', callback_data="main_menu")
        ]

        keyboard.add(*buttons)
        bot.edit_message_text('⬇️ Выберите действие', callback.message.chat.id, callback.message.id, reply_markup=keyboard)

    elif callback.data == "rise_teacher":
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        buttons = [
            types.InlineKeyboardButton('Олимпиада 🏆', url='https://movavi.ru/olympiad'),
            types.InlineKeyboardButton('Расписание 📅', url='https://movavi.ru/schedule_rise'),
            types.InlineKeyboardButton('Курсы 📚', url='https://movavi.ru/courses_rise'),
            types.InlineKeyboardButton('Назад 🔙', callback_data="partners_teacher"),
            types.InlineKeyboardButton('В главное меню 🔚', callback_data="main_menu")
        ]

        keyboard.add(*buttons)
        bot.edit_message_text('⬇️ Выберите действие', callback.message.chat.id, callback.message.id, reply_markup=keyboard)

    elif callback.data == "rise_tutor":
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        buttons = [
            types.InlineKeyboardButton('Олимпиада 🏆', url='https://movavi.ru/olympiad'),
            types.InlineKeyboardButton('Курсы 📚', url='https://movavi.ru/courses_rise'),
            types.InlineKeyboardButton('Назад 🔙', callback_data="partners_tutor"),
            types.InlineKeyboardButton('В главное меню 🔚', callback_data="main_menu")
        ]

        keyboard.add(*buttons)
        bot.edit_message_text('⬇️ Выберите действие', callback.message.chat.id, callback.message.id, reply_markup=keyboard)

    elif callback.data == "proskul_teacher":
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        buttons = [
            types.InlineKeyboardButton('Курсы 📚', url='https://movavi.ru/courses_proskul'),
            types.InlineKeyboardButton('Расписание 📅', url='https://movavi.ru/schedule_proskul'),
            types.InlineKeyboardButton('Назад 🔙', callback_data="partners_teacher"),
            types.InlineKeyboardButton('В главное меню 🔚', callback_data="main_menu")
        ]

        keyboard.add(*buttons)
        bot.edit_message_text('⬇️ Выберите действие', callback.message.chat.id, callback.message.id, reply_markup=keyboard)

    elif callback.data == "proskul_tutor":
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        buttons = [
            types.InlineKeyboardButton('Курсы 📚', url='https://movavi.ru/courses_proskul'),
            types.InlineKeyboardButton('Назад 🔙', callback_data="partners_tutor"),
            types.InlineKeyboardButton('В главное меню 🔚', callback_data="main_menu")
        ]

        keyboard.add(*buttons)
        bot.edit_message_text('⬇️ Выберите действие', callback.message.chat.id, callback.message.id, reply_markup=keyboard)

    elif callback.data == "10gymnasiums_teacher":
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        buttons = [
            types.InlineKeyboardButton('Расписание 📅', url='https://movavi.ru/schedule_10gymnasiums'),
            types.InlineKeyboardButton('Назад 🔙', callback_data="partners_teacher"),
            types.InlineKeyboardButton('В главное меню 🔚', callback_data="main_menu")
        ]

        keyboard.add(*buttons)
        bot.edit_message_text('⬇️ Выберите действие', callback.message.chat.id, callback.message.id, reply_markup=keyboard)

    elif callback.data == "10gymnasiums_tutor":
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        buttons = [
            types.InlineKeyboardButton('Курсы 📚', url='https://movavi.ru/courses_10gymnasiums'),
            types.InlineKeyboardButton('Назад 🔙', callback_data="partners_tutor"),
            types.InlineKeyboardButton('В главное меню 🔚', callback_data="main_menu")
        ]

        keyboard.add(*buttons)
        bot.edit_message_text('⬇️ Выберите действие', callback.message.chat.id, callback.message.id, reply_markup=keyboard)

    elif callback.data == "axo":
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        buttons = [
            types.InlineKeyboardButton('Полезные телефоны 📞', url='https://movavi.ru/useful_phones'),
            types.InlineKeyboardButton('Назад 🔙', callback_data="main_menu"),
            types.InlineKeyboardButton('В главное меню 🔚', callback_data="main_menu")
        ]

        keyboard.add(*buttons)
        bot.edit_message_text('⬇️ Выберите действие', callback.message.chat.id, callback.message.id, reply_markup=keyboard)

    elif callback.data == "main_menu":
        if User.get_role_by_id(callback.message.chat.id) == 'teacher':
            bot.edit_message_text('⬇️ Выберите действие', callback.message.chat.id, callback.message.id, reply_markup=teacher_menu())
        
        elif User.get_role_by_id(callback.message.chat.id) == 'tutor':
            bot.edit_message_text('⬇️ Выберите действие', callback.message.chat.id, callback.message.id, reply_markup=tutor_menu())


if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling()