from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

TOKEN = "8706653486:AAF9QfiiHJM5u_khFRgWwyLzlF1_tHHUzSI"
bot = Bot(TOKEN)
dp = Dispatcher()

current_temp = 22
light_status = "Вимкнено"
security_status = "Не активована"


def get_status_text():
    return (
        f"Поточний стан системи:\n"
        f"Світло: {light_status}\n"
        f"Температура: {current_temp}°C\n"
        f"Безпека: {security_status}\n"
    )


def get_main_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💡 Світло", callback_data="menu_light"),
         InlineKeyboardButton(text="🌡️ Клімат", callback_data="menu_climate")],
        [InlineKeyboardButton(text="🛡️ Безпека", callback_data="menu_security"),
         InlineKeyboardButton(text="ℹ️ Довідка", callback_data="menu_help")]
    ])
    return keyboard


def get_light_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Увімкнути", callback_data="light_on"),
         InlineKeyboardButton(text="Вимкнути", callback_data="light_off")],
        [InlineKeyboardButton(text="Назад", callback_data="back_to_main")]
    ])
    return keyboard


def get_security_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Увімкнути датчики", callback_data="sec_on"),
         InlineKeyboardButton(text="Вимкнути датчики", callback_data="sec_off")],
        [InlineKeyboardButton(text="Назад", callback_data="back_to_main")]
    ])
    return keyboard


def get_climate_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="back_to_main")]
    ])
    return keyboard


@dp.message(CommandStart())
async def start(msg: types.Message):
    text = (
        "Доброго дня. Я бот - прототип системи \"Розумний будинок\".\n\n"
        f"{get_status_text()}\n"
        "Керуйте пристроями за допомогою кнопок нижче або текстових команд."
    )
    await msg.answer(text, reply_markup=get_main_menu())


@dp.callback_query()
async def handle_callback(call: types.CallbackQuery):
    global light_status, security_status, current_temp

    if call.data == "back_to_main":
        text = f"Головне меню:\n\n{get_status_text()}"
        await call.message.edit_text(text, reply_markup=get_main_menu())

    elif call.data == "menu_light":
        text = f"Керування світлом:\n\n{get_status_text()}"
        await call.message.edit_text(text, reply_markup=get_light_menu())

    elif call.data == "light_on":
        light_status = "Увімкнено"
        text = f"Світло увімкнено.\n\n{get_status_text()}"
        await call.message.edit_text(text, reply_markup=get_light_menu())

    elif call.data == "light_off":
        light_status = "Вимкнено"
        text = f"Світло вимкнено.\n\n{get_status_text()}"
        await call.message.edit_text(text, reply_markup=get_light_menu())

    elif call.data == "menu_climate":
        text = (
            f"Керування кліматом.\nПоточна температура: {current_temp}°C\n\n"
            "Напишіть у чат бажану температуру (від +16 до +42 градусів), наприклад: \"25\"."
        )
        await call.message.edit_text(text, reply_markup=get_climate_menu())

    elif call.data == "menu_security":
        text = f"Керування безпекою:\n\n{get_status_text()}"
        await call.message.edit_text(text, reply_markup=get_security_menu())

    elif call.data == "sec_on":
        security_status = "Активована"
        text = f"Система безпеки активована. Датчики працюють.\n\n{get_status_text()}"
        await call.message.edit_text(text, reply_markup=get_security_menu())

    elif call.data == "sec_off":
        security_status = "Вимкнена"
        text = f"Система безпеки вимкнена. Датчики не працюють.\n\n{get_status_text()}"
        await call.message.edit_text(text, reply_markup=get_security_menu())

    elif call.data == "menu_help":
        text = (
            "Довідка:\n"
            "Цей бот є прототипом системи \"Розумний будинок\".\n"
            "Він підтримує керування світлом, кліматом та безпекою.\n"
            "Технології: Python, aiogram, Telegram Bot API."
        )
        await call.message.edit_text(text, reply_markup=get_main_menu())

    await call.answer()


@dp.message()
async def answer_text(msg: types.Message):
    global light_status, security_status, current_temp

    if msg.text.startswith("/"):
        await msg.answer("Я вас не зрозумів. Напишіть /start для появи меню.")
        return

    q = msg.text.lower().strip().replace("ї", "и").replace("і", "i")

    if "свiтло" in q or "свитло" in q:
        if "вимк" in q or "викл" in q:
            light_status = "Вимкнено"
            await msg.answer(f"Світло вимкнено.\n\n{get_status_text()}", reply_markup=get_main_menu())
        else:
            light_status = "Увімкнено"
            await msg.answer(f"Світло увімкнено.\n\n{get_status_text()}", reply_markup=get_main_menu())

    elif "градус" in q or "температур" in q or q.isdigit():
        words = q.split()
        num_str = None
        for word in words:
            if word.isdigit():
                num_str = word
                break

        if num_str:
            temp = int(num_str)
            if 16 <= temp <= 42:
                current_temp = temp
                await msg.answer(f"Температуру встановлено на {temp}°C.\n\n{get_status_text()}",
                                 reply_markup=get_main_menu())
            else:
                await msg.answer(f"Помилка! Температура має бути в межах від +16°C до +42°C. Ви вказали: {temp}°C.")
        else:
            await msg.answer("Будь ласка, вкажіть число. Наприклад: \"Постав 23 градуси\".")

    elif "безпек" in q or "сигналізац" in q or "перевiр" in q or "перевир" in q or "датчик" in q:
        if "вимк" in q or "викл" in q:
            security_status = "Вимкнена"
            await msg.answer(f"Система безпеки вимкнена.\n\n{get_status_text()}", reply_markup=get_main_menu())
        else:
            security_status = "Активована"
            await msg.answer(f"Система безпеки активована.\n\n{get_status_text()}", reply_markup=get_main_menu())

    elif "допомог" in q or "довідк" in q:
        await msg.answer("Я можу керувати світлом, кліматом та безпекою. Натисніть /start, щоб побачити меню.")

    else:
        await msg.answer("Я вас не зрозумів. Напишіть /start для появи меню.")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())