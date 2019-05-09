from TwitchWebsocket import TwitchWebsocket
import json, time, threading

class Settings:
    def __init__(self, bot):
        try:
            # Try to load the file using json.
            # And pass the data to the MyBot class instance if this succeeds.
            with open("settings.txt", "r") as f:
                settings = f.read()
                data = json.loads(settings)
                bot.set_settings(data['Host'],
                                data['Port'],
                                data['Channel'],
                                data['Nickname'],
                                data['Authentication'])
        except ValueError:
            raise ValueError("Error in settings file.")
        except FileNotFoundError:
            # If the file is missing, create a standardised settings.txt file
            # With all parameters required.
            with open('settings.txt', 'w') as f:
                standard_dict = {
                                    "Host": "irc.chat.twitch.tv",
                                    "Port": 6667,
                                    "Channel": "#<channel>",
                                    "Nickname": "<name>",
                                    "Authentication": "oauth:<auth>"
                                }
                f.write(json.dumps(standard_dict, indent=4, separators=(',', ': ')))
                raise ValueError("Please fix your settings.txt file that was just generated.")

class TwitchSendMessage:
    def __init__(self):
        self.host = None
        self.port = None
        self.chan = None
        self.nick = None
        self.auth = None
        self.sent = False
        
        # Fill previously initialised variables with data from the settings.txt file
        Settings(self)

        self.ws = TwitchWebsocket(host=self.host, 
                                  port=self.port,
                                  chan=self.chan,
                                  nick=self.nick,
                                  auth=self.auth,
                                  callback=self.message_handler,
                                  capability=["membership", "tags", "commands"],
                                  live=True)
        GetInput(self.ws)
        self.ws.start_bot()

    def set_settings(self, host, port, chan, nick, auth):
        self.host = host
        self.port = port
        self.chan = chan
        self.nick = nick
        self.auth = auth

    def message_handler(self, m):
        print(m)

class GetInput(threading.Thread):

    def __init__(self, ws):
        threading.Thread.__init__(self)
        self.name = "GetInput"

        self.ws = ws
        self.start()
    
    def run(self):
        while True:
            inp = input(">")
            self.ws.send_message(inp)
    
if __name__ == "__main__":
    TwitchSendMessage()
