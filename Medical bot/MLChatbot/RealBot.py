import nltk
import random
import string
import pyttsx3

f=open('medical.txt','r',errors = 'ignore')
raw=f.read()
raw=raw.lower()# converts to lowercase

sent_tokens = nltk.sent_tokenize(raw)# converts to list of sentences
word_tokens = nltk.word_tokenize(raw)# converts to list of words

lemmer = nltk.stem.WordNetLemmatizer()

def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up", "hey",)
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]


def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def response(user_response):
    robo_response=''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    jdx=vals.argsort()[0][-3]
    kdx=vals.argsort()[0][-4]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    st = sent_tokens

    if(req_tfidf==0):
        robo_response=robo_response+"I am sorry! I don't understand you"
        return robo_response
    else:
        robo_response = robo_response+st[idx]+'\n'+st[jdx]+'\n'+st[kdx]
        return robo_response



#print("ROBO: My name is Robo. I will answer your queries about disease and health problems. If you want to exit, type Bye!")
def chatresponse(m):
    user_response = m
    user_response=user_response.lower()
    if(user_response!='bye'):
        if(user_response=='thanks' or user_response=='thank you' ):
            x = "ROBO: You are welcome.."
            return x
        else:
            if(greeting(user_response)!=None):
                x = greeting(user_response)
                return x
            else:
                x = response(user_response)
                sent_tokens.remove(user_response)
                return x

    else:
        x = "ROBO: Bye! take care.."
        return x

l = ['bye','thanks','thank you']
def on_closing():
    top.destroy()

def send():
    msg = Entrybox.get("1.0","end-1c")
    Entrybox.delete("0.0",END)

    if msg in l:
        bye("Have a nice day! see ya")
        on_closing()
    if msg != '':
        Chatlog.config(state=NORMAL)
        Chatlog.delete("0.0",END)
        Chatlog.insert(END,"YOU SAID:"+ msg + '\n\n')
        Chatlog.config(foreground="#442265",font=("Verdana",12))

        res = chatresponse(msg)
        Chatlog.insert(END,"ROBO SAYS:"+ res + '\n\n')

        Chatlog.config(state=DISABLED)

# Implement voice reader
eng = pyttsx3.init('sapi5')
voices = eng.getProperty('voices')
eng.setProperty('voice',voices[0].id)

def bye(audio):
    eng.say(audio)
    eng.runAndWait()

def speak():
    re = Chatlog.get("1.0","end-1c")
    eng.say(re)
    eng.runAndWait()


from tkinter import *
top = Tk()
top.geometry('500x605')
top.resizable(height=FALSE,width=FALSE)
top.title("Chatbot")
top.configure(bg="#a3a3a3")
#top.protocol("WM_DELETE_WINDOW",on_closing)       #close button event

#Create Chat window
Chatlog = Text(top,bd=0,bg='white',width=50,height=8,font='Arial')
Chatlog.insert(END,"ROBO: My name is Robo. I will answer your queries about disease and health problems. If you want to exit, type Bye!")
Chatlog.config(state=DISABLED)

#Bind scrollbar to Chat window
scroll = Scrollbar(top,command=Chatlog.yview(),cursor='heart')
Chatlog['yscrollcommand']=scroll.set

#Create button to tell the bot
B = Button(top,text="Tell",width=10,height=2,bg='yellow',fg='black',command=send)
Lb = Button(top,text="Listen",width=10,height=2,bg='cyan',fg='black',command=speak)

#Create box to enter text
Entrybox = Text(top,bd=0,bg='white',width=29,height=5,font='Arial')
Entrybox.bind('<Return>',None)


#Place all components in screen
scroll.place(x=471,y=6,height=400)
Chatlog.place(x=20,y=6,height=400,width=450)
Entrybox.place(x=20,y=460,height=90,width=460)
B.place(x=410,y=555)
Lb.place(x=410,y=411)

top.mainloop()