#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

import subprocess
from subprocess import Popen, PIPE
import sys, os, getopt, ast
import asyncio
import random
import telepot
import telepot.aio
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import InlineQueryResultArticle, InlineQueryResultPhoto, InputTextMessageContent

"""
"""

GlobalStarting = False

async def on_chat_message(msg):
    global GlobalStarting
    
    content_type, chat_type, chat_id,  = telepot.glance(msg)
    print('Chat:', content_type, chat_type, chat_id)

    if content_type != 'text':
        print(content_type)
        print(msg)
        if content_type == 'document':
            file_id = msg['document']['file_id']
            download_file = os.path.join('/tmp', msg['document']['file_name'])
            try:
                dest = open(download_file, 'wb')
                await bot.download_file(file_id, dest)
                dest.close()
                await bot.sendMessage(chat_id, 'Файл загружен...')
            except Exception as e:
                await bot.sendMessage(chat_id, 'Ошибки при загрузке файла!\n%s' %e)
        return

    command = msg['text'].lower()
    print(msg)
 
    remove_markup = ReplyKeyboardRemove()
    
    if command == '/exit':
        if GlobalStarting:
          await bot.sendMessage(chat_id, 'Ведь только стартовали...', 'HTML', reply_markup=remove_markup)
          GlobalStarting = False
        else:
          await bot.sendMessage(chat_id, 'Понял. Ушел...', 'HTML', reply_to_message_id=msg['message_id'], reply_markup=remove_markup)
          sys.exit(0)
    else:
        await bot.sendMessage(chat_id, 'Скоро все будет хорошо :)', 'HTML', reply_markup=remove_markup)
    GlobalStarting = False

    return

async def on_callback_query(msg):
    query_id, from_id, data = telepot.glance(msg, flavor='callback_query')
    print('Callback query:', query_id, from_id, data)
    return

def on_inline_query(msg):
    def compute():
        query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')
        print('Computing for: %s' % query_string)
    answerer.answer(msg, compute)
    return

def on_chosen_inline_result(msg):
    result_id, from_id, query_string = telepot.glance(msg, flavor='chosen_inline_result')
    print('Chosen Inline Result:', result_id, from_id, query_string)
    return

if __name__ == "__main__":
    bot_key = sys.argv[1]
    admin_id = sys.argv[2]

    bot = telepot.aio.Bot(bot_key) 
    answerer = telepot.aio.helper.Answerer(bot)

    loop = asyncio.get_event_loop()
    loop.create_task(bot.message_loop({'chat': on_chat_message,
                                       'callback_query': on_callback_query,
                                       'inline_query': on_inline_query,
                                       'chosen_inline_result': on_chosen_inline_result}))
    print('Listening ...')
    telepot.Bot(bot_key).sendMessage(admin_id, '<b>Босс</b>, если что - я на месте...', 'HTML', reply_markup = ReplyKeyboardRemove())
    GlobalStarting = True
    try:
        loop.run_forever()
    finally:
        loop.close()
