#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

# the logging things
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)

import os

from tobrot import (
    DOWNLOAD_LOCATION,
    TG_BOT_TOKEN,
    APP_ID,
    API_HASH,
    AUTH_CHANNEL
)

from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from tobrot.plugins.new_join_fn import help_message_f
from tobrot.plugins.incoming_message_fn import incoming_message_f, incoming_youtube_dl_f

from tobrot.plugins.call_back_button_handler import button
from tobrot.plugins.custom_thumbnail import (
    save_thumb_nail,
    clear_thumb_nail
)


if __name__ == "__main__" :
    # create download directory, if not exist
    if not os.path.isdir(DOWNLOAD_LOCATION):
        os.makedirs(DOWNLOAD_LOCATION)
    #
    app = Client(
        "my_first_bot",
        bot_token=TG_BOT_TOKEN,
        api_id=APP_ID,
        api_hash=API_HASH,
        workers=343
    )
    #
    incoming_message_handler = MessageHandler(
        incoming_message_f,
        filters=filters.command(["leech"]) & filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(incoming_message_handler)
    #
    incoming_youtube_dl_handler = MessageHandler(
        incoming_youtube_dl_f,
        filters=filters.command(["ytdl"]) & filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(incoming_youtube_dl_handler)
   
    
 

    help_text_handler = MessageHandler(
        help_message_f,
        filters=filters.command(["help"]) & filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(help_text_handler)
    

    group_new_join_handler = MessageHandler(
        help_message_f,
        filters=filters.chat(chats=AUTH_CHANNEL) & filters.new_chat_members
    )
    app.add_handler(group_new_join_handler)
    #
    call_back_button_handler = CallbackQueryHandler(
        button
    )
    app.add_handler(call_back_button_handler)
    #
    save_thumb_nail_handler = MessageHandler(
        save_thumb_nail,
        filters=filters.command(["savethumbnail"]) & filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(save_thumb_nail_handler)
    #
    clear_thumb_nail_handler = MessageHandler(
        clear_thumb_nail,
        filters=filters.command(["clearthumbnail"]) & filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(clear_thumb_nail_handler)
    #
    app.run()
