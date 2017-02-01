from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory

class MySubscribeCallback(SubscribeCallback):
    def __init__(self):
        self.question_mode = False
        self.question = None
        self.answers = None
        self.has_answered = False

    def presence(self, pubnub, presence):
        # print(presence)
        # print(presence.uuid == pubnub.uuid)
        pass

    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            pass
            # This event happens when radio / connectivity is lost

        elif status.category == PNStatusCategory.PNConnectedCategory:
        # Connect event. You can do stuff like publish, and know you'll get it.
        # Or just use the connected event to confirm you are subscribed for
        # UI / internal notifications, etc
            pass
        elif status.category == PNStatusCategory.PNReconnectedCategory:
            pass
        # Happens as part of our regular operation. This event happens when
        # radio / connectivity is lost, then regained.
        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            pass
        # Handle message decryption error. Probably client configured to
        # encrypt messages and on live data feed it received plain text.

    def message(self, pubnub, message):
        if message.message['msgType'] == 'question':
            if self.question_mode == False:
                print(message.message['message']['Title'])
                print(message.message['message']['Question'])
                self.answers = message.message['message']['Answers']
                answerkey = self.answers.keys()
                answerkey.sort()
                for key in answerkey:
                    print(key + ": " + self.answers[key][0])
                self.question_mode = True
                self.question = message.message
            else:
                pass
        elif message.message['msgType'] == 'end_question':
            if self.question_mode:
                print(self.question['message']['Title'] + " has ended")
                self.question_mode = False
                self.question = None
                self.answers = None
                self.has_answered = False

        elif (pubnub.uuid == message.message["UUID"]):
            if self.question_mode == False:
                print("No question has been set yet")
            elif self.has_answered == False:
                your_answer = message.message['message']
                if your_answer in self.answers.keys():
                    print("Your answer is: " + your_answer)
                    print("You earned " + str(self.answers[your_answer][1]) + " point(s)")
                    self.has_answered = True
                else:
                    print("Invalid answer")
            else:
                print("You have already answered for this round")
        else:
            pass


class AdminSubscribeCallback(SubscribeCallback):
    def __init__(self):
        self.users = {}
        self.question_mode = False
        self.question = None
        self.answers = None
        self.has_answered = False
        self.results = {}
        self.uuid_ans_map = {}

    def presence(self, pubnub, presence):
        print(presence)
        if presence.event == "join":
            if self.question_mode:
                pubnub.publish().channel(presence.channel).message(self.question).sync()
            if presence.uuid not in self.users.keys():
                self.users[presence.uuid] = {"points": 0}
                print("UUID " + presence.uuid + " has joined")
        if presence.event == "leave":
            if presence.uuid in self.users.keys():
                del self.users[presence.uuid]
                print("UUID " + presence.uuid + " has left")

    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            pass
            # This event happens when radio / connectivity is lost

        elif status.category == PNStatusCategory.PNConnectedCategory:
        # Connect event. You can do stuff like publish, and know you'll get it.
        # Or just use the connected event to confirm you are subscribed for
        # UI / internal notifications, etc
            pass
        elif status.category == PNStatusCategory.PNReconnectedCategory:
            pass
        # Happens as part of our regular operation. This event happens when
        # radio / connectivity is lost, then regained.
        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            pass
        # Handle message decryption error. Probably client configured to
        # encrypt messages and on live data feed it received plain text.

    def message(self, pubnub, message):
        if message.message["UUID"] == pubnub.uuid:
            if message.message['msgType'] == 'question':
                if self.question_mode == False:
                    print(message.message['message']['Title'])
                    print(message.message['message']['Question'])
                    self.answers = message.message['message']['Answers']
                    answerkey = self.answers.keys()
                    answerkey.sort()
                    for key in answerkey:
                        print(key + ": " + self.answers[key][0])
                        self.results[key] = 0
                    self.question_mode = True
                    self.question = message.message                
                else:
                    print("Question mode still active. To end question mode, type \"end question\"")
            elif message.message['msgType'] == 'end_question':
                if self.question_mode:
                    print(self.question['message']['Title'] + " has ended")
                    self.question_mode = False
                    self.question = None
                    self.answers = None
                    self.has_answered = False
                    print(self.results)
                    self.results = {}
                    self.uuid_ans_map = {}
            elif message.message['msgType'] == 'results':
                if len(self.results):
                    print(self.results)
                    print(self.uuid_ans_map)
                else:
                    print("Question mode inactive. No results yet")
            
            else:
                print("Question mode still active. To end question mode, type \"end question\"")
        else:
            if message.message["User"] == "client":
                answer = message.message["message"]
                uuid = message.message["UUID"]
                if uuid not in self.uuid_ans_map.keys():
                    if answer in self.results.keys():
                        self.results[answer] += 1
                        self.uuid_ans_map[uuid] = answer
                else:
                    #client has already answered
                    pass

            pass
        

       
