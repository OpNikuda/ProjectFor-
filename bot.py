import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TELEGRAM_TOKEN = '7695079641:AAEPnIMhTbVcgFTsxvGLiD0nd_iiORT8dbE'

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Dictionary, containing all of the dialogues and corresponding ids
dialogue_map = {
    (0, 1): "You dont remember neither who you are, nor what is happening and will happen in your not-so distant future.",
    (0, 2): "Suddenly, you found yourself driving in an old, dark truck. There were a lot of men, silently sitting on planks that were loosely tied up to the exterior of a machine.",
    (0, 3): "After a short moment of time, car stopped its movement.",
    (0, 4): "You have arrived at your new home. You are a criminal.",
    (0, 5): "At your arrival to the quarantine department, rep of a prison camp very \"politely\" asks you to wash the floors.",

    (1, 1): "Laying on your bench, you are doing something in your smartphone",
    (1, 2): "However, your moment of silence and peace, gets disrupted by a passing guardian, who wants to take away your precious thing!",

    (2, 1): "You are summoned to the operative unit, and there, the husky voices offer to sign a document on cooperation in exchange for various goods.",
    (2, 2): "What is your move?",

    (3, 1): "The local public monitoring comission visited the colony.",
    (3, 2): "Its reps asked if there were any comlpaints.",
    (3, 3): "What is your reaction?",

    (4, 1): "You work at a sewing factory in a penal colony. Over time, you realize that the inmates are underpaid a substantial part of their wages. Your descision?",

    (5, 1): "Out of desperation, you decide to escape. What do you do?",

    (6, 1): "Yay! You won!",


    (-1, 1): "Game over."

}

# Branching instructions [call_data, text, health_change, rep_change, cons_id]
dialogue_map_branches = {
    (0, 5): [[1, "Yes sir! Washing floors is my speciality!", 0, -100, 1], [2, "No.", -20, 20, 2], [3, "Its time to fight!", -40, -40, 3]],
    (1, 2): [[4, "Punch him and try to quickly hide your phone.", -15, -5, 1], [5, "Give up.", -30, -30, 2], [6, "Maybe let's make a \"deal\"?", 0, 30, 3]],
    (2, 2): [[7, "Agree. They are for sure a bunch of a good people!", 30, 0, 1], [8, "Indignantly refuse", -20, 20, 2]],
    (3, 3): [[9, "Refuse from communication in an absolutely rude manner.", -10, 10, 1], [10, "Tell them that this place is like a heaven or even better", 30, -30, 2], [11, "Very enthusiastically describe this place as a hell on earth.", -80, 40, 3]],
    (4, 1): [[12, "Ignore it.", 0, 0, 1], [13, "Ask warden about this.", 50, 0, 2], [14, "Group up with your inmates and go on strike.", -40, 100, 3]],
    (5, 1): [[15, "Find a comrade like you and go into the woods with him.", 0, 0, 1], [16, "Bribe the warden to let you out.", 0, 0, 2], [17, "Go the legal way.", 0, 0, 3]]
}

# List of consequences
conss_map = {
    1 : "Your boss is happy. And your reputation is not.",
    2 : "Auch. Everybody are impressed with your steel nerves.",
    3 : "You have been beaten like a little bug. Git gud.",\
    4 : "Unfortunately, there is no place whwre you can hide your phone.",
    5 : "Unluckily, they have found phone numbers of your comrades in your phonebook, and took away their phones too. Your comrades were not really happy about that.",
    6 : "The money is sent to the guard's wallet - to their delight and your relief.",
    7 : "Somehow, you managed to keep it a secret from your fellow prisoners.",
    8 : "You are getting a little beat up in the squad room. As a mere formality.",
    9 : "Your unlawful acts of rudeness are interrupted by the use of physical force and with the full approval of the monitoring comission.",
    10 : "The warden of the colony gives you an incentive in the form of an extra grocery pass",
    11 : "Comission sent a report to the prosecutor, who appears to be the deputy's father-in-law. He decided to give you hell on earth.",
    12 : "You have succesfully ignored this problem.",
    13 : "Warden realizes that the best way out is to pay you for your loyalty with extra perks.",
    14 : "For destabilizing a correctional facility, you get a few years added to your sentence.",
    15 : "Somehow you both managed to do it. After your escape you both decided that out there is actually better, and you both had a long, happy life in the forest.",
    16 : "It seems like it's a pretty standard practice, and for a fee, you're swapped with a hobo.",
    17 : "Having paid the expenses of attorneys and responsible members of the administration, prosecutor's office and the education of the daughters of a federal judge, standing firmly on the path of correction, you go free with a clear consience"

}
# Current dialogue
position = 1

# Current branch
branch = 0

# Game stats
health = 0
reputation = 0

# Generate markup for inline keyboard. Checks possible branhces
def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("<", callback_data="kb_prev"),
                               InlineKeyboardButton(">", callback_data="kb_next"))
    try :
        for x in dialogue_map_branches[(branch, position)] :
            markup.add((InlineKeyboardButton(x[1], callback_data=x[4])))
    except :
        pass
    return markup

# Code, responsible for button logic
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):

    global position
    global branch
    global reputation
    global health

    if reputation <= -200 or health <= -100 :
        branch = -1
        position = 1

    if call.data == "kb_next":
        position += 1
        try :
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = f"Reputation: {reputation}\nHealth: {health}\n\n{dialogue_map[(branch, position)]}", reply_markup=gen_markup())
            return None
        except :
            position -= 1
            return None
        

    elif call.data == "kb_prev":
        position -= 1
        try :
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = f"Reputation: {reputation}\nHealth: {health}\n\n{dialogue_map[(branch, position)]}", reply_markup=gen_markup())
            return None
        except :
            position += 1
            return None

    elif call.data == "cons_next" :
        if reputation <= -200 or health <= -100 :
            branch = -1
            position = 1
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = f"Reputation: {reputation}\nHealth: {health}\n\n{dialogue_map[(branch, position)]}", reply_markup=gen_markup())
            return None
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = f"Reputation: {reputation}\nHealth: {health}\n\n{dialogue_map[(branch, position)]}", reply_markup=gen_markup())
    
    else :
        reputation += dialogue_map_branches[(branch, position)][int(call.data) - 1][3]
        health += dialogue_map_branches[(branch, position)][int(call.data) - 1][2]
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton(">", callback_data="cons_next"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = conss_map[dialogue_map_branches[(branch, position)][int(call.data) - 1][0]], reply_markup=markup)
        position = 1
        branch += 1
    


# Startup
@bot.message_handler(commands=["start"])
def message_handler(message):
    global branch
    global position
    global health
    global reputation

    branch = 0
    position = 1
    health = 0
    reputation = 0

    bot.send_message(message.chat.id, f"Reputation: {reputation}\nHealth: {health}\n\n{dialogue_map[(branch, position)]}", reply_markup=gen_markup())

bot.infinity_polling()
