from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnubtest import MySubscribeCallback
import sys
from questionnaire import Questionnaire

pn_config = PNConfiguration()
pn_config.publish_key = 'pub-c-c96b6401-1254-4fe2-9d2a-0c193f5818ad'
pn_config.subscribe_key = 'sub-c-24bd254c-df80-11e6-8652-02ee2ddab7fe'

pubnub = PubNub(pn_config)

name = raw_input("Enter your name: ")
pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels('awesome').with_presence().execute()
try:
    while 1:
        arg = raw_input()
        if arg:
            message = {"Name": name, "User": "client", "msgType": "string" ,"message": arg, "UUID": pubnub.uuid}
            pubnub.publish().channel('awesome').message(message).meta({"UUID": pubnub.uuid}).sync()
except KeyboardInterrupt:
    print("\nUnsubscribing and exiting")
    pubnub.unsubscribe().channels('awesome').execute()
    sys.exit(1)

