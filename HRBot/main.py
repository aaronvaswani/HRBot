from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from flask import Flask, render_template, request, redirect, url_for, flash
import logging
import time

app = Flask(__name__)

bot = ChatBot(
            'Bob',
            # remove the below line to start the chatbot learning
            # read_only=True,
            storage_adapter='chatterbot.storage.SQLStorageAdapter',
            # remove the below line when you want 
            # database_uri=None,
            #input_adapter='chatterbot.input.TerminalAdapter',
            #output_adapter='chatterbot.output.TerminalAdapter',
            logic_adapters=[
            {
                'import_path': 'chatterbot.logic.BestMatch',
                'default_response': 'I apologize, I do not understand. Can you rephrase?',
                'maximum_similarity_threshold': 0.9
            }
    ]
)

#bot.set_trainer(ChatterBotCorpusTrainer)
trainer = ChatterBotCorpusTrainer(bot)
# trainer.train("chatterbot.corpus.english")
# trainer.train("./trivial.yml")
trainer.train("./Corpus/greetings.yml")
trainer.train("./Corpus/general.yml")
trainer.train("./Corpus/counterresponse.yml")

@app.route("/")
def home():
    return render_template("start.html")

@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        enteredname = request.form['username']
        enteredfunction = request.form['jobFunction']

        flash(enteredname)
        flash(enteredfunction)

        if enteredname != "":
            return redirect(url_for('chatbot'))

@app.route("/", methods=['GET'])
def chatbot():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(bot.get_response(userText))

if __name__ == "__main__":
    app.run()

def loadReward():
    trainer.train("./Reward/rewardBalance.yml")
    trainer.train("./Reward/rewardGeneral.yml")
    trainer.train("./Reward/rewardHealth.yml")
    trainer.train("./Reward/rewardInsurance.yml")
    trainer.train("./Reward/rewardPension.yml")

#user = input('what is your name...? ')
#time.sleep(1)
#print('Nice to meet you ' + user + "!")
#time.sleep(1.5)
#function = input('and which job function do you work in? \nReward, Recruitment or EHS\n')

#if the users name is X then it loads specific training data
#if (function == "Reward"):
#   loadReward()

while True:
    try:
        user_input = input(': ')

        #Breaks out of while loop and quits the chat bot
        if (user_input == "break" or user_input == "bye"):
            print("bye!")
            break

        bot_response = bot.get_response(user_input)

        print(bot_response)

    except(KeyboardInterrupt, EOFError, SystemExit):
        break