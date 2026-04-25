import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Токен, полученный от @BotFather
TOKEN = '8092743460:AAEf1WBmd9gjsqckWgSVdB47-opYMRMD1_E'

bot = Bot(token=TOKEN)
dp = Dispatcher()


# --- Вспомогательные функции для создания клавиатур ---

def get_main_menu():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Приложение", url="https://google.com"))
    builder.row(types.InlineKeyboardButton(text="Сайт", url="https://google.com"))
    builder.row(types.InlineKeyboardButton(text="ВКонтакте", url="https://vk.com"))
    builder.row(types.InlineKeyboardButton(text="Подсказки к лабораторным", callback_data="show_classes"))
    return builder.as_markup()


def get_classes_menu():
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="7 класс", callback_data="class_7"))
    builder.add(types.InlineKeyboardButton(text="8 класс", callback_data="class_8"))
    builder.add(types.InlineKeyboardButton(text="9 класс", callback_data="class_9"))
    builder.row(types.InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu"))
    return builder.as_markup()


def get_subjects_menu(grade):
    builder = InlineKeyboardBuilder()
    # Передаем класс дальше в callback, чтобы знать, куда вернуться
    builder.add(types.InlineKeyboardButton(text="Химия", callback_data=f"sub_{grade}_chem"))
    builder.add(types.InlineKeyboardButton(text="Биология", callback_data=f"sub_{grade}_bio"))
    builder.add(types.InlineKeyboardButton(text="Физика", callback_data=f"sub_{grade}_phys"))
    builder.row(types.InlineKeyboardButton(text="⬅️ Назад", callback_data="show_classes"))
    return builder.as_markup()


def get_labs_menu(grade, subject):
    builder = InlineKeyboardBuilder()
    for i in range(1, 6):
        builder.row(types.InlineKeyboardButton(text=f"{i} лабораторная", callback_data=f"lab_{grade}_{subject}_{i}"))
    builder.row(types.InlineKeyboardButton(text="⬅️ Назад", callback_data=f"class_{grade}"))
    return builder.as_markup()


# --- Обработчики событий ---

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Добро пожаловать! Выберите нужный раздел:", reply_markup=get_main_menu())


@dp.callback_query(F.data == "main_menu")
async def back_to_main(callback: types.CallbackQuery):
    await callback.message.edit_text("Выберите нужный раздел:", reply_markup=get_main_menu())


@dp.callback_query(F.data == "show_classes")
async def select_class(callback: types.CallbackQuery):
    await callback.message.edit_text("Выберите класс:", reply_markup=get_classes_menu())


@dp.callback_query(F.data.startswith("class_"))
async def select_subject(callback: types.CallbackQuery):
    grade = callback.data.split("_")[1]
    await callback.message.edit_text(f"Выбран {grade} класс. Теперь выберите предмет:",
                                     reply_markup=get_subjects_menu(grade))


@dp.callback_query(F.data.startswith("sub_"))
async def select_lab(callback: types.CallbackQuery):
    data = callback.data.split("_")
    grade, subject = data[1], data[2]

    subjects_ru = {"chem": "Химия", "bio": "Биология", "phys": "Физика"}

    text = f"Ваш выбор: {grade} класс, предмет — {subjects_ru[subject]}.\nВыберите номер работы:"
    await callback.message.edit_text(text, reply_markup=get_labs_menu(grade, subject))


@dp.callback_query(F.data.startswith("lab_"))
async def show_lab_info(callback: types.CallbackQuery):
    data = callback.data.split("_")
    # Структура: lab_[grade]_[subject]_[number]
    await callback.answer(f"Вы выбрали лабораторную №{data[3]}", show_alert=True)


# --- Запуск бота ---
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())