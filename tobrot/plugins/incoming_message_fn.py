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
LOGGER = logging.getLogger(__name__)


import os

from tobrot import (
    DOWNLOAD_LOCATION
)
import asyncio
import subprocess
import pyrogram
import time
from tobrot.helper_funcs.extract_link_from_message import extract_link
# from tobrot.helper_funcs.download_aria_p_n import call_apropriate_function, aria_start
from tobrot.helper_funcs.download_from_link import request_download
from tobrot.helper_funcs.display_progress import progress_for_pyrogram
from tobrot.helper_funcs.youtube_dl_extractor import extract_youtube_dl_formats
from subprocess import call
from tobrot.helper_funcs.upload_to_tg import upload_to_tg

async def incoming_message_f(client, message):
    """/leech command"""
    i_m_sefg = await message.reply_text("processing", quote=True)
    is_zip = False
    is_unzip = False
    if len(message.command) > 1:
        if message.command[1] == "archive":
            is_zip = True
        elif message.command[1] == "unzip":
            is_unzip = True
    # get link from the incoming message
    if message.reply_to_message.document:
      hell = await message.reply_to_message.download(
        file_name = DOWNLOAD_LOCATION
        )
      sent_message_to_update_tg_p = i_m_sefg
      current_user_id = message.from_user.id
      new_download_location = os.path.join(DOWNLOAD_LOCATION,str(current_user_id),str(time.time()))
                
                
                
              
      if not os.path.isdir(new_download_location):
          os.makedirs(new_download_location)
      new_download_location = new_download_location + "/"
      #i_m_sefg = await message.reply_text(text=hell, quote=True)
      with open (hell) as foe:
        for rec in foe:
          url = rec
          
          
          command =[
               "youtube-dl",
               "--no-warnings",
               "--console-title",
               #"--min-sleep-interval=10",
               #"--max-sleep-interval=20",
               "-o"+new_download_location,
               url
          ]   
      process = call(command, shell=False)
      to_upload_file = new_download_location
      response = {}
      LOGGER.info(response)
      user_id = sent_message_to_update_tg_p.reply_to_message.from_user.id
      final_response = await upload_to_tg(sent_message_to_update_tg_p,to_upload_file,user_id,response)
                  
                  
                  
                  
    else:
      pass

   

async def incoming_youtube_dl_f(client, message):
    """ /ytdl command """
    i_m_sefg = await message.reply_text("processing", quote=True)
    # LOGGER.info(message)
    # extract link from message
    dl_url, cf_name = extract_link(message.reply_to_message)
    LOGGER.info(dl_url)
    LOGGER.info(cf_name)
    if dl_url is not None:
        await i_m_sefg.edit_text("extracting links")
        current_user_id = message.from_user.id
        # create an unique directory
        user_working_dir = os.path.join(DOWNLOAD_LOCATION, str(current_user_id))
        # create download directory, if not exist
        if not os.path.isdir(user_working_dir):
            os.makedirs(user_working_dir)
        # list the formats, and display in button markup formats
        text_message, reply_markup = await extract_youtube_dl_formats(
            dl_url,
            user_working_dir
        )
        await i_m_sefg.edit_text(
            text=text_message,
            reply_markup=reply_markup
        )
    else:
        # if no links found, delete the "processing" message
        await i_m_sefg.delete()
