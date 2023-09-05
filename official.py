from telegram.ext import Updater
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from datetime import datetime
import mysql.connector

updater = Updater('5440879489:AAFZaFxAOGj0rKNUlDycS2JSPlPYLPEe_HE')

def start(update: Update, context: CallbackContext):    
    update.message.reply_text('Welcome to Mybot!')

def help(update: Update, context: CallbackContext):
	update.message.reply_text('''These are the commands available in Mybot :-
	/start - Shows a welcome msg 
	/help - Shows the available commands
	/time - Shows the current time
    Hi/hi/Hello/hello - Provides your attendance''')

def time(update: Update, context: CallbackContext):
    now = datetime.now()
    date_time = now.strftime('%d/%m/%y, %H:%M:%S')
    update.message.reply_text(str(date_time))

def receive_contact(update: Update, context: CallbackContext):
    from_number = update['message']['contact']['phone_number']
    from_number = from_number[2:]
    print(from_number)
    db=mysql.connector.connect(database='sql12644516', host='sql12.freemysqlhosting.net', user='sql12644516', password='45r3aJP6g4')
    db1=db.cursor(buffered=True)
    db1.execute('SELECT * FROM `TABLE 1` WHERE `Student Ph no.`=%s',(from_number,))
    st_det=db1.fetchone()

    if st_det is not None:
        update.message.reply_text("Hello "+list(st_det)[0]+"!\nYour attendance is "+ list(st_det)[2])
    else:
        update.message.reply_text("""Can't fetch your attendance with this number!
        Try with another number""")

def send_contact(update: Update, context: CallbackContext):
    user_message = str(update.message.text).lower()

    if user_message in ("hello", "hi"):
        update.message.reply_text("To get your attendance or a student's attendance, provide the student's 10-digit contact number.", reply_markup={
            "keyboard": [[{"text": "Send contact", "request_contact": True}], ["Cancel"]],
            "resize_keyboard": True,
            "one_time_keyboard": True
        })
    elif user_message.isdigit() and len(user_message) == 10:
        student_number = user_message  

        db = mysql.connector.connect(database='sql12644516', host='sql12.freemysqlhosting.net', user='sql12644516', password='45r3aJP6g4')
        db_cursor = db.cursor(buffered=True)
        db_cursor.execute('SELECT * FROM `TABLE 1` WHERE `Student Ph no.` = %s', (student_number,))
        student_data = db_cursor.fetchone()

        if student_data is not None:
            update.message.reply_text(f"Student Name: {student_data[0]}\nAttendance: {student_data[2]}")
        else:
            update.message.reply_text("Student not found in the database.")
    else:
        update.message.reply_text("Please provide a valid 10-digit student number or send 'Hi' or 'Hello' to get instructions.")

def echo(update: Update, context: CallbackContext):
    update.message.reply_text(update.message.text)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('time', time))
updater.dispatcher.add_handler(CommandHandler('echo', echo))
updater.dispatcher.add_handler(MessageHandler(Filters.contact, receive_contact)) 
updater.dispatcher.add_handler(MessageHandler(Filters.text | Filters.contact, send_contact))



if __name__=="__main__":
    updater.start_polling()
