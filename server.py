# Done by - Priyanka Bangalore Jayadeva (1001512908)
from flask import Flask
from flask import request
import json
import requests
from Tkinter import *
import threading


INP_FILE = 'synonyms.json' # file containing the words and their synonyms
PORT_NUMBER = 5544
ARG_NAME = 'word'
HOST = '0.0.0.0'  # listen to every available network interface
NUM_SYNONYMS = 5 # number of synonyms to return
INVALID_MESSAGE = 'Word not found' # returned if an invalid word is entered

#Initializing GUI
master = Tk()
master.minsize(400, 400) # mentioning the window size
textVar = StringVar()
labelfont = ('sans-serif', 12, '') # setting the font style and size
lab = Label(master, textvariable=textVar)
lab.config(font=labelfont)
lab.pack()



# server related code

app = Flask(__name__)

responseHtml = '''
<!DOCTYPE HTML>
<html>
<head><title>{0}</title></head>
<body>
    <h1>{1}</h1>
    <ul>
    {2}
    </ul>
</body>
</html>
'''

# loading the synonyms file into memory
def loadSyn():
    '''
    Read from file and return a dictionary of word -> synonym
    '''
    with open(INP_FILE) as f:
        return json.loads(f.read())

synDict = loadSyn()

# displaying the synonyms
def getLiString(synonyms):
    s = ''
    for syn in synonyms:
        s += '<li>' + syn + '</li>'
    return s

def getHtmlResponse(key, synonyms):
    liStr = getLiString(synonyms)
    return responseHtml.format(key, key, liStr)

# shutting down the Flask server
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    func()

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'


# displaying the connection details on the server GUI
@app.route('/', methods=['GET'])
def service():
    textVar.set(textVar.get() + '\nRecieved a GET Request...')
    key = request.args.get(ARG_NAME) # obtaining the word to be searched for
    key = key.lower() # converting the entered word to lower case before looking up in the thesaurus
    synonyms = synDict.get(key) # returns synonyms if exists else None
    if synonyms is None:
        return INVALID_MESSAGE
    else:
        return getHtmlResponse(key, synonyms[:NUM_SYNONYMS]) # returning the synonym

# making the server multithreaded
class ServerThread(threading.Thread):

    def __init__(self, app):
        super(ServerThread, self).__init__()
        self.app = app

    def run(self):
        app.run(host=HOST, port= PORT_NUMBER, threaded=True)

# starting the server
if __name__ == '__main__':
    textVar.set('Initializing Server...')

    serverThread = ServerThread(app)
    serverThread.start()
    textVar.set(textVar.get() + '\nServer Running')
    master.mainloop()
    requests.post('http://localhost:' + str(PORT_NUMBER) + '/shutdown')
