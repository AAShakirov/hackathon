from aiogram import Router
from aiogram.types import Message

router: Router = Router()


# Этот хэндлер будет реагировать на любые сообщения пользователя,
# не предусмотренные логикой работы бота
@router.message()
async def send_echo(message: Message):
    await message.answer(f'К сожалению, я Вас не понял.\nПожалуйста, ознакомьтесь со списком доступных команд /help')
