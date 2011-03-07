#!/usr/bin/env python

import sys
import Skype4Py
import re
import threading
import time
import os
import datetime
import codecs
import ConfigParser

Config = ConfigParser.ConfigParser()
Config.read(os.path.dirname(sys.argv[0])+"/config.ini")

skype = Skype4Py.Skype()

if not skype.Client.IsRunning:
    skype.Client.Start()
    
skype.FriendlyName = 'Gossip-Remover'

users = Config.get("UserOptions","RestrictedUsers").split(",")

skype.Attach()

theChat = skype.Chat(Config.get("Chat","Name")

removeCommand = re.compile(r"^\s*!v(v)*!", re.IGNORECASE)
hoi = re.compile(r"^\s*/h", re.IGNORECASE)
bye = re.compile(r"^\s*/b", re.IGNORECASE)
nicole = re.compile(r"^\s*/mute_nicole", re.IGNORECASE)
roman = re.compile(r"^\s*/mute_roman", re.IGNORECASE)
laura = re.compile(r"^\s*/mute_laura", re.IGNORECASE)
schwan= re.compile(r"^\s*/mute_schwan", re.IGNORECASE)
unmute = re.compile(r"^\s*/unmute", re.IGNORECASE)
leet = re.compile(r"^\s*1337", re.IGNORECASE)

mute_schwan = 0
mute_laura = 0
mute_nicole = 0
mute_roman = 0

def removeMessage(msg_id):
    message = skype.Message(msg_id)
    print message.FromHandle, msg_id
    if(message and message.IsEditable):
        print "removing message"," ", str(msg_id)
        message.Body = ""
        
def leetSpam():
    for i in range(0,20):
        print "hallo"
        theChat.SendMessage("1337")

def staythis(msg_id):
    while True:
        time.sleep(3)
        message = skype.Message(msg_id)
        print message.FromHandle, msg_id
        if(message and message.IsEditable):
            print "staying LEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEET"," ",str(msg_id)
            message.Body = "LEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEET"    
            
def removeRecentMessages():
    for chat in skype.ActiveChats:
        for message in chat.RecentMessages:
            if(message.IsEditable and removeCommand.search(message.Body)):
                removeMessage(message.Id)


def OnMessageStatus(message, status):
    global mute_schwan
    global mute_nicole
    global mute_laura
    global mute_roman

    if(status==Skype4Py.cmsSent or status==Skype4Py.cmsReceived or status==Skype4Py.cmsRead):
        print message.Id, " ", status," ",message.Chat
        
        try:
          logfile = codecs.open(os.path.dirname(__file__)+"/log.txt", "a","utf-8")
          try:
            logfile.write(str(message.Datetime)+" "+message.FromHandle+" "+message.Body+"\n")
          finally:
            logfile.close()
        except IOError:
          pass
        
        if(message.IsEditable):
            enmatsch = bye.search(message.Body)
            if(enmatsch):
              message.Body = "So.. ich gan jetzt emal hei ... ich hoffe ihr hend no en super Tag bis morn oder susch irgendwenn"  
              
            klatsch = leet.search(message.Body)
            if(klatsch):
              message.Body = "LEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEET"       
              t = threading.Timer(3, staythis, [message.Id])
              t.start()  
            if(message.FromHandle == "herr.oliver.xxx"):    
                enmatch = nicole.search(message.Body)
                if(enmatch):
                  mute_nicole = 1
                  message.Body ="well done"

                enmatch = laura.search(message.Body)
                if(enmatch):
                  mute_laura = 1
                  message.Body ="well done"

                enmatch = roman.search(message.Body)
                if(enmatch):
                  mute_roman = 1
                  message.Body ="well done"  

                enmatch = schwan.search(message.Body)
                if(enmatch):
                  mute_schwan = 1
                  message.Body ="well done"


                enmatch = unmute.search(message.Body)
                if(enmatch):
                  mute_schwan = 0
                  mute_laura = 0
                  mute_nicole = 0
                  message.Body ="well done"

            if(message.FromHandle in users):
              if(message.FromHandle == "siobhan224" and mute_schwan == 1):
                message.Body = ""
              elif(message.FromHandle == "laura.eschmann" and mute_laura == 1):
                message.Body = ""
              elif(message.FromHandle == "nicolelovescoffeee" and mute_nicole == 1):
                message.Body = ""   
              elif(message.FromHandle == "desert-storm-2000" and mute_roman == 1):
                message.Body = ""   

            enmatch = hoi.search(message.Body)
            if(enmatch):
              message.Body = "Guete Morge mitenand mir schriebed s Datum: "+str(message.Datetime)+" ich hoffe ihr sind au so guet i de Tag gstarted wie ich"

            match = removeCommand.search(message.Body)
            if(match and match.group(1)):
                removeRecentMessages()
            elif(match):
                t = threading.Timer(300, removeMessage, [message.Id])
                t.start()

def OnOnlineStatus(user,status):
    if(status != Skype4Py.olsOffline and user.Handle in users):
        print user.Handle, " changed status"
        removeRecentMessages()

skype.OnMessageStatus = OnMessageStatus
skype.OnOnlineStatus = OnOnlineStatus

removeRecentMessages()

while True:
    localtime = time.localtime(time.time())
    if(localtime[3]==13 and localtime[4]==37):
        theChat.SendMessage("1337")
    if(localtime[3]==18 and localtime[4]==00):
        theChat.SendMessage("yeee hei gah")
    time.sleep(60)
