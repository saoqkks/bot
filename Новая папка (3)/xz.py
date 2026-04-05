import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.markdown import hbold, hcode

TOKEN = '8766020585:AAFaA7KSkWEUvxWue5PC7QkFjCGeO5VtWG4'
ADMIN_ID = 6196887078

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    text = (
        f"👋 {hbold('Привет!')}\n\n"
        "Чтобы я получил твое сообщение и смог на него ответить, убедись, что у тебя "
        f"{hbold('включена пересылка сообщений')} в настройках конфиденциальности.\n"
        "⚙️Как проверить:\n"
        "Настройки -> Конфиденциальность -> Пересылка сообщений -> "
        f"{hbold('Все')} (или 'Мои контакты', если я у тебя есть).\n"
        "Теперь просто напиши свой вопрос ниже 👇"
    )
    await message.answer(text, parse_mode="HTML")

# Пересылка админу
@dp.message(F.chat.type == "private", F.from_user.id != ADMIN_ID)
async def forward_to_admin(message: types.Message):
    # Проверка на наличие forward_from (если скрыто — будет None)
    try:
        await message.forward(chat_id=ADMIN_ID)
        await bot.send_message(
            ADMIN_ID, 
            f"📩 {hbold('Новое сообщение!')}\n"
            f"От: @{message.from_user.username or 'без ника'}\n"
            f"ID: {hcode(message.from_user.id)}",
            parse_mode="HTML"
        )
        await message.answer("✅ Сообщение отправлено! Ожидай ответа.")
    except Exception:
        await message.answer("❌ Ошибка! У тебя скрыта пересылка сообщений. Я не вижу твой ID, чтобы ответить.")

# Ответ админа
@dp.message(F.from_user.id == ADMIN_ID, F.reply_to_message)
async def reply_to_user(message: types.Message):
    # Пытаемся взять ID из пересланного сообщения
    if message.reply_to_message.forward_from:
        target_id = message.reply_to_message.forward_from.id
        try:
            await bot.send_message(
                target_id, 
                f"✉️ {hbold('Ответ от администратора:')}\n\n{message.text}", 
                parse_mode="HTML"
            )
            await message.answer("🚀 Ответ успешно доставлен!")
        except Exception as e:
            await message.answer(f"❌ Ошибка при отправке: {e}")
    else:
        await message.answer(
            "❌ Не могу ответить! У этого пользователя {hbold('скрыта пересылка')}. "
            "Я не знаю его ID.", 
            parse_mode="HTML"
        )

async def main():
    print("🚀 Feedback Bot запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())