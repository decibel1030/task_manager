import os
from bot_functions import *
from aiogram import types, executor, Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from config import TOKEN
from aiogram.dispatcher.filters import Text, Command
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


token = TOKEN

bot = Bot(token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class UserState(StatesGroup):
    title = State()
    description = State()
    # todo add photo state


@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    add_button = KeyboardButton("Создать")
    issues_count = get_count_for_kb(message.from_user.id)
    if issues_count is not False and issues_count != 0:
        show_button = KeyboardButton(f"Показать({issues_count})")
    else:
        show_button = KeyboardButton("Показать")

    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(add_button, show_button)
    await message.answer("Привет! Чтобы запланировать какую либо задачу импользуй команду /add"
                         " или введите строку 'Создать'", reply_markup=kb)


@dp.message_handler(Text(equals="Создать") or Command('add'))
async def request_title(message: types.Message):
    await UserState.title.set()
    await message.answer("Введите заголовок для вашей задачи")


@dp.message_handler(state=UserState.title)
async def request_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['title'] = message.text
    await message.answer("Введите описание для задачи")
    await UserState.description.set()


@dp.message_handler(state=UserState.description)
async def finish(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
        title = data['title']
        date = get_date()
        description = message.text
    # check user data file is exist
    if os.path.exists(f"data/{message.from_user.id}.json"):
        refresh_data_in_user_file(user_id=message.from_user.id,
                                  issue_data={"title": title,
                                              "description": description,
                                              "created_at": date})
    else:
        create_user_data_file(user_id=message.from_user.id)
        refresh_data_in_user_file(user_id=message.from_user.id,
                                  issue_data={"title": title,
                                              "description": description,
                                              "created_at": date})

    await message.answer(text='Запись успешно сохранена!\nХотите создать новые записи ?')
    await state.finish()


class Show(StatesGroup):
    show_all = State()


@dp.message_handler(Command("get") or Text(equals="Показать"))
async def show_init(message: types.Message):
    data = get_all_tasks_count(message.from_user.id)
    if data is not False:
        ans_yes = KeyboardButton("Да")
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add(ans_yes)
        await message.answer(text=get_all_tasks_count(message.from_user.id), reply_markup=kb)
        await Show.show_all.set()
    else:
        button = KeyboardButton("Создать")
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add(button)
        await message.reply(text="У вас нету сохранённых записей", reply_markup=kb)


@dp.message_handler(Text(equals="Да"), state=Show.show_all)
async def show_all(message: types.Message):
    add_button = KeyboardButton("Создать")
    issues_count = get_count_for_kb(message.from_user.id)
    if issues_count is not False and issues_count != 0:
        show_button = KeyboardButton(f"Показать({issues_count})")
    else:
        show_button = KeyboardButton("Показать")
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(add_button, show_button)
    await message.answer(get_all_task_list(message.from_user.id), parse_mode='html', reply_markup=kb)


@dp.message_handler(Command("info"))
async def info(message: types.Message):
    await message.answer("Бот всё ещё тестируется. Но впринципе я старался")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)


