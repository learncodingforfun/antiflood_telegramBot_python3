import telepot
from threading import Thread, Timer
import time
from antiflood_config import token, settings

data = []


def delMsg(chat_id, msg_id):
    return bot.deleteMessage((chat_id, msg_id))


def antiflood(user_id, chat_id):
    counter = 0
    msg_ids = []
    for idx, item in enumerate(data):
        combined = chat_id + ":" + user_id
        if combined in item:
            msg_id = data[idx].split(":")[2]
            # appends the message id to the msg_ids list
            msg_ids.append(msg_id)
            # increases counter by 1
            counter += 1
    if counter >= settings['antiflood_max_msgs']:
        data.clear()
        bot.kickChatMember(chat_id, user_id)
        print("[!] " + str(user_id) + " banned from " + str(chat_id))
        for msg in msg_ids:
            # starts a thread for each message id to be deleted
            Thread(target=delMsg, args=(chat_id, int(msg),), ).start()
    elif counter < settings['antiflood_max_msgs']:
        data.clear()


def on_message(msg):
    # main function to be used
    if msg['chat']['type'] == "supergroup" and "new_chat_member" not in msg and "left_chat_participant" not in msg:
        string_to_append = str(msg['chat']['id']) + ":" + str(msg['from']['id']) + ":" + str(msg['message_id'])
        data.append(string_to_append)
        Timer(settings['antiflood_seconds'], antiflood, [str(msg['from']['id']), str(msg['chat']['id'])]).start()


def main(msg):
    # starts thread for main function
    t = Thread(target=on_message, args=(msg,), )
    t.start()


if __name__ == '__main__':
    # defines telepot client
    bot = telepot.Bot(token)
    # loops the threaded main function
    bot.message_loop(main)

    while 1:
        # used for receiving updates repeatedly
        time.sleep(10)


