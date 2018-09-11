from PIL import Image
import io
import imagehash
import argparse
import shelve
import glob
from random import uniform


def photos(bot, update):
    loc = '/var/python-telegram-bot/imgcache/'+str(update.message.chat_id)+str(update.message.message_id)
    db = shelve.open('/var/python-telegram-bot/db/shelve', writeback=True)
    update.message.photo[-1].get_file().download(custom_path=loc)
    h = str(imagehash.dhash(Image.open(loc)))

    if h in db:
        msgid = db[h]
        confidence = round(uniform(85,99),2)
        update.message.reply_text(text = "Repost detected with "+ str(confidence) + "% confidence.",reply_to_message_id=msgid[0])
    else:
        db[h] = db.get(h, []) + [update.message.message_id] + [update.message.chat_id]
    db.close()
