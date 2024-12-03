import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup


API = ''
bot = Bot(token=API)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()  # возраст
    growth = State()  # рост
    weight = State()  # вес


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.')


@dp.message_handler(text='Calories')
async def set_age(message):
    await message.answer('Введите свой возраст: ')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост: ')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес: ')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    try:
        calories = ((10*float(data['weight'])) +
                    (6.25*float(data['growth'])) -
                    (5*float(data['age'])) + 5)
        await message.answer(f'Ваша норма калорий: {calories}')
    except ValueError:
        await message.answer('Вы ввели не верные данные, попробуйте еще раз.')
    await state.finish()


@dp.message_handler()
async def all_message(message):
    await message.answer('Введите \'Calories\', чтобы узнать норму калорий в день.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
