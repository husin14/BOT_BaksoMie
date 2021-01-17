# -*- coding: utf-8 -*-
"""
This Example will show you how to use register_next_step handler.
"""

import telebot
import time
from telebot import types

TOKEN = '1407437021:AAHiFWk4fj4_f1FM16FDJH7NmE-PQwaRo9s'

bot = telebot.TeleBot(TOKEN)

user_dict = {}


commands = {  # command description used in the "help" command
    'start'         : 'memulai bot',
    'hargamakan'    : 'memberi harga makanan yang dijual',
    'hargaminum'    : 'memberi harga minuman yang dijual',
    'pesan'         : 'memesan makanan',
    'alamat'        : 'alamat warung Bakso Boedjangan',
    'video'         : 'Video Overview Bakso Boedjangan'
}

hargalistmakan = ['Mie Ayam', 'Bakso' , 'Mie Ayam Bakso' ]
hargalistminum = ['Es Teh' , 'Es Jeruk' ]

hargamakan = types.ReplyKeyboardMarkup(one_time_keyboard=True)  
hargaminum = types.ReplyKeyboardMarkup(one_time_keyboard=True)
hargamakan.add('Mie Ayam','Bakso', 'Mie Ayam Bakso')
hargaminum.add('Es Teh','Es Jeruk')
hideBoard = types.ReplyKeyboardRemove()


class User:
    def __init__(self, name):
        self.name = name
        self.panganan = None
        self.minuman = None
       

# Handle '/start' 

@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    bot.send_message(cid, "Selamat datang di warung Bakso Boedjangan")
    bot.send_chat_action(cid, 'typing')  # show the bot "typing" (max. 5 secs)
    time.sleep(1)
    menubot = "berikut list perintah yang tersedia\n"
    for key in commands:  # generate help text out of the commands dictionary defined at the top
        menubot += "/" + key + ": "
        menubot += commands[key] + "\n"
    bot.send_message(cid, menubot)

@bot.message_handler(commands=['hargamakan'])
def perintahhargamakan(m):
    cid = m.chat.id
    bot.send_message(cid,'berikut list harga yang kami sediakan',reply_markup=hargamakan)

@bot.message_handler(commands=['alamat'])
def command_alamat(m):
    cid = m.chat.id
    bot.send_chat_action(cid, 'typing')  # show the bot "typing" (max. 5 secs)
    time.sleep(1)
    bot.send_message(cid, "Jl. MT. Haryono No.886, Peterongan, Kec. Semarang Sel., Kota Semarang, Jawa Tengah 50242")
    bot.send_chat_action(cid, 'typing')  # show the bot "typing" (max. 5 secs)
    time.sleep(1)
    bot.send_message(cid, "Berikut akan kami kirimkan lokasi warung kami.. Tunggu sebentar kak")

    # bot.send_video(cid, open('alamat.mp4', 'rb'))
    bot.send_location(cid,-6.9973984,110.4278288)

@bot.message_handler(commands=['video'])
def command_video(m):
    cid = m.chat.id
    bot.send_chat_action(cid, 'typing')  # show the bot "typing" (max. 5 secs)
    time.sleep(1)
    bot.send_message(cid, "Berikut video Tentang Bakso Boedjangan")
    time.sleep(1)

    bot.send_video(cid, open('baksovideo.mp4', 'rb'))
    
   
    
@bot.message_handler(func=lambda m : m.text in hargalistmakan)
def listhargamakan(m):
    cid = m.chat.id
    text = m.text 
 
    bot.send_chat_action(cid, 'typing')

    if text == 'Mie Ayam':  
        bot.send_photo(cid, open('mieayam.jpg', 'rb'),reply_markup=hideBoard) 
        bot.send_message(cid,'\n Harga Mie Ayam = Rp. 8.000')
    elif text == 'Bakso':
        bot.send_photo(cid, open('bakso.jpg', 'rb'), reply_markup=hideBoard)
        bot.send_message(cid,'\n Harga Bakso = Rp. 10.000')
    elif text == 'Mie Ayam Bakso':
        bot.send_photo(cid, open('mieayambakso.jpg', 'rb'), reply_markup=hideBoard) 
        bot.send_message(cid,'\n Harga Mie Ayam Bakso = Rp. 13.000')  
    else:
        bot.send_message(cid, "Not Defined!")
        bot.send_message(cid, "Please try again")


@bot.message_handler(commands=['hargaminum'])
def perintahhargaminum(m):
    cid = m.chat.id
    bot.send_message(cid,'berikut list harga yang kami sediakan',reply_markup=hargaminum)
   
    
@bot.message_handler(func=lambda m : m.text in hargalistminum)
def listhargaminum(m):
    cid = m.chat.id
    text = m.text
 
    bot.send_chat_action(cid, 'typing')

    if text == 'Es Teh':  
        bot.send_photo(cid, open('esteh.jpg', 'rb'),reply_markup=hideBoard) 
        bot.send_message(cid,'\n Harga Es Teh = Rp. 2500')
    elif text == 'Es Jeruk':
        bot.send_photo(cid, open('esjeruk.jpg', 'rb'), reply_markup=hideBoard)
        bot.send_message(cid,'\n Harga Es Jeruk = Rp. 4000')  
    else:
        bot.send_message(cid, "Not Defined!")
        bot.send_message(cid, "Please try again")

@bot.message_handler(commands=['pesan'])
def send_welcome(message):
    cid = message.chat.id
    msg = bot.reply_to(message,'Oke, mari saya bantu anda untuk memesan makanan')
    msg = bot.send_message(cid ,'Siapa Nama Anda?')
    
    bot.register_next_step_handler(msg, process_name_step)
   

def process_name_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        user = User(name)
        user_dict[chat_id] = user  
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Mie Ayam','Bakso','Mie Ayam Bakso')
        msg = bot.reply_to(message, user.name+ '. Makanan apa yang ingin anda pesan?',reply_markup=markup)
        bot.register_next_step_handler(msg, process_panganan_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')
        


def process_panganan_step(message):
    try:
        chat_id = message.chat.id
        panganan = message.text
        hargamakan = message.text
        user = user_dict[chat_id]
        if (panganan == u'Bakso'):
            user.hargamakan = 10000
            user.panganan = panganan
        elif (panganan == u'Mie Ayam'):
            user.hargamakan = 7000
            user.panganan = panganan
        elif (panganan == u'Mie Ayam Bakso'):
            user.hargamakan = 15000
            user.panganan = panganan

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Es Teh', 'Es Jeruk')
        msg = bot.reply_to(message, 'Pilih Minuman yang mana?',reply_markup=markup)
        bot.register_next_step_handler(msg,process_minuman_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_minuman_step(message):
    try:
        chat_id = message.chat.id
        minuman = message.text
        hargaminum = message.text
        user = user_dict[chat_id]
        if (minuman == u'Es Teh'): 
            user.hargaminum = 2500
            user.minuman = minuman
        elif (minuman == u'Es Jeruk') :
            user.hargaminum = 4000
            user.minuman = minuman
        else:
            raise Exception()
        bot.send_message(chat_id, 'List Pesanan : \n' +'Nama pemesan = ' +user.name+ '\n Makanan yang dipesan :' +user.panganan+ ' harga = '+str(user.hargamakan)+  '\n Minuman yang dipesan :'+user.minuman+' harga =  ' +str(user.hargaminum)+ '\n Total harga = {}'.format(user.hargaminum+user.hargamakan) )
        bot.send_message(chat_id,'\n Terima kasih telah makan di Warung Mie Ayam Bakso mang Ujang')
        
    except Exception as e:
        bot.reply_to(message, 'oooops')



  




        


# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
# bot.load_next_step_handlers()

bot.polling()
