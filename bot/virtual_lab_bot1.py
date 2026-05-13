import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import BotCommand

TOKEN = '8092743460:AAEf1WBmd9gjsqckWgSVdB47-opYMRMD1_E'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

LABS_DATA = {
    "phys": {
        "7": [
            {"name": "Определение цены деления измерительного прибора",
             "hint": "На колбе видны полосочки, они наверняка что-то значат."},
            {"name": "Измерение размеров малых тел",
             "hint": "Выстроив горошины (зеленые шарики) вдоль линейки, можно узнать средний диаметр одной горошины."},
            {"name": "Измерение массы тела на рычажных весах",
             "hint": "Все, что тебе нужно, - это перестаскивать появляющиеся предметы на весы."},
        ],
        "8": [
            {"name": "Сравнение количества теплоты при смешивании воды разной температуры",
             "hint": "Массу воды нужно посчитать по формуле, плостность единица из таблицы, а вот объем можно узнать только в начале опыта, поэтому, если ты уже перелил воду из колбы в стакан, то тебе придется начинать опыт заново."},
            {"name": "Измерение удельной теплоемкости твердого тела",
             "hint": "Не забывай проверять температуру воды во всех емкостях после каждого шага."},
            {"name": "Сборка электрической цепи и измерение силы тока",
             "hint": "Перед выполнением этой работы внимательно изучи как выглядят различные приборы связанные с электрическими цепями."},
            {"name": "Измерение напряжения на различных участках цепи",
             "hint": "Чтобы понять, почему напряжение на всей цепи больше, чем на отдельной лампочке, измерьте его на разных участках и сравните результаты с показаниями на зажимах источника тока."},
        ],
        "9": [
            {"name": "Исследование равноускоренного движения",
             "hint": "Внимательно следи за опытом, потому что посмотреть ты его сможешь только один раз."},
            {"name": "Измерение ускорения свободного падения",
             "hint": "Измерив период и длину маятника, вычислите g и проверьте, получится ли у вас 9,8 м/с², несмотря на погрешности измерений."},
            {"name": "Исследование колебаний нитяного маятника",
             "hint": "Попробуйте по очереди менять длину нити, массу грузика и амплитуду, чтобы выяснить, какой из этих параметров на самом деле влияет на период колебаний."},
        ]
    },
    "chem": {
        "8": [
            {"name": "Изменение окраски индикаторов", "hint": "Капните лакмус, метилоранж и фенолфталеин в пробирки с кислотой, щелочью и водой, чтобы увидеть, как каждый индикатор меняет цвет в зависимости от среды."},
            {"name": "Распознавание соляной кислоты и галогенидов",
             "hint": "Внимательно читай задание (оно тее поможет ответить на вопрос)."},
            {"name": "Типы химических реакций (Cu(OH)2, Fe+CuCl2)",
             "hint": "Сначала прокалите голубой осадок Cu(OH)₂, наблюдая разложение на черный оксид и воду, а затем опустите железный гвоздь в синий раствор CuCl₂, чтобы вытеснить красную медь по реакции замещения."},
            {"name": "Взаимодействие металлов с кислотами", "hint": "Опустите магний, цинк и медь в пробирки с соляной кислотой и сравните, какой металл выделяет водород с наибольшей скоростью, а какой не реагирует вообще."},
            {"name": "Взаимодействие кислот с щелочами",
             "hint": "Внимательно читай задание (оно тее поможет ответить на вопрос)."},
            {"name": "Получение нерастворимых оснований",
             "hint": "Внимательно читай задание (оно тее поможет ответить на вопрос)."},
            {"name": "Отбеливающие свойства хлора",
             "hint": "Все ответы ты можешь найти в задании или в названии темы."},
        ],
        "9": [
            {"name": "Факторы скорости реакции",
             "hint": "В каждом задании есть инструкция к выполнению опыта, после ее выполнения не забудь нажать на кнопку (Провести опыт) иначе реакция не пойдет. Если ты выполняешь лабораторную работу с телефона, то в конце (в таблице с твоими ответами на предыдущие задания) прокрути влево и у тебя откроется еще один столбец для заполнения."},
            {"name": "Получение и свойства аммиака",
             "hint": "Нажимай на кнопку (Провести опыт) несколько раз, после каждого нажатия у тебя будет производиться новый шаг опыта, каждй шаг важен для заполнения таблицы."},
            {"name": "Получение CO2 и распознавание карбонатов",
             "hint": "Будь осторожен! После первой проверки таблицы отвветов у заданий, ты больше не сможешь проверять ее."},
        ]
    },
    "bio": {
        "7": [
            {"name": "Строение шляпочных грибов",
             "hint": "У трубчатых грибов под шляпкой много круглых отверстий, а у пластинчатых под шляпкой видно множество пластинок."},
            {"name": "Строение зеленых водорослей",
             "hint": "На большинство вопросов ты ответишь если внимательно изучишь изображение, но вот тебе одна подсказка: у одного из органоидов есть всё, кроме оболочки, а у другого есть оболочка, но нет некоторых других частей."},
            {"name": "Изучение строения папоротника и хвоща",
             "hint": "Найдите на живых или гербарных образцах корневище, вайи (листья) папоротника и членистые зелёные побеги с мутовками хвоща, а затем рассмотрите под лупой сорусы со спорами на нижней стороне листа папоротника."},
        ],
        "8": [
            {"name": "Микроскопическое строение кости", "hint": "Рассмотрите при малом и большом увеличении постоянный препарат «Распил кости», чтобы отличить тёмные концентрические пластины (гаверсовы каналы) от пустот, где лежали клетки-остеоциты."},
            {"name": "Мышцы человеческого тела", "hint": "Покажите на торсе или рисунке мышцы сгибатели и разгибатели руки и ноги, а затем попробуйте напрячь их при движении, чтобы понять, как они работают парами."},
        ],
        "9": [
            {"name": "Клетки под микроскопом", "hint": "Сравните готовые микропрепараты животных (эпителий, клетки крови) и растительных (элодея, лук) клеток, чтобы найти главные отличия: клеточную стенку и хлоропласты у растений и отсутствие их у животных клеток."},
            {"name": "Выявление изменчивости организмов",
             "hint": "Внимательно рассмотрите листья представленные на картинках. Определите частоты появления листовых пластин определенной длины для каждого листа."},
            {"name": "Морфологический критерий вида",
             "hint": "Внимательно рассмотрите листья представленные на картинках. Определите частоты появления листовых пластин определенной длины для каждого листа."},
        ]
    }
}

SUBJECT_NAMES = {"phys": "Физика", "chem": "Химия", "bio": "Биология"}


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
    if grade != "7":
        builder.row(types.InlineKeyboardButton(text="🧪 Химия", callback_data=f"sub_{grade}_chem"))
    builder.row(types.InlineKeyboardButton(text="🧬 Биология", callback_data=f"sub_{grade}_bio"))
    builder.row(types.InlineKeyboardButton(text="⚡ Физика", callback_data=f"sub_{grade}_phys"))
    builder.row(types.InlineKeyboardButton(text="⬅️ Назад к классам", callback_data="show_classes"))
    return builder.as_markup()


def get_labs_menu(grade, subject):
    builder = InlineKeyboardBuilder()
    labs = LABS_DATA.get(subject, {}).get(grade, [])

    for idx, lab in enumerate(labs):
        name = lab['name']
        short_name = (name[:30] + '..') if len(name) > 30 else name
        builder.row(types.InlineKeyboardButton(text=f"🔬 {short_name}", callback_data=f"lab_{grade}_{subject}_{idx}"))

    builder.row(types.InlineKeyboardButton(text="⬅️ Назад к предметам", callback_data=f"class_{grade}"))
    builder.row(types.InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu"))
    return builder.as_markup()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
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
        f"📍 {grade} класс | {SUBJECT_NAMES[subject]}\nВыберите лабораторную работу:",
        reply_markup=get_labs_menu(grade, subject)
    )


@dp.callback_query(F.data.startswith("lab_"))
async def show_lab_info(callback: types.CallbackQuery):
    data = callback.data.split("_")
    grade, subject, idx = data[1], data[2], int(data[3])


    lab_data = LABS_DATA[subject][grade][idx]

    text = (
        f"🔬 **Лабораторная работа:** {lab_data['name']}\n"
        f"📊 **Предмет:** {SUBJECT_NAMES[subject]}\n"
        f"🏫 **Класс:** {grade}\n"
        f"────────────────────\n"
        f"💡 **ПОДСКАЗКА:**\n\n"
        f"{lab_data['hint'] if lab_data['hint'] else '*(Текст подсказки еще не добавлен)*'}"
    )

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="⬅️ Назад к списку", callback_data=f"sub_{grade}_{subject}"))
    builder.row(types.InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu"))

    await callback.message.edit_text(text, reply_markup=builder.as_markup(), parse_mode="Markdown")


async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен.")
