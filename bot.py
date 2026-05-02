import asyncio
from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, PreCheckoutQuery, LabeledPrice

TOKEN = "8649939857:AAF-CQUhDwSX9OJHnTK6FhX0okNo3brAEJE"

bot = Bot(token=TOKEN)
router = Router()
dp = Dispatcher()
dp.include_router(router)

@router.message(CommandStart())
async def start(message: Message):
    args = message.text.split()
    if len(args) > 1 and args[1].startswith("donate_"):
        amount = int(args[1].split("_")[1])
        await bot.send_invoice(
            chat_id=message.chat.id,
            title="Поддержать PayTracker",
            description="Спасибо за поддержку разработки!",
            payload=f"donation_{amount}",
            currency="XTR",
            provider_token="",
            prices=[LabeledPrice(label="Донат", amount=amount)]
        )
    else:
        await message.answer("Привет! Я бот PayTracker.")

@router.pre_checkout_query()
async def pre_checkout(query: PreCheckoutQuery):
    await query.answer(ok=True)

@router.message(F.successful_payment)
async def payment_done(message: Message):
    stars = message.successful_payment.total_amount
    await message.answer(f"Спасибо! Получено {stars} ★")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
