
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Токен, полученный от @BotFather
TOKEN = '8092743460:AAEf1WBmd9gjsqckWgSVdB47-opYMRMD1_E'

# Настройка логирования (помогает видеть ошибки в консоли)
logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()


# --- КЛАВИАТУРЫ ---

def get_main_menu():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="📱 Приложение", url="https://google.com"))
    builder.row(types.InlineKeyboardButton(text="🌐 Наш сайт", url="https://google.com"))
    builder.row(types.InlineKeyboardButton(text="💬 Группа ВК", url="https://vk.com"))
    builder.row(types.InlineKeyboardButton(text="📚 Подсказки к лабораторным", callback_data="show_classes"))
    return builder.as_markup()


def get_classes_menu():
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text="7 класс", callback_data="class_7"),
        types.InlineKeyboardButton(text="8 класс", callback_data="class_8"),
        types.InlineKeyboardButton(text="9 класс", callback_data="class_9")
    )
    builder.row(types.InlineKeyboardButton(text="⬅️ Назад в меню", callback_data="main_menu"))
    return builder.as_markup()


def get_subjects_menu(grade):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="🧪 Химия", callback_data=f"sub_{grade}_chem"))
    builder.row(types.InlineKeyboardButton(text="🧬 Биология", callback_data=f"sub_{grade}_bio"))
    builder.row(types.InlineKeyboardButton(text="⚡ Физика", callback_data=f"sub_{grade}_phys"))
    builder.row(types.InlineKeyboardButton(text="⬅️ Назад к классам", callback_data="show_classes"))
    return builder.as_markup()


def get_labs_menu(grade, subject):
    builder = InlineKeyboardBuilder()
    for i in range(1, 6):
        builder.row(types.InlineKeyboardButton(text=f"🔬 Лабораторная №{i}", callback_data=f"lab_{grade}_{subject}_{i}"))
    builder.row(types.InlineKeyboardButton(text="⬅️ Назад к предметам", callback_data=f"class_{grade}"))
    return builder.as_markup()


# --- ОБРАБОТЧИКИ (ХЕНДЛЕРЫ) ---

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    welcome_text = (
        f"👋 **Привет, {message.from_user.first_name}!**\n\n"
        "Я твой цифровой помощник по лабораторным работам. "
        "Здесь ты найдешь подсказки и алгоритмы, "
        "которые помогут сдать всё на отлично! 🔬✨\n\n"
        "Выбирай нужный раздел ниже:"
    )
    await message.answer(welcome_text, reply_markup=get_main_menu(), parse_mode="Markdown")


@dp.callback_query(F.data == "main_menu")
async def back_to_main(callback: types.CallbackQuery):
    text = "Добро пожаловать! Выберите нужный раздел:"
    await callback.message.edit_text(text, reply_markup=get_main_menu(), parse_mode="Markdown")


@dp.callback_query(F.data == "show_classes")
async def select_class(callback: types.CallbackQuery):
    text = (
        "📖 **Раздел: Лабораторные работы**\n\n"
        "Каждый год обучения — это новые вызовы. "
        "Выбери свой класс, чтобы получить актуальные подсказки:"
    )
    await callback.message.edit_text(text, reply_markup=get_classes_menu(), parse_mode="Markdown")


@dp.callback_query(F.data.startswith("class_"))
async def select_subject(callback: types.CallbackQuery):
    grade = callback.data.split("_")[1]
    text = (
        f"🎓 **Уровень: {grade} класс**\n\n"
        "Наука — это не скучно, если знать, куда смотреть! "
        "По какому предмету ищем материалы?"
    )
    await callback.message.edit_text(text, reply_markup=get_subjects_menu(grade), parse_mode="Markdown")


@dp.callback_query(F.data.startswith("sub_"))
async def select_lab(callback: types.CallbackQuery):
    data = callback.data.split("_")
    grade, subject = data[1], data[2]

    subjects_ru = {"chem": "🧪 Химия", "bio": "🧬 Биология", "phys": "⚡ Физика"}

    text = (
        f"📍 **Вы находитесь здесь:**\n"
        f"└ {grade} класс / {subjects_ru[subject]}\n\n"
        "📜 **Список доступных работ:**\n"
        "Выбери номер лабораторной, чтобы увидеть ход работы."
    )
    await callback.message.edit_text(text, reply_markup=get_labs_menu(grade, subject), parse_mode="Markdown")


@dp.callback_query(F.data.startswith("lab_"))
async def show_lab_info(callback: types.CallbackQuery):
    data = callback.data.split("_")
    # Структура callback: lab_[класс]_[предмет]_[номер]
    grade, subject, num = data[1], data[2], data[3]

    subjects_ru = {"chem": "Химия", "bio": "Биология", "phys": "Физика"}

    # Здесь в будущем можно добавить текст самой лабораторной
    await callback.answer(
        f"Вы открыли: {subjects_ru[subject]}, {grade} класс, работа №{num}.\nКонтент скоро появится!",
        show_alert=True
    )


# --- ЗАПУСК ---
async def main():
    print("Бот запущен и готов к работе...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")
