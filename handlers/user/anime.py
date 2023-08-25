from loader import dp, bot
import requests
from aiogram import types
from loguru import logger
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.db.db_utils_сhats import *
from utils.db.db_utils_warning import *

anime_query = """
           query ($id: Int,$search: String) {
              Media (id: $id, type: ANIME,search: $search) {
                id
                title {
                  romaji
                  english
                  native
                }
                description (asHtml: false)
                startDate{
                    year
                  }
                  episodes
                  season
                  type
                  format
                  status
                  duration
                  siteUrl
                  studios{
                      nodes{
                           name
                      }
                  }
                  trailer{
                       id
                       site
                       thumbnail
                  }
                  averageScore
                  genres
                  bannerImage
              }
            }
        """
        
anime_url = "https://graphql.anilist.co"

@dp.message_handler(commands=["anime", "аниме", "анимэ"], commands_prefix="/!.")
async def anime_info(message: types.Message): 
    chats = message.chat.id #Отсюда и далее, до пустой строки - выключатель этого прикола.
    chat = get_chat(chats)

    if check_chat(message.chat.id):
        create_chat(message.chat.id)
        chat = get_chat(chats)
    funny = chat[4] #проверка разрешения приколов
    if funny == 0:
        await message.answer("❌ В этом чате игры с ботом запрещены!")
        return
    
    if message.chat.type != 'private':
        warner = get_warner(message.chat.id, message.from_user.id)
        if warner == None:
            warner = [message.chat.id, message.from_user.id, 0, 0, 0]
        if warner[4] != 0:
            return
    
    anime = message.text
    find = ' '.join(anime.split(' ')[1:])
    
    variables = {"search": find}
    status_code = requests.post(anime_url, json={'query': anime_query,'variables': variables}).status_code
    
    if status_code == 200:
        anime_data = requests.post(anime_url, json={'query': anime_query,'variables': variables}).json()['data'].get('Media', None)
        anime_site = anime_data.get('siteUrl')
        image = anime_site.replace('anilist.co/anime/', 'img.anili.st/media/')
        anime_keyboard = InlineKeyboardMarkup()
        more_button = InlineKeyboardButton(text="Больше", url=anime_site)
        anime_keyboard.insert(more_button)
        
        type_en = anime_data['type']
        status_en = anime_data['status']
        description_en = str(anime_data['description']).replace('<br>', ' ')

        
        if anime_data['title']['english']:
            title = anime_data['title']['english']
        else:
            title = anime_data['title']['romaji']
        if anime_data['title']['native']:
            native_title = anime_data['title']['native']
        else:
            native_title = 'Не найдено ;)'
            
        await message.answer(f"{title} <code>({native_title})</code>\n"
                             f"Тип: <b>{type_en}</b>\n"
                             f"Оценка: <b>{anime_data['averageScore']}</b>\n"
                             f"Продолжительность: <b>{anime_data['duration']}</b>\n"
                             f"Формат: <b>{anime_data['format']}</b>\n"
                             f"Жанры: <code>{' '.join(anime_data['genres'])}</code>\n"
                             f"Статус: <b>{status_en})</b>\n\n"
                             f"Описание: <i>{description_en}</i>"
                             f"<a href='{image}'>&#xad</a>", reply_markup=anime_keyboard)
    else:
        logger.info(f"аниме не найдено --> код статуса: {status_code} \n")
        await message.answer("<code>Не найдено 😭</code>")