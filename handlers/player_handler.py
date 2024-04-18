import json

import requests
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, CallbackQuery
from bs4 import BeautifulSoup
from forms import ProPlayer, PlayerIdCallback, Hero, MatchIdCallback
from headers_and_useragent import headers_for_stratz, headers_for_opendota

router = Router()


@router.message(F.text == 'Pro Players')
async def get_name(message: Message, state: FSMContext):
    await message.answer('Enter nickname:')
    await state.set_state(ProPlayer.name)


@router.message(ProPlayer.name)
async def get_proplayer(message: Message, state: FSMContext):
    if message.text == 'Heroes':
        await state.set_state(Hero.name)
    import re
    response = requests.get('https://docs.stratz.com/api/v1/Player/proSteamAccount', headers=headers_for_stratz)
    players = response.json()
    name = message.text.lower()
    for player_id in players:
        player = players.get(player_id)
        if name in player.get('name').lower():
            player_name = re.sub(r'[^A-Za-z0-9 ]+', '', player.get('name'))
            player_btn = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text='Stratz', web_app=WebAppInfo(
                        url=f"https://stratz.com/players/{player.get('steamAccountId')}")),
                    InlineKeyboardButton(text='Dotabuff', web_app=WebAppInfo(
                        url=f"https://www.dotabuff.com/players/{player.get('steamAccountId')}")),
                    InlineKeyboardButton(text='Dota2ProTracker', web_app=WebAppInfo(
                        url=f"https://dota2protracker.com/player/{player.get('name')}#"))
                ],
                [
                    InlineKeyboardButton(text='Recent Matches',
                                         callback_data=PlayerIdCallback(player_name=player_name, player_id=str(player.get('steamAccountId')),
                                                                        action='showrecentmatches').pack())
                ]
            ])
            await message.answer(f"Player: {player.get('name')}",
                                 reply_markup=player_btn)


@router.callback_query(PlayerIdCallback.filter(F.action == 'showrecentmatches'))
async def get_recent_matches(query: CallbackQuery, callback_data: PlayerIdCallback):
    player_name = callback_data.player_name
    try:
        matches = requests.get(url=f'https://dota2protracker.com/player/{player_name}#', headers=headers_for_stratz).text
        matches = BeautifulSoup(matches, 'lxml')
        for i in range(7):
            body = matches.find('tr', class_=f'row-{i}')
            name = body.get('name')
            hero = body.get('hero')
            proplayers = body.get('players').split(',')
            proplayers.remove(name)
            proplayers = ', '.join(proplayers)
            mmr = body.find('td', class_='td-mmr').find(string=True).strip()
            result = body.get('won').strip()
            if result == '1':
                result = 'Win'
                text = f"Player: {name}\nHero: {hero}\nAvg MMR: {mmr}\nOther pro's in game: {proplayers}\nResult: {result}\nItem Build:\n\n"
            else:
                result = 'Lose'
                text = f"Player: {name}\nHero: {hero}\nAvg MMR: {mmr}\nOther pro's in game: {proplayers}\nResult: {result}\nItem Build:\n\n"
            items = body.get('items')
            items = items.split(',')
            inventory_items = body.find('div', class_='item_build')
            for item in items:
                inventory_item_time = inventory_items.find('div', title=f'{item}').find(string=True).strip()
                text += f'{item} - {inventory_item_time}\n'
            stratz_match = body.find('td', class_='td-links').find('a', class_='info').get('href').strip()
            dotabuff_match = body.find('td', class_='td-links').find('a', class_='info dotabuff').get('href').strip()
            match_id = body.find('td', class_='td-copy').find('a', class_='copy-id').get('data').strip()
            player_kb = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text='Match On Stratz', web_app=WebAppInfo(url=stratz_match)),
                    InlineKeyboardButton(text='Match On Dotabuff', web_app=WebAppInfo(url=dotabuff_match)),
                ],
                [
                    InlineKeyboardButton(text='Copy Match ID',
                                         callback_data=MatchIdCallback(match_id=str(match_id),
                                                                       action='copymatchid').pack())
                ]
            ])
            await query.message.answer(text=text, reply_markup=player_kb)
        await query.answer('Done')
    except:
        player_id = callback_data.player_id
        recent_matches = requests.get(url=f'https://api.opendota.com/api/players/{player_id}/recentMatches', headers=headers_for_opendota).json()
        if not recent_matches:
            await query.answer('Player not found (maybe account is private)')
        else:
            await query.answer('Player not found on D2PT')
            recent_matches = recent_matches[:7]
            for recent_match in recent_matches:
                match_id = recent_match.get('match_id')
                hero_id = recent_match.get('hero_id')
                with open('static/heroes.json', 'r') as file:
                    heroes = json.load(file)
                    for hero in heroes:
                        if hero.get('id') == hero_id:
                            hero_name = hero.get('localized_name')
                kills = recent_match.get('kills')
                deaths = recent_match.get('deaths')
                assists = recent_match.get('assists')
                gpm = recent_match.get('gold_per_min')
                avg_rank = recent_match.get('average_rank')
                player_kb = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text='Match On Stratz', web_app=WebAppInfo(url=f'https://stratz.com/matches/{match_id}')),
                        InlineKeyboardButton(text='Match On Dotabuff', web_app=WebAppInfo(url=f'https://www.dotabuff.com/matches/{match_id}')),
                    ],
                    [
                        InlineKeyboardButton(text='Copy Match ID',
                                                callback_data=MatchIdCallback(match_id=str(match_id),
                                                                            action='copymatchid').pack())
                    ]
                ])
                await query.message.answer(text=f'Player: {player_name}\nHero: {hero_name}\nAverage Rank: {avg_rank}\nKills: {kills}\nDeaths: {deaths}\nAssists: {assists}\nGPM: {gpm}', reply_markup=player_kb)


@router.callback_query(MatchIdCallback.filter(F.action == 'copymatchid'))
async def get_match_id(query: CallbackQuery, callback_data: MatchIdCallback):
    import pyperclip
    match_id = callback_data.match_id
    pyperclip.copy(match_id)
    await query.answer('Match ID Copied')
