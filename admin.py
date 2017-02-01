from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from questionnaire import Questionnaire
from pubnubtest import AdminSubscribeCallback
import sys
import re

class Admin(object):
    def __init__(self, pub_key, sub_key, name, channel):
        self.pub_key = pub_key
        self.sub_key = sub_key
        self.name = name
        self.channel = channel
        pnconfig = PNConfiguration()
        pnconfig.publish_key = self.pub_key
        pnconfig.subscribe_key = self.sub_key
        self.pubnub = PubNub(pnconfig)
        self.metadata = {"Name": self.name, "User": "admin", "UUID": self.pubnub.uuid}
        self.pubnub.add_listener(AdminSubscribeCallback())
        self.pubnub.subscribe().channels(channel).with_presence().execute()
        self.questions = []
        self.titles = []
    
    def publish_callback(self, result, status):
        print(result)
        print(status)

    def pub(self, msg, msgType):
        message = {"Name": self.name, "User": "admin", "msgType": msgType ,"message": msg, "UUID": self.pubnub.uuid}
        self.pubnub.publish().channel(self.channel).message(message).meta(self.metadata).sync()
    
    def unsub(self):
        self.pubnub.unsubscribe().channels(self.channel).execute()
    
    def commands(self, input):
        inputList = re.sub("[^\w]", " ",  input).split()

        title = None
        if len(inputList) > 1:
            title = ""
            for word in inputList[1:]:
                    title += word + " "
            title = title.strip()

        if inputList[0] == "help":
            pass
        elif input == "end question":
            self.end_question()
        elif input == "create question":
            self.create_question()
        elif input == "list question":
            self.list_question()
        elif inputList[0] == "view":
            if title:
                self.view_question(title)
        elif inputList[0] == "send":
            if title:
                self.send_question(title)
        elif input == "results":
            self.ask_for_results()
        else:
            print("Invalid command")
    
    def end_question(self):
        msgType = "end_question"
        message = "end_question"
        self.pub(message, msgType)
    
    def add_question(self, question):
        self.questions += [question]
        title = question.get_title()
        self.titles += [title]
    
    def delete_question(self, question):
        self.questions.remove(question)
        self.titles.remove(question.get_title())
    
    def create_question(self):
        title = raw_input("Set title: ")
        if title == None:
            print("No question made")
            return None
        elif title in self.titles:
            print("A question with the same title already exists")
            return None
        question_string = raw_input("Type question: ")
        question = Questionnaire(title, question_string)
        add_answer_bool = True
        while add_answer_bool:
            print("Type an answer or type quit")
            answer = raw_input("Answer: ")
            if answer == "quit" or answer == "q":
                if question.count_answers():
                    self.add_question(question)
                    print("Question " + title + " successfully created")
                else:
                    print("Error: Question " + title + " has no answers and was deleted")
                add_answer_bool = False
            elif answer:
                points = raw_input("Points: ")
                try:
                    p = int(points)
                    question.add_answer(answer, p)
                except:
                    print("Error: Point value must be numeric")
    
    def list_question(self):
        if len(self.titles):
            self.titles.sort()
            for title in self.titles:
                print(title)
        else:
            print("No questions exist")
    
    def get_question(self, title):
        for question in self.questions:
            if question.get_title() == title:
                return question
        print("Error: Cannot find question \"" + title + "\"")
        return None
    
    def view_question(self, title):
        question = self.get_question(title)
        if question:
            print(question.get_title())
            print(question.get_question())
            answers = question.get_answers()
            answerkey = answers.keys()
            answerkey.sort()
            for key in answerkey:
                print(key + ": " + answers[key][0] + ", Points: " + str(answers[key][1]))
    
    def send_question(self, title):
        question = self.get_question(title)
        if question:
            self.pub(question.serialize(), "question")

    def ask_for_results(self):
        self.pub("results", "results")
    
    

        



publish_key = 'pub-c-c96b6401-1254-4fe2-9d2a-0c193f5818ad'
subscribe_key = 'sub-c-24bd254c-df80-11e6-8652-02ee2ddab7fe'
name = "alex"
admin = Admin(publish_key, subscribe_key, name, "awesome")
q1 = Questionnaire("Q1", "What is 1+1?")
q1.add_answer("2", 1)
q1.add_answer("1", 0)
q1.add_answer("3", 0)
q1.add_answer("4", 0)
admin.add_question(q1)
# admin.pub(q1.serialize(), "question")
print("Type help for commands. Press CTRL+C to exit.")
while True:
    try:
        input = raw_input()
        if input:
            admin.commands(input)
    except KeyboardInterrupt:
        print("Exiting")
        admin.end_question()
        admin.unsub()
        sys.exit(1)