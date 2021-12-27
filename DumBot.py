import telebot
from telebot import types
bot = telebot.TeleBot('paste_your_api_token_here')

name = '';
surname = '';
age = 0;
kek = False;

@bot.message_handler(content_types=['text'])
def start(message): #name

    if message.text == '/start':
        bot.send_message(message.from_user.id, "What's ur name?");
        bot.register_next_step_handler(message, get_name); 
    else:
        bot.send_message(message.from_user.id, 'Write /start');

def get_name(message): #name
    global name;
    name = message.text;
    bot.send_message(message.from_user.id, "What's ur surname?");
    bot.register_next_step_handler(message, get_surname);

def get_surname(message): #surname
    global surname;
    surname = message.text;
    bot.send_message(message.from_user.id, 'How old are u?');
    bot.register_next_step_handler(message, get_age);

def get_age(message): #age
    global age;
    while age == 0: 
        try:
             age = int(message.text) 
        except Exception:
             bot.send_message(message.from_user.id, 'Numbers, please!');
      
    keyboard = types.InlineKeyboardMarkup(); #keyboard
    key_yes = types.InlineKeyboardButton(text='Yes', callback_data='yes'); #yes button
    keyboard.add(key_yes); #let's add yes button
    key_no= types.InlineKeyboardButton(text='No', callback_data='no');
    keyboard.add(key_no); #let's add no button
    question = 'Are u dumb?';
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

def ask_again_one():
    keyboard = types.InlineKeyboardMarkup(); #keyboard
    key_no= types.InlineKeyboardButton(text='No', callback_data='no');
    keyboard.add(key_no); #let's add no button
    key_yes = types.InlineKeyboardButton(text='Yes', callback_data='yes'); #yes button
    keyboard.add(key_yes); #let's add yes button
    return keyboard


def ask_again_two():
    keyboard = types.InlineKeyboardMarkup(); #keyboard
    key_yes = types.InlineKeyboardButton(text='Yes', callback_data='yes'); #yes button
    keyboard.add(key_yes); #let's add yes button
    key_no= types.InlineKeyboardButton(text='No', callback_data='no');
    keyboard.add(key_no);
   
    return keyboard

def ask_confirm():
    keyboard = types.InlineKeyboardMarkup(); #keyboard
    key_yes = types.InlineKeyboardButton(text='Yes', callback_data='confirm'); #yes button
    keyboard.add(key_yes); #let's add yes button
    
    return keyboard
   

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global kek;
    if call.data == "confirm": 

        bot.send_message(call.message.chat.id, "Ok, I'll remember it :)");
    elif call.data == "yes": 
         bot.edit_message_text(chat_id=call.message.chat.id,
                              text="So, u are " +name+ " " +surname+ ", " +str(age)+ " y.o. and u are dumb?",
                              message_id=call.message.message_id,
                              reply_markup=ask_confirm(),
                              parse_mode='HTML')
    elif call.data == "no":

        #need to switch buttons
        if kek == True:
            reply = ask_again_two();
        else:
            reply = ask_again_one();

        kek = not kek
        bot.edit_message_text(chat_id=call.message.chat.id,
                              text="Ok, I'll ask u again. Are u dumb?",
                              message_id=call.message.message_id,
                              reply_markup=reply,
                              parse_mode='HTML')

bot.polling(none_stop=True, interval=0)    
