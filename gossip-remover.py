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

theChat = skype.Chat(Config.get("Chat","Name"))

removeCommand = re.compile(r"^\s*!v(v)*!", re.IGNORECASE)

def removeMessage(msg_id):
    message = skype.Message(msg_id)
    print message.FromHandle, msg_id
    if(message and message.IsEditable):
        print "removing message"," ", str(msg_id)
        message.Body = ""
        
def removeRecentMessages():
    for chat in skype.ActiveChats:
        for message in chat.RecentMessages:
            if(message.IsEditable and removeCommand.search(message.Body)):
                removeMessage(message.Id)

def OnMessageStatus(message, status):
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
              
            match = removeCommand.search(message.Body)
            if(match and match.group(1)):
                removeRecentMessages()
            elif(match):
                t = threading.Timer(20, removeMessage, [message.Id]) 
                t.start()

def OnOnlineStatus(user,status):
    if(status != Skype4Py.olsOffline and user.Handle in users):
        print user.Handle, " changed status"
        removeRecentMessages()

skype.OnMessageStatus = OnMessageStatus
skype.OnOnlineStatus = OnOnlineStatus

removeRecentMessages()

while True:
    time.sleep(60)
