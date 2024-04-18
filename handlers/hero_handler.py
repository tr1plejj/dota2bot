import requests
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, WebAppInfo
import json
from bs4 import BeautifulSoup
from forms import Hero, ProPlayer, HeroIdCallback, MatchIdCallback
from headers_and_useragent import headers

router = Router()


@router.message(F.text == 'Heroes')
async def get_hero(message: Message, state: FSMContext):
    await message.answer('Enter hero name:')
    await state.set_state(Hero.name)


@router.message(Hero.name)
async def find_heroes(message: Message, state: FSMContext):
    if message.text == 'Pro Players':
        await message.answer('Enter nickname:')
        await state.set_state(ProPlayer.name)
    name = message.text.lower()
    with open('static/heroes.json', 'r') as file:
        heroes = json.load(file)
        for hero in heroes:
            hero_name = hero.get('localized_name')
            if name in hero_name.lower():
                hero_kb = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text='Show recent matches', callback_data=HeroIdCallback(hero_name=str(hero.get('localized_name')), action='showrecentmatches').pack())
                    ],
                    [
                        InlineKeyboardButton(text='Show top item and ability build',
                                             callback_data=HeroIdCallback(hero_name=str(hero.get('localized_name')),
                                                                          action='showtopbuild').pack())
                    ]
                ])
                await message.answer(text=hero_name, reply_markup=hero_kb)

# parse data for recent matches on hero https://dota2protracker.com/hero/Anti-Mage#
# make start item build + make popular build (maybe pars ability build)


@router.callback_query(HeroIdCallback.filter(F.action == 'showrecentmatches'))
async def get_recent_matches(query: CallbackQuery, callback_data: HeroIdCallback):
    hero_name = callback_data.hero_name
    page = requests.get(f'https://dota2protracker.com/hero/{hero_name}#', headers=headers).text
    soup = BeautifulSoup(page, 'lxml')
    for i in range(7):
        body = soup.find('tr', class_=f'row-{i}')
        name = body.get('name')
        mmr = body.find('td', class_='td-mmr').find(string=True).strip()
        proplayers = body.get('players').split(',')
        proplayers.remove(name)
        proplayers = ', '.join(proplayers)
        result = body.get('won').strip()
        if result == '1':
            result = 'Win'
            text = f"Player: {name}\nHero: {hero_name}\nAvg MMR: {mmr}\nOther pro's in game: {proplayers}\nResult: {result}\nItem Build:\n\n"
        else:
            result = 'Lose'
            text = f"Player: {name}\nHero: {hero_name}\nAvg MMR: {mmr}\nOther pro's in game: {proplayers}\nResult: {result}\nItem Build:\n\n"
        items = body.get('items')
        items = items.split(',')
        inventory_items = body.find('div', class_='item_build')
        for item in items:
            inventory_item_time = inventory_items.find('div', title=f'{item}').find(string=True).strip()
            text += f'{item} - {inventory_item_time}\n'
        stratz_match = body.find('td', class_='td-links').find('a', class_='info').get('href').strip()
        dotabuff_match = body.find('td', class_='td-links').find('a', class_='info dotabuff').get('href').strip()
        match_id = body.find('td', class_='td-copy').find('a', class_='copy-id').get('data').strip()
        matches_kb = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text='Match On Stratz', web_app=WebAppInfo(url=stratz_match)),
                InlineKeyboardButton(text='Match On Dotabuff', web_app=WebAppInfo(url=dotabuff_match))
            ],
            [
                InlineKeyboardButton(text='Copy Match ID',
                                     callback_data=MatchIdCallback(match_id=str(match_id), action='copymatchid').pack())
            ]
        ])
        await query.message.answer(text=text, reply_markup=matches_kb)


@router.callback_query(MatchIdCallback.filter(F.action == 'copymatchid'))
async def get_match_id(query: CallbackQuery, callback_data: MatchIdCallback):
    import pyperclip
    match_id = callback_data.match_id
    pyperclip.copy(match_id)
    await query.answer('Match ID Copied')


@router.callback_query(HeroIdCallback.filter(F.action == 'showtopbuild'))
async def show_top_build(query: CallbackQuery, callback_data: HeroIdCallback):
    try:
        hero = callback_data.hero_name
        hero_info = requests.get(url=f'https://dota2protracker.com/hero/{hero}/new',
                                 headers=headers).text
        hero_info = BeautifulSoup(hero_info, 'lxml')
        builds_divs = hero_info.find_all('div',
                                         class_='flex mb-2 flex-col p-4 gap-2 rounded-md bg-d-gray-5 border-[1px] border-solid border-d-gray-8')
        abilities_build = builds_divs[0]
        abilities = abilities_build.find('div', class_='flex gap-1')
        abilities = abilities.find_all('div', class_='flex w-[28px] h-[28px]')
        ab_names = []
        for ability in abilities:
            ability_name = ability.find('img').get('title')
            ab_names.append(ability_name)
        ab_names.pop()
        abilities_text = 'Abilities build\n\n'
        for ab in ab_names:
            abilities_text += f'{ab}\n'
        await query.message.answer(text=abilities_text)

        talents = abilities_build.find('div', class_='flex talent')
        talents = talents.find_all('div', class_='talent-tree-lvl')
        talents_text = 'Talent tree\n\n'
        for talent in talents:
            talent_name = talent.find('div', class_='active-node').find(string=True)
            talents_text += f'{talent_name}\n'
        await query.message.answer(text=talents_text)

        item_build = builds_divs[1]
        item_build_text = 'Item build\n\n'
        items = item_build.find_all('div', class_='flex flex-col')
        for item in items:
            item_name = item.find('div', class_='item-row-top w-[32px] h-[24px]').get('title')
            item_time = item.find('div', class_='flex text-cente text-[10px]').find(string=True).strip()
            item_percent = item.find('div', class_='item-row-bottom text-center').find(string=True).strip()
            item_build_text += f'{item_name} - {item_time} - {item_percent}\n'
        await query.message.answer(text=item_build_text)
        await query.answer('Done')
    except:
        await query.answer('Error')
