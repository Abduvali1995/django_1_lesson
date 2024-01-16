from telegram import InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import CommandHandler,CallbackQueryHandler,MessageHandler,Updater

t = "6497612120:AAGtmpJkIAxp1L8NJxVSFGMGBhWQC5GuUik"

from bs4 import BeautifulSoup
# from transliterate import translit
import requests

respons = requests.get('https://islom.uz')
soup= BeautifulSoup(respons.text,'html.parser')
def mintaqani_tanlash():
    # select tegi ichidagi optionlarni izlash
    options = soup.select('select[name="region"] option')
    print(len(options))
    # optionlarning text va value ni chiqarish
    for option in options:
        return option.text

# div_elements = soup.find_all('div', class_='a')
#
# # Har bir div ichidagi a elementlarini izlash va ma'lumotlarni chiqarish
# for div in div_elements:
#     a_elements = div.find_all('a', class_='reg')
#     for a in a_elements:
#         print(f"href: {a['href']}, text: {a.text}")



# respons = requests.get('https://islom.uz/vaqtlar/27/12')
#
# soup= BeautifulSoup(respons.text,'html.parser')
# regions = soup.find_all('tr')
# l = []
# for i in regions:
#     a = i.find_all('td')
#     b = [h.text for h in a]
#     l.append(b)
# print(l)

def star_hand(update,context):
    update.message.reply_text(text=f"Assalamu alykum {update.message.from_user.first_name}\n"
                                   f"Shahringizni tanlang",reply_markup=InlineKeyboardMarkup(city()))


def city():
    return [
        [InlineKeyboardButton(text=f"Fergana",callback_data='37'),
        InlineKeyboardButton(text=f"Toshkent",callback_data='27')],
        [InlineKeyboardButton(text=f"Namangan", callback_data='15'),
        InlineKeyboardButton(text=f"Andijon", callback_data='1')],
        [InlineKeyboardButton(text=f"Buxoro", callback_data='4'),
         InlineKeyboardButton(text=f"Samarqand", callback_data='18')],
        [InlineKeyboardButton(text=f"Jizzax", callback_data='жиззах'),
         InlineKeyboardButton(text=f"Navoiy", callback_data='14')],
        [InlineKeyboardButton(text=f"Qashqadaryo", callback_data='93'),
         InlineKeyboardButton(text=f"Qoraqqolpoq", callback_data='андижан')],
        [InlineKeyboardButton(text=f"Surxandaryo", callback_data='наманган'),
         InlineKeyboardButton(text=f"Xorazm", callback_data='андижан')],
        [InlineKeyboardButton(text=f"Guliston", callback_data='5')]
    ]
def back():
    return [
        [InlineKeyboardButton(text="Orqaga",callback_data="back1")]]

def inline_handler(update,context):
    global region_num
    query = update.callback_query
    region_num = query.data
    respons = requests.get(f'https://islom.uz/region/{region_num}')
    soup = BeautifulSoup(respons.text, 'html.parser')
    elemets = soup.find_all(class_='p_clock')
    name_namoz = soup.find_all(class_="p_v")
    context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
    buttons = []
    for i,j in zip(elemets,name_namoz):
        buttons.append([InlineKeyboardButton(text=f"{j.text} : {i.text}",callback_data='1',parse_mode="HTML")])
    buttons.append([InlineKeyboardButton(text="back",callback_data='back1')])
    query.message.reply_text(text='Namoz vaqtlari',reply_markup=InlineKeyboardMarkup(buttons))
    if query.data == "back1":
        context.bot.delete_message(chat_id=query.message.chat_id,message_id=query.message.message_id)
        query.message.reply_text(text='tanlang',reply_markup=InlineKeyboardMarkup(city()))
def main():
    updater = Updater(token=t)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start',star_hand))
    dispatcher.add_handler(CallbackQueryHandler(inline_handler))
    updater.start_polling()
    updater.idle()

if __name__=="__main__":
    main()


