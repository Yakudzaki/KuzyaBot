from loader import dp, bot
from aiogram import types
import openai  #pip install openai
from settings import kuzya_news_link
import requests
keys = openai.api_key = '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'
import html
import g4f

# @dp.message_handler(commands=['кузя', 'чат', 'chat'], commands_prefix="!/.")
async def chatgpt(message: types.Message):
    command = message.text.split()[0]
    promt = message.text.replace(f'{command} ', '')
    user = f"user:{message.from_user.id}" 
    
    if promt == command:
        msg = await message.reply("<b>❌ Укажите запрос!</b>")
        return
    
    response = chatgptg4f(promt, user)
    # for message in response:
    # print(response, flush=True, end='')
    print(response)
    # await message.reply(f"{html.escape(response)}\n\n<a href='https://t.me/KuzyaBotNews'>Канал с новостями 🗞</a>", disable_web_page_preview=True)


def chatgptg4f(promt, user):
    response = g4f.ChatCompletion.create(
    model = "gpt-3.5-turbo",
    messages = [{"role":  user, "content": promt}],
    stream = False
    )
    return response


@dp.message_handler(commands=['img'], commands_prefix="!/.")
async def handle_chat(message: types.Message):
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