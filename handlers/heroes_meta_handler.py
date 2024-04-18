import requests
from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from bs4 import BeautifulSoup
from forms import MetaPosCallback, HeroIdCallback
from headers_and_useragent import headers

router = Router()


@router.message(F.text == 'Meta')
async def get_name(message: Message):
    pos_kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='1', callback_data=MetaPosCallback(pos_id='1', action='showmeta').pack()),
            InlineKeyboardButton(text='2', callback_data=MetaPosCallback(pos_id='2', action='showmeta').pack()),
            InlineKeyboardButton(text='3', callback_data=MetaPosCallback(pos_id='3', action='showmeta').pack()),
            InlineKeyboardButton(text='4', callback_data=MetaPosCallback(pos_id='4', action='showmeta').pack()),
            InlineKeyboardButton(text='5', callback_data=MetaPosCallback(pos_id='5', action='showmeta').pack())
        ]
    ])
    await message.answer('Choose position', reply_markup=pos_kb)


@router.callback_query(MetaPosCallback.filter(F.action == 'showmeta'))
async def showmeta(query: CallbackQuery, callback_data: MetaPosCallback):
    pos_id = callback_data.pos_id
    heroes = requests.get(url=f'https://dota2protracker.com/_get/herotable/pos-{pos_id}/html', headers=headers).text
    heroes = BeautifulSoup(heroes, 'lxml')
    all_heroes = heroes.find_all('div', class_='grid grid-cols-4 gap-2 py-1 px-2 bg-d2pt-gray-3 justify-start border-solid border-b border-d2pt-gray-5 text-xs font-medium')
    heroes_list = []
    for hero in all_heroes:
        name = hero.get('data-hero').strip()
        matches = int(hero.get('data-matches').strip())
        winrate = hero.find('div', class_='flex items-center justify-center text-sm font-medium').find('span').find(string=True).strip()  # don't parse heroes with wr < 50 %
        hero_list = [matches, name, winrate]
        heroes_list.append(hero_list)
    heroes_list.sort(reverse=True)
    heroes_list = heroes_list[:10]
    for hero in heroes_list:
        name = hero[1]
        matches = hero[0]
        winrate = hero[2]
        hero_kb = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text='Recent matches',
                                     callback_data=HeroIdCallback(hero_name=name, action='showrecentmatches').pack())
            ]
        ])
        await query.message.answer(f'Position: {pos_id}\n\nHero: {name}\nMatches: {matches}\nWinrate: {winrate}', reply_markup=hero_kb)
    await query.answer('Done')



