from copy import deepcopy
import re

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram import Router, Bot
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import CallbackQuery, Message
from database.database import user_dict_template, users_db
from filters.filters import IsDelBookmarkCallbackData, IsDigitCallbackData
from aiogram.filters.state import State, StatesGroup
from keyboards.bookmarks_kb import (create_bookmarks_keyboard,
                                    create_edit_keyboard)
from keyboards.pagination_kb import create_pagination_keyboard
from lexicon.lexicon import LEXICON
from services.file_handling import book


router: Router = Router()

class Form(StatesGroup):
    login = State()
    password = State()

def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками в один ряд
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)


# Этот хэндлер будет срабатывать на команду "/start" -
# добавлять пользователя в базу данных, если его там еще не было
# и отправлять ему приветственное сообщение
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(LEXICON[message.text])
    if message.from_user.id not in users_db:
        users_db[message.from_user.id] = deepcopy(user_dict_template)


# Этот хэндлер будет срабатывать на команду "/help"
# и отправлять пользователю сообщение со списком доступных команд в боте
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(LEXICON[message.text])

# Этот хэндлер будет срабатывать на команду "worktime"
# и отправлять пользователю сообщение со списком доступных команд в боте
@router.message(Command(commands='worktime'))
async def process_help_command(message: Message):
    await message.answer(LEXICON[message.text])

# Этот хэндлер будет срабатывать на команду "/sign_up"
# и авторизовывать пользователя на сайте


    # await message.answer(LEXICON[message.text])
    await Form.login.set() # set state to the first field to fill (name)
    await message.reply("Введите номер студенческого билета")
    # await bot.send_message(f'{user_login = }\n{user_password = }')

# @router.message(Command("sign_up'"))
# async def process_sign_up_command(message: Message, state: FSMContext):
#     await message.answer(
#         text="Введите номер студенческого билета:",
#         # reply_markup=make_row_keyboard(available_food_names)
#     )
#     # Устанавливаем пользователю состояние "выбирает название"
#     await state.set_state(Form.login)





# # handler to get the user's name and move to the next state (age)
# @router.message(state=Form.login)
# async def process_name(message: Message, state: FSMContext):
#     async with state as data:
#         data['login'] = message.text
#     await Form.next()
#     await message.reply("Введите пароль от moodle")

# @router.message(lambda message: message.text.isdigit(), state=Form.password)
# async def process_age(message: Message, state: FSMContext):
#     async with state as data:
#         data['password'] = message.text
#     await Form.next()
#     await message.reply("Введите пароль от moodle")

# # handler to get the user's gender and wrap up the form filling process
# @router.message(state=Form.gender)
# async def process_gender(message: Message, state: FSMContext):
#     async with state as data:
#         data['password'] = message.text
#         # you can do something with the data here, for example,
#         # store it in a database or send it to an API
#         response = f"Thank you for filling out the form, {data['password']}.  {data['password']}"





# Этот хэндлер будет срабатывать на команду "/beginning"
# и отправлять пользователю первую страницу книги с кнопками пагинации
@router.message(Command(commands='beginning'))
async def process_beginning_command(message: Message):
    users_db[message.from_user.id]['page'] = 1
    text = book[users_db[message.from_user.id]['page']]
    await message.answer(
            text=text,
            reply_markup=create_pagination_keyboard(
                    'backward',
                    f'{users_db[message.from_user.id]["page"]}/{len(book)}',
                    'forward'))


# Этот хэндлер будет срабатывать на команду "/continue"
# и отправлять пользователю страницу книги, на которой пользователь
# остановился в процессе взаимодействия с ботом
@router.message(Command(commands='continue'))
async def process_continue_command(message: Message):
    text = book[users_db[message.from_user.id]['page']]
    await message.answer(
                text=text,
                reply_markup=create_pagination_keyboard(
                    'backward',
                    f'{users_db[message.from_user.id]["page"]}/{len(book)}',
                    'forward'))


# Этот хэндлер будет срабатывать на команду "/bookmarks"
# и отправлять пользователю список сохраненных закладок,
# если они есть или сообщение о том, что закладок нет
@router.message(Command(commands='bookmarks'))
async def process_bookmarks_command(message: Message):
    if users_db[message.from_user.id]["bookmarks"]:
        await message.answer(
            text=LEXICON[message.text],
            reply_markup=create_bookmarks_keyboard(
                *users_db[message.from_user.id]["bookmarks"]))
    else:
        await message.answer(text=LEXICON['no_bookmarks'])


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "вперед"
# во время взаимодействия пользователя с сообщением-книгой
@router.callback_query(Text(text='forward'))
async def process_forward_press(callback: CallbackQuery):
    if users_db[callback.from_user.id]['page'] < len(book):
        users_db[callback.from_user.id]['page'] += 1
        text = book[users_db[callback.from_user.id]['page']]
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(
                    'backward',
                    f'{users_db[callback.from_user.id]["page"]}/{len(book)}',
                    'forward'))
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "назад"
# во время взаимодействия пользователя с сообщением-книгой
@router.callback_query(Text(text='backward'))
async def process_backward_press(callback: CallbackQuery):
    if users_db[callback.from_user.id]['page'] > 1:
        users_db[callback.from_user.id]['page'] -= 1
        text = book[users_db[callback.from_user.id]['page']]
        await callback.message.edit_text(
                text=text,
                reply_markup=create_pagination_keyboard(
                    'backward',
                    f'{users_db[callback.from_user.id]["page"]}/{len(book)}',
                    'forward'))
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# с номером текущей страницы и добавлять текущую страницу в закладки
@router.callback_query(lambda x: '/' in x.data and x.data.replace('/', '').isdigit())
async def process_page_press(callback: CallbackQuery):
    users_db[callback.from_user.id]['bookmarks'].add(
        users_db[callback.from_user.id]['page'])
    await callback.answer('Страница добавлена в закладки!')


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# с закладкой из списка закладок
@router.callback_query(IsDigitCallbackData())
async def process_bookmark_press(callback: CallbackQuery):
    text = book[int(callback.data)]
    users_db[callback.from_user.id]['page'] = int(callback.data)
    await callback.message.edit_text(
                text=text,
                reply_markup=create_pagination_keyboard(
                    'backward',
                    f'{users_db[callback.from_user.id]["page"]}/{len(book)}',
                    'forward'))
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# "редактировать" под списком закладок
@router.callback_query(Text(text='edit_bookmarks'))
async def process_edit_press(callback: CallbackQuery):
    await callback.message.edit_text(
                text=LEXICON[callback.data],
                reply_markup=create_edit_keyboard(
                                *users_db[callback.from_user.id]["bookmarks"]))
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# "отменить" во время работы со списком закладок (просмотр и редактирование)
@router.callback_query(Text(text='cancel'))
async def process_cancel_press(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON['cancel_text'])
    await callback.answer()

reg = re.compile(r'^Логин: (.*)$')
async def handle_message_start_with_123(message: Message):
    # Check if the message text matches the regular expression
    match = reg.match(message.text)
    if match:
        # Do something with the message (e.g. reply with a message)
        await message.reply("You sent a message that starts with 'Логин: '")

# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# с закладкой из списка закладок к удалению
@router.callback_query(IsDelBookmarkCallbackData())
async def process_del_bookmark_press(callback: CallbackQuery):
    users_db[callback.from_user.id]['bookmarks'].remove(
                                                    int(callback.data[:-3]))
    if users_db[callback.from_user.id]['bookmarks']:
        await callback.message.edit_text(
                    text=LEXICON['/bookmarks'],
                    reply_markup=create_edit_keyboard(
                            *users_db[callback.from_user.id]["bookmarks"]))
    else:
        await callback.message.edit_text(text=LEXICON['no_bookmarks'])
    await callback.answer()
