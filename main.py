import telebot
import os.path
from telebot import types

import delayed
import mytime

config = {
    "name": "HappyRSPBot",
    "token": "5981874060:AAGgIW_t1oiUMuVZSJQLSpWKE3l7MzOqk4o"
}

happy_rsp = telebot.TeleBot(config["token"])

@happy_rsp.message_handler(content_types=['text'])
def step7(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Registration")
    btn2 = types.KeyboardButton("Autorization")
    btn3 = types.KeyboardButton("START")
    markup.add(btn1, btn2, btn3)
    happy_rsp.send_message(message.chat.id, "Use 'Registration' or 'Autorization' to see the common report")
    happy_rsp.send_message(message.chat.id, "Or START to work with or without autorization", reply_markup=markup)
    happy_rsp.register_next_step_handler(message, get_text)

@happy_rsp.message_handler(content_types=['text'])
def get_text(message):
    if message.text == "START":
        inlines = telebot.types.InlineKeyboardMarkup()
        happy_rsp.send_message(message.chat.id, "Hello!")
        inlines.add(telebot.types.InlineKeyboardButton(text='Just a bit', callback_data="High"))
        inlines.add(telebot.types.InlineKeyboardButton(text='Have some time', callback_data="Medium"))
        inlines.add(telebot.types.InlineKeyboardButton(text='Have enough time', callback_data="Low"))
        happy_rsp.send_message(message.chat.id, "How much time do you have?", reply_markup=inlines)
    elif message.text == "Registration":
        happy_rsp.send_message(message.chat.id, "Choose your password")
        happy_rsp.register_next_step_handler(message, get_password)
    elif message.text == "Autorization":
        happy_rsp.send_message(message.chat.id, "What's your password?")
        happy_rsp.register_next_step_handler(message, check_password)

def get_password(message):
    password = message.text
    myid = str(message.from_user.id)
    path = os.path.join("", myid + "password.txt")
    file = open(path, "w")
    file.write(password)
    file.close()
    happy_rsp.send_message(message.chat.id, "Thanks for registration! Do you want to continue?")
    happy_rsp.register_next_step_handler(message, step7)

def check_password(message):
    password = message.text
    myid = str(message.from_user.id)
    path = os.path.join("", myid + "password.txt")
    file = open(path, "r")
    passw = file.readline()
    file.close()
    if password == passw:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton("Common report")
        markup.add(btn)
        happy_rsp.send_message(message.chat.id, "You can check your common report now",
                               reply_markup=markup)
        happy_rsp.register_next_step_handler(message, step8)
    else:
        happy_rsp.send_message(message.chat.id, "Password isn't correct")
        happy_rsp.send_message(message.chat.id, "Do you want to try again?")
        happy_rsp.register_next_step_handler(message, step7)


def step8(message):
    if message.text == 'Common report':
        delayed.delayed.common_report(myid=str(message.from_user.id))
        happy_rsp.send_message(message.chat.id, delayed.delayed.status)
    happy_rsp.send_message(message.chat.id, "Say anything if you want to start working")
    happy_rsp.register_next_step_handler(message, step7)

@happy_rsp.callback_query_handler(func=lambda call: call.data in ['High', 'Medium', 'Low'])
def step1(call):
    myid = str(call.from_user.id)
    mytime.mytime.get_tasks_today(thisday=mytime.mytime.thisday, todaylist=mytime.mytime.todaylist)
    if call.data == "High":

        clean_file(myid=str(call.from_user.id))
        mytime.mytime.get_high(todaylist=mytime.mytime.todaylist, myid=str(call.from_user.id))
        set_future(myid=myid)
    elif call.data == "Medium":

        clean_file(myid=str(call.from_user.id))
        mytime.mytime.get_medium(todaylist=mytime.mytime.todaylist, myid=str(call.from_user.id))
        set_future(myid=myid)
    elif call.data == "Low":

        clean_file(myid=str(call.from_user.id))
        mytime.mytime.get_low(todaylist=mytime.mytime.todaylist, myid=str(call.from_user.id))
        set_future(myid=myid)
    mytime.mytime.get_selected_action(selected_action=mytime.mytime.selected_action, myid=str(call.from_user.id))
    inlines = telebot.types.InlineKeyboardMarkup()
    if len(mytime.mytime.selected_action) < 1:
        happy_rsp.send_message(call.message.chat.id, "You have nothing to do today")
    else:
        happy_rsp.send_message(call.message.chat.id, "Your list to do for today")
        for element24 in mytime.mytime.selected_action:
            if element24 == "\n" or element24 =='':
                mytime.mytime.selected_action.remove(element24)
        happy_rsp.send_message(call.message.chat.id, '\n'.join(mytime.mytime.selected_action))
        inlines.add(telebot.types.InlineKeyboardButton(text='Press me', callback_data="Checking"))
        happy_rsp.send_message(call.message.chat.id, 'When ready to check', reply_markup=inlines)
#
@happy_rsp.callback_query_handler(func=lambda call: call.data in ["Checking"])
def step2(call):
    myid = str(call.from_user.id)
    mytime.mytime.selected_action.clear()
    mytime.mytime.get_selected_action(selected_action=mytime.mytime.selected_action, myid=myid)
    inlines = telebot.types.InlineKeyboardMarkup()
    for element17 in mytime.mytime.selected_action:
        if element17 == '' or element17 == "\n":
            mytime.mytime.selected_action.remove(element17)
    if len(mytime.mytime.selected_action) > 0:
        for element18 in mytime.mytime.selected_action:
            inlines.add(telebot.types.InlineKeyboardButton(text=element18, callback_data=element18))
        happy_rsp.send_message(call.message.chat.id, 'What have you done?', reply_markup=inlines)


@happy_rsp.callback_query_handler(func=lambda call: call.data in [*mytime.mytime.selected_action])
def step3(call):
    if len(mytime.mytime.selected_action) > 1:
        myid = str(call.from_user.id)
        for element18 in mytime.mytime.selected_action:
            if element18 == "\n" or element18 == '':
                mytime.mytime.selected_action.remove(element18)
            if call.data == element18:
                mytime.mytime.selected_action.remove(element18)
                clean_file(myid=myid)
                path2 = os.path.join("", myid + "now.txt")
                file2 = open(path2, "a")
                for x in mytime.mytime.selected_action:
                    file2.write(x)
                file2.close()
        inlines = telebot.types.InlineKeyboardMarkup()
        inlines.add(telebot.types.InlineKeyboardButton(text="What else?", callback_data="Checking"))
        inlines.add(telebot.types.InlineKeyboardButton(text="Enough", callback_data="Enough"))
        happy_rsp.send_message(call.message.chat.id, "Let's continue!", reply_markup=inlines)
    else:
        inlines1 = telebot.types.InlineKeyboardMarkup()
        inlines1.add(telebot.types.InlineKeyboardButton(text="I do", callback_data="Start_delayed"))
        inlines1.add(telebot.types.InlineKeyboardButton(text="I do not", callback_data="Delay again"))
        happy_rsp.send_message(call.message.chat.id, 'Want to do some delayed deals?', reply_markup=inlines1)

@happy_rsp.callback_query_handler(func=lambda call: call.data in ["Enough"])
def step4(call):
    myid = str(call.from_user.id)
    delayed.delayed.append_to_delayed(myid=myid, delayed_today_list=delayed.delayed.delayed_today_list)
    delayed.delayed.get_delayed_list(delayed_today_list=delayed.delayed.delayed_today_list, myid=str(call.from_user.id))
    happy_rsp.send_message(call.message.chat.id, "Thanks for collaboration! See you!")

@happy_rsp.callback_query_handler(func=lambda call: call.data in ["Start_delayed", "Delay again"])
def step5(call):
    if call.data == "Start_delayed":
        myid = str(call.from_user.id)
        path2 = os.path.join("", myid + "future.txt")
        file2 = open(path2, "r")
        delayed.delayed.list_notdone = file2.readlines()
        for element19 in delayed.delayed.list_notdone:
            if element19 == '' or element19 == '\n':
                delayed.delayed.list_notdone.remove(element19)
        if len(delayed.delayed.list_notdone) < 1:
            happy_rsp.send_message(call.message.chat.id, "Your place is super pure! Relax!")
        else:
            inlines = telebot.types.InlineKeyboardMarkup()
            for element in delayed.delayed.list_notdone:
                inlines.add(telebot.types.InlineKeyboardButton(text=element, callback_data=element))
            happy_rsp.send_message(call.message.chat.id, 'What do you want to do?', reply_markup=inlines)
        file2.close()
    elif call.data == "Delay again":
        delayed.delayed.get_delayed_list(delayed_today_list=delayed.delayed.delayed_today_list, myid=str(call.from_user.id))
        happy_rsp.send_message(call.message.chat.id, "Thanks for collaboration! See you!")


@happy_rsp.callback_query_handler(func=lambda call: call.data in [*delayed.delayed.list_notdone])
def step6(call):
    myid = str(call.from_user.id)
    path2 = os.path.join("", myid + "future.txt")
    file2 = open(path2, "r+")
    file2.truncate()
    file2.close()
    for element19 in delayed.delayed.list_notdone:
        if call.data == element19:
            delayed.delayed.list_notdone.remove(element19)
    delayed.delayed.list_notdone = list(set(delayed.delayed.list_notdone))
    for element20 in delayed.delayed.list_notdone:
        path2 = os.path.join("", myid + "future.txt")
        file2 = open(path2, "a")
        file2.write(element20)
        file2.close()
    if len(delayed.delayed.list_notdone) > 0:
        inlines1 = telebot.types.InlineKeyboardMarkup()
        inlines1.add(telebot.types.InlineKeyboardButton(text="I do", callback_data="Start_delayed"))
        inlines1.add(telebot.types.InlineKeyboardButton(text="I do not", callback_data="Delay again"))
        happy_rsp.send_message(call.message.chat.id, 'Want to do some delayed deals?', reply_markup=inlines1)
        delayed.delayed.list_notdone.clear()
    else:
        happy_rsp.send_message(call.message.chat.id, "Your place is super pure! Relax!")

def clean_file(myid):
    path2 = os.path.join("", myid + "now.txt")
    file2 = open(path2, "r+")
    file2.truncate()
    file2.close()
    return "OK"

def set_future(myid):
    list4 = list()
    path2 = os.path.join("", myid + "future.txt")
    file2 = open(path2, "r")
    list3 = file2.readlines()
    file2.close()
    path2 = os.path.join("", myid + "future.txt")
    file2 = open(path2, "r+")
    file2.truncate()
    file2.close()
    for element1 in list3:
        element2 = element1.split(" - ")
        element3 = element2[0] + " - " + element2[1]
        element4 = element3.rstrip("\n")
        list4.append(element4)
    list5 = list(set(list4))
    path2 = os.path.join("", myid + "future.txt")
    file2 = open(path2, "a")
    for element5 in list5:
        file2.write(element5 + "\n")
    file2.close()
    return "OK"



happy_rsp.polling(none_stop=True, interval=0)
