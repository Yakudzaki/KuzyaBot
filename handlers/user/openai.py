from loader import dp, bot
from aiogram import types
import openai  #pip install openai
from settings import kuzya_news_link, botik_id
import requests
keys = openai.api_key = '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'
import html
import g4f
from utils.db.db_utils_users import *
from utils.db.db_utils_warning import *
from utils.db.db_utils_сhats import *
from ..f_lib.other import is_sub

@dp.message_handler(commands=['кузя', 'чат', 'chat'], commands_prefix="!/.")
async def chatgpt(message: types.Message):
    if message.chat.type != 'private':
        chats = message.chat.id #Отсюда и далее, до пустой строки - выключатель этого прикола.
        chat = get_chat(chats)
        if check_chat(message.chat.id):
            create_chat(message.chat.id)
            chat = get_chat(chats)
    
        funny = chat[4] #проверка разрешения приколов
        if not funny:
            await message.answer("❌ В этом чате игры с ботом запрещены!")
            return
        
        warner = get_warner(message.chat.id, message.from_user.id)
        if warner == None:
            warner = [message.chat.id, message.from_user.id, 0, 0, 0]
        if warner[4] != 0:
            return
    sub = await is_sub(message)
    if sub == False:
        return 1
    
    if message.reply_to_message and message.reply_to_message.from_user.id == botik_id and not message.text.startswith("!") and not message.text.startswith(".") and not message.text.startswith("/"):
        promt = message.text
    
    else:
        command = message.text.split()[0]
        promt = message.text.replace(f'{command} ', '')
        if promt == command:
            msg = await message.reply("<b>❌ Укажите запрос!</b>")
            return 1
    
    user = f"{message.from_user.first_name}" 
    await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)

    response = await chatgptg4f(promt, user)
    # for message in response:
    # print(response, flush=True, end='')
    # print(response)
    # await message.reply(f"{html.escape(response)}\n\n<a href={kuzya_news_link}>Канал с новостями 🗞</a>", disable_web_page_preview=True)
    if f"{response}" == "":
        response = "Без комментариев!"
    await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
    await message.reply(f"{response}\n\nКузяGpt", disable_web_page_preview=True, parse_mode='Markdown')
    return 1

async def chatgptg4f(promt, user):
    response = await g4f.ChatCompletion.create_async(
    model = "gpt-3.5-turbo",
    messages = [{"role":  user, "content": promt}],
    stream = False
    )
    return response


@dp.message_handler(commands=['img'], commands_prefix="!/.")
async def handle_chat(message: types.Message):
    if message.chat.type != 'private':
        chats = message.chat.id #Отсюда и далее, до пустой строки - выключатель этого прикола.
        chat = get_chat(chats)
        if check_chat(message.chat.id):
            create_chat(message.chat.id)
            chat = get_chat(chats)
    
        funny = chat[4] #проверка разрешения приколов
        if not funny:
            await message.answer("❌ В этом чате игры с ботом запрещены!")
            return
        
        warner = get_warner(message.chat.id, message.from_user.id)
        if warner == None:
            warner = [message.chat.id, message.from_user.id, 0, 0, 0]
        if warner[4] != 0:
            return
    
    
    result = process_img_step(message.text.replace('/img',  '').replace("!img", ""))
    text_photo = message.text.replace('/img',  '').replace("!img", "")
    if result == 'no key':
        await message.reply('<b>⛱️ ChatGpt в отпуске!</b> (тех. работы)', disable_web_page_preview=True, parse_mode='html')
        return
    elif result == 'limit':
        await message.reply(f"<b>Вы не можете отправлять сообщения больше 60 символов</b>!")
    elif result == 'bad':
        await message.reply(f"<b>❌ Не удалось сгенерировать картинку</b>!")
    else:
        await bot.send_photo(message.chat.id, result, f"Текст генерации: {text_photo}", reply_to_message_id=message.message_id)


def process_img_step(messages):
    if len(messages) >= 61:
        return "limit"
    
    while True:
        try:
            response = requests.post(
                'https://api.openai.com/v1/images/generations',
                headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {keys}'},
                json={'model': 'image-alpha-001', 'prompt': messages}
            )
            response_json = response.json()
            image_url = response_json['data'][0]['url']
            return image_url

        except Exception as er:
            print(er)
            if str(er) == "You exceeded your current quota, please check your plan and billing details.":
                return "bad"
            elif "Incorrect API key provided" in str(er):
                return "bad"
                
            else:
                return 'bad'
                

def process_chat_step(messages):
    if len(messages) >= 10001:
        return "limit"
    while True:
        try:
            chat_response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=messages,
                max_tokens=2400,
                n=1,
                stop=None,
                temperature=0.3
            )
            return chat_response["choices"][0]["text"]

        except Exception as er:
            print(er)
            if str(er) == "You exceeded your current quota, please check your plan and billing details.":
                return "error"
            elif "Incorrect API key provided" in str(er):
                return "error"
            else:
            	return f"Была вызвана ошибка: {str(er)}"


def process_edit_step(messages):
    while True:
        try:
            openai.api_key = keys
            chat_response = openai.Image.create_variation(
                image=open(f"{messages}", "rb"),
                n=1,
                size="1024x1024"
            )
            return chat_response['data'][0]['url']

        except Exception as er:
            print(er)
            if str(er) == "You exceeded your current quota, please check your plan and billing details.":
                return "error"
            elif "Incorrect API key provided" in str(er):
                return "error"
            else:
            	return f"error"