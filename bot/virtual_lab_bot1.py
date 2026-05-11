
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import BotCommand

# Токен от @BotFather
TOKEN = '8092743460:AAEf1WBmd9gjsqckWgSVdB47-opYMRMD1_E'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- БАЗА ДАННЫХ ЛАБОРАТОРНЫХ ---
LABS_DATA = {
    "phys": {
        "7": [
            "Определение цены деления измерительного прибора",
            "Измерение размеров малых тел",
            "Измерение массы тела на рычажных весах"
        ],
        "8": [
            "Сравнение количества теплоты при смешивании воды разной температуры",
            "Измерение удельной теплоемкости твердого тела",
            "Сборка электрической цепи и измерение силы тока",
            "Измерение напряжения на различных участках цепи"
        ],
        "9": [
            "Исследование равноускоренного движения",
            "Измерение ускорения свободного падения",
            "Исследование колебаний нитяного маятника"
        ]
    },
    "chem": {
        "8": [
            "Изменение окраски индикаторов",
            "Распознавание соляной кислоты и галогенидов",
            "Типы химических реакций (Cu(OH)2, Fe+CuCl2)",
            "Взаимодействие металлов с кислотами",
            "Взаимодействие кислот с щелочами",
            "Получение нерастворимых оснований",
            "Отбеливающие свойства хлора"
        ],
        "9": [
            "Факторы скорости реакции",
            "Получение и свойства аммиака",
            "Получение CO2 и распознавание карбонатов"
        ]
    },
    "bio": {
        "7": [
            "Строение шляпочных грибов",
            "Строение зеленых водорослей",
            "Изучение строения папоротника и хвоща"
        ],
        "8": [
            "Микроскопическое строение кости",
            "Мышцы человеческого тела"
        ],
        "9": [
            "Клетки под микроскопом",
            "Выявление изменчивости организмов",
            "Морфологический критерий вида"
        ]
    }
}

SUBJECT_NAMES = {"phys": "Физика", "chem": "Химия", "bio": "Биология"}


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
    # Убираем Химию для 7 класса
    if grade != "7":
        builder.row(types.InlineKeyboardButton(text="🧪 Химия", callback_data=f"sub_{grade}_chem"))
    builder.row(types.InlineKeyboardButton(text="🧬 Биология", callback_data=f"sub_{grade}_bio"))
    builder.row(types.InlineKeyboardButton(text="⚡ Физика", callback_data=f"sub_{grade}_phys"))
    builder.row(types.InlineKeyboardButton(text="⬅️ Назад к классам", callback_data="show_classes"))
    return builder.as_markup()


def get_labs_menu(grade, subject):
    builder = InlineKeyboardBuilder()
    labs = LABS_DATA.get(subject, {}).get(grade, [])

    for idx, name in enumerate(labs):
        # Ограничиваем длину текста на кнопке, чтобы она не была огромной
        short_name = (name[:30] + '..') if len(name) > 30 else name
        builder.row(types.InlineKeyboardButton(text=f"🔬 {short_name}", callback_data=f"lab_{grade}_{subject}_{idx}"))

    builder.row(types.InlineKeyboardButton(text="⬅️ Назад к предметам", callback_data=f"class_{grade}"))
    builder.row(types.InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu"))
    return builder.as_markup()


# --- ОБРАБОТЧИКИ ---

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    # Настраиваем кнопку меню команд рядом с вводом
    main_commands = [BotCommand(command="start", description="Запустить бота / Главное меню")]
    await bot.set_my_commands(main_commands)

    await message.answer(
        f"👋 **Привет, {message.from_user.first_name}!**\n\nЯ помогу тебе с лабораторными работами. "
        "Выбери нужный раздел ниже:",
        reply_markup=get_main_menu(), parse_mode="Markdown"
    )


@dp.callback_query(F.data == "main_menu")
async def back_to_main(callback: types.CallbackQuery):
    await callback.message.edit_text("Главное меню. Выберите раздел:", reply_markup=get_main_menu())


@dp.callback_query(F.data == "show_classes")
async def select_class(callback: types.CallbackQuery):
    await callback.message.edit_text("📖 Выберите класс:", reply_markup=get_classes_menu())


@dp.callback_query(F.data.startswith("class_"))
async def select_subject(callback: types.CallbackQuery):
    grade = callback.data.split("_")[1]
    await callback.message.edit_text(f"🎓 {grade} класс. Выберите предмет:", reply_markup=get_subjects_menu(grade))


@dp.callback_query(F.data.startswith("sub_"))
async def select_lab(callback: types.CallbackQuery):
    data = callback.data.split("_")
    grade, subject = data[1], data[2]
    await callback.message.edit_text(
        f"📍 {grade} класс | {SUBJECT_NAMES[subject]}\nВыберите работу:",
        reply_markup=get_labs_menu(grade, subject)
    )


@dp.callback_query(F.data.startswith("lab_"))
async def show_lab_info(callback: types.CallbackQuery):
    data = callback.data.split("_")
    grade, subject, idx = data[1], data[2], int(data[3])
    lab_name = LABS_DATA[subject][grade][idx]

    text = (
        f"🧪 **Предмет:** {SUBJECT_NAMES[subject]}\n"
        f"📏 **Класс:** {grade}\n"
        f"📝 **Работа:** {lab_name}\n\n"
        f"💡 **Тут подсказка!**"
    )

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="⬅️ Назад к списку", callback_data=f"sub_{grade}_{subject}"))
    builder.row(types.InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu"))

    await callback.message.edit_text(text, reply_markup=builder.as_markup(), parse_mode="Markdown")


async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
