import json

import pandas as pd
from openpyxl import Workbook
import datetime
from bs4 import BeautifulSoup
import requests
import aiofiles, asyncio
from aiocsv import AsyncWriter

async def get_data():

    url = 'https://select.by/kurs'
    try:
        req = requests.get(url)
        src = req.text
    except Exception as e:
        print(e)

    with open('page.html','w') as file:
        file.write(src)


    with open('page.html') as fp:
        file = fp.read()

    soup = BeautifulSoup(file,'lxml')
    bank_head = soup.find(class_='head-sort_i_first').find('th')
    table_head = soup.find(class_='head-sort_i_first').find_all('a')
    BANK = bank_head.text
    USD = table_head[0].text
    EUR = table_head[1].text
    RUB = table_head[2].text
    date = datetime.date.today()
    date = str(date)

    async with aiofiles.open('course.csv', 'a', encoding='UTF-8') as csv_file:
        await csv_file.truncate(0)
        writer = AsyncWriter(csv_file)
        await writer.writerow(
            (
                "DATE:",
                date,
                BANK,
                USD,
                " ",
                EUR,
                "  ",
                RUB,
                "   "
             )
        )
    find_all_courses = soup.find_all(class_='tablesorter-hasChildRow')

    bank_data_json = []
    for item in find_all_courses:
        item_course = item.find_all('td')
        bank = item_course[0].find('a').text
        if bank == '':
            bank = 'imbanking'
        USD = item_course[1].text
        USD2 = item_course[2].text
        EUR = item_course[3].text
        EUR2 = item_course[4].text
        RUB = item_course[5].text
        RUB2 = item_course[6].text


        bank_data_json.append(
            {
                "Date":date,
                "Bank":bank,
                'USD sell':USD,
                'USD buy':USD2,
                'EUR sell':EUR,
                'EUR buy': EUR2,
                'RUB sell':RUB,
                'RUB buy': RUB2
            }
        )

        async with aiofiles.open('course.csv', 'a', encoding='UTF-8') as csv_file:
            writer = AsyncWriter(csv_file)
            await writer.writerow(
                (   " ",
                    " ",
                    bank,
                    USD,
                    USD2,
                    EUR,
                    EUR2,
                    RUB,
                    RUB2

                 )
            )
        with open('course.json', 'a', encoding='UTF-8') as json_file:
                json_file.truncate(0)
                json.dump(bank_data_json,json_file,indent=4, ensure_ascii=False)

    return bank_data_json



async def convert_to_xls():
    read_file = pd.read_csv('course.csv')
    read_file.to_excel('exel_currency.xlsx', index=None, header=True)

    return 'exel_currency.xlsx'


async def main():
    await get_data()
    await convert_to_xls()


if __name__ == "__main__":
    asyncio.run(main())