from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
ua = UserAgent()

headers_for_stratz = {
    'User-Agent': f'{ua.random}'
    # 'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJTdWJqZWN0IjoiNzVmODYxYzktMWFlZi00NmRmLTliZDYtYzY0NWFiOGE5NDQwIiwiU3RlYW1JZCI6IjExNTEwNjcxODYiLCJuYmYiOjE3MTAwNTkxMTIsImV4cCI6MTc0MTU5NTExMiwiaWF0IjoxNzEwMDU5MTEyLCJpc3MiOiJodHRwczovL2FwaS5zdHJhdHouY29tIn0.84meNwXgF6YuVOIVKLo7v3GhlK4uvmnZqYM7zfNa_s4'
}
hero_info = requests.get(url=f'https://dota2protracker.com/hero/Dark Willow/new', headers=headers_for_stratz).text
hero_info = BeautifulSoup(hero_info, 'lxml')
# builds_divs = hero_info.find('div', class_='flex mb-2 flex-col p-4 gap-2 rounded-md bg-d-gray-5 border-[1px] border-solid border-d-gray-8')
builds_divs = hero_info.find('div', class_='flex mb-2 flex-col p-4 gap-2 rounded-md bg-d-gray-5 border-[1px] border-solid border-d-gray-8', style='grid-column: 1 / span 2;')
# abilities_build = builds_divs[0]
print(builds_divs)
# abilities = abilities_build.find_all('div', class_='flex w-[28px] h-[28px]')
# for ability in abilities:
#     skill = ability.find('img').get('title')
#     print(skill)
#     # last one is useless
# talents = abilities_build.find_all('div', class_='talent-tree-lvl')
# for talent in talents:
#     activated_talent = talent.find('div', class_='active-node').find(string=True)
#     print(activated_talent)
# builds = hero_info.find('div', class_='flex flex-col xl:w-1/2')
# core_builds = builds.find_all('div', class_='flex mb-2 flex-col p-4 gap-2 rounded-md bg-d-gray-5 border-[1px] border-solid border-d-gray-8')
# for build in core_builds:
#     print(build.find('div', class_='flex font-bold').find(string=True))

# abilities_build = hero_info.find('div', class_='text-[10px] flex flex-col 2xs:flex-row 2xs:justify-center md:justify-start items-center gap-1')
abilities = abilities_build.find('div', class_='flex gap-1')
abilities = abilities.find_all('div', class_='flex w-[28px] h-[28px]')
ab_names = []
for ability in abilities:
    ability_name = ability.find('img').get('title')
    ab_names.append(ability_name)
ab_names.pop()
for ab in ab_names:
    print(ab)

# talents = abilities_build.find('div', class_='flex talent')
# print(talents)
# talents = talents.find_all('div', class_='talent-tree-lvl')
# for talent in talents:
#     talent_name = talent.find('div', class_='active-node').find(string=True)
#     print(talent_name)

item_build = builds_divs[1]
items = item_build.find_all('div', class_='flex flex-col')
for item in items:
    item_name = item.find('div', class_='item-row-top w-[32px] h-[24px]').get('title')
    item_time = item.find('div', class_='flex text-cente text-[10px]').find(string=True).strip()
    item_percent = item.find('div', class_='item-row-bottom text-center').find(string=True).strip()
    print(f'{item_name} - {item_time} - {item_percent}')

# troubles with dark willow and dark seer

# hero_info = requests.get(url=f'https://dota2protracker.com/hero/{hero}/new', headers=headers).text
    # hero_info = BeautifulSoup(hero_info, 'lxml')
    # builds_div = hero_info.find('div', class_='flex flex-col xl:w-1/2')
    # builds = builds_div.find_all('div',
    #                              class_='flex flex-col p-4 gap-2 rounded-md bg-d-gray-5 border-[1px] border-solid border-d-gray-8 col-span-2')
    # for build in builds:
    #     build_name = build.find('div', class_='flex').find(string=True)
    #     text = f'{build_name}\n\n'
    #     items = build.find_all('div', class_='flex flex-col gap-2 bg-d2pt-gray-1 p-2 rounded-md border-one')
    #     for item in items:
    #         item_name = item.find('div',
    #                               class_='w-[32px] h-[24px] text-xs text-white text-shadow font-medium text-right rounded-md').get(
    #             'style').split(';')[0].split('/')[-1].split("'")[0].split('.')[0].split('_')
    #         item_name = ' '.join(item_name).title()
    #         percent = item.find('div', class_='flex justify-center text-xs text-white').find(string=True).strip()
    #         text += f'{item_name} - {percent}\n'
    #     await query.message.answer(text=text)
    # await query.answer(text='Done')

