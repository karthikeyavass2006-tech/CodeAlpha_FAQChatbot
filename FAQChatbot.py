from tkinter import*
from tkinter import ttk
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string

#nltk process
#nltk.download('punkt')
#nltk.download('stopwords')
#nltk.download('wordnet')
sw=set(stopwords.words('english'))
lemmatizer=WordNetLemmatizer()
vectorizer=TfidfVectorizer()

background_theme="#121212"
theme="#50AB00"
theme_light="#6FD000"
theme_superlight="#87FE00"
FONT=('Corbel',18)
FONT_BOLD=(FONT[0], FONT[1], 'bold')
FONT_BOLD_ITALIIC=(FONT[0], FONT[1], 'bold italic')

def preprocess(q): #Preprocess question before send
    tokens=nltk.word_tokenize(q.lower())
    ct=[lemmatizer.lemmatize(token) for token in tokens if token not in string.punctuation and token not in sw]
    return " ".join(ct)

faq = {
    "What is Artificial Intelligence": "Artificial Intelligence (AI) is the simulation of human intelligence by computers.",
    "How many types of ai": "There are two major types:\n1. Generative AI\n2. Traditional AI",
    "What is traditional AI": "Traditional AI is designed to perform specific tasks by following predefined rules, algorithms, or learned patterns.",
    "What is generative AI": "Generative AI is a type of AI that can create new content such as text, images, audio, video, or code based on patterns learned from large amounts of data.",
    "What is machine learning": "Machine Learning (ML) is a branch of AI that enables computers to learn from data and improve their performance without being explicitly programmed for every task.",
    "What is deep learning": "Deep Learning is a subset of Machine Learning that uses artificial neural networks with multiple layers to learn complex patterns from large amounts of data.",
    "What is Natural Language Processing": "Natural Language Processing (NLP) enables computers to understand, interpret, and generate human language.",
    "What is Computer Vision": "Computer Vision enables computers to recognize, analyze, and understand images and videos.",
    "What is Robotics": "Robotics is the field of designing, building, and programming robots to perform tasks automatically.",
    "What is Data Science": "Data Science combines statistics, programming, and machine learning to extract meaningful insights from data.",
    "What are the applications of AI": "AI is widely used in healthcare, education, finance, transportation, manufacturing, entertainment, and customer service.",
    "Who is the father of AI": "John McCarthy is widely known as the father of Artificial Intelligence."
}
questions = [preprocess(question) for question in faq.keys()]
answers = [answer for answer in faq.values()]
v=vectorizer.fit_transform(questions) #Fit transform

def resize(event): #Fill the chat window to full size
    c.itemconfig(cw, width=event.width)

def responses(question): #Give answers for the question
    pq = preprocess(question) #Preprocessed question
    qv=vectorizer.transform([pq]) #Transform preprocesed question to document-term matrix
    best_match = cosine_similarity(v, qv).flatten() #Computes similarity
    best_index =  best_match.argmax()
    best_score = best_match[best_index]
    if best_score < 0.30:
        return None
    best_answer = answers[best_index]
    
    return best_answer

def send(): #Send response
    msg=e.get().strip()
    if msg:
        l=Label(chat,text=msg,font=FONT_BOLD,wraplength=275,bg=theme_light,fg='black',justify=LEFT,anchor=E,padx=5,pady=3)
        l.pack(anchor=E,pady=5,padx=2)
        e.delete(0, END)
        response=responses(msg)
        if response:
            delay=300
            fo=FONT_BOLD
        else:
            response="Sorry, I don't understand what you said."
            delay=150
            fo=FONT_BOLD_ITALIIC
        w.after(delay, lambda: give_response(response, fo))
        c.configure(scrollregion=c.bbox("all"))
        scroll()

def scroll(): #Moves down if we chat further if the chat frame fills 
    chat.update_idletasks()
    c.yview_moveto(1.0)

def give_response(r, fo):#Gives response as output

    L=Label(chat,text=r,font=fo,wraplength=275,bg='black',fg='white',justify=LEFT,anchor=W,padx=5,pady=3)
    L.pack(anchor=W,pady=5,padx=2)

    c.configure(scrollregion=c.bbox("all"))
    scroll()

def round_button(frame, txt): #Creates round button
    b=Canvas(frame,width=55,height=55,bg=background_theme, highlightthickness=0)
    b.pack(side=RIGHT)

    B =b.create_oval(5,5,50,50,fill=theme)
    t=b.create_text(28, 28, text=txt, fill=background_theme, font=FONT)

    def normal(event):
        b.itemconfig(B, fill=theme)

    def hover(event):
        b.itemconfig(B, fill=theme_light)

    def trigger(event):
        b.itemconfig(B, fill=theme_superlight)
        send()
        b.after(100, lambda: b.itemconfig(B, fill=theme_light))

    b.bind('<Enter>', hover)
    b.bind('<Leave>', normal)
    b.bind('<Button-1>', trigger)

w=Tk()
w.config(background=background_theme)
w.title('FAQ Chatbot')
w.resizable(False, False)

st=ttk.Style()
st.theme_use('clam')
st.configure('Custom.Vertical.TScrollbar',troughcolor='black',background=background_theme,arrowcolor=theme,grip=0)
st.map('Custom.Vertical.TScrollbar',background=[('active','#404040')])

l=Label(w,text='🤖 FAQ Chatbot',font=FONT_BOLD_ITALIIC,fg='white',bg='black',anchor=W, padx=5, pady=2)
l.pack(pady=5,padx=2,fill=X)

f=Frame(w,width=500,height=600,background=background_theme)
f.pack(fill=BOTH,expand=True)
f.pack_propagate(False)

s=ttk.Scrollbar(f,style='Custom.Vertical.TScrollbar')
s.pack(side=RIGHT,fill=Y)

c=Canvas(f,bg=background_theme,highlightthickness=0,yscrollcommand=s.set)
c.pack(side=LEFT,fill=BOTH,expand=True)
s.config(command=c.yview)

chat=Frame(c, bg=background_theme)
cw = c.create_window((0, 0),window=chat, anchor=NW)
c.bind('<Configure>',resize) #Fill the whole frame size
chat.bind("<Configure>",lambda e: c.configure(scrollregion=c.bbox("all")))#Keep the scrollbar updated

f1=Frame(w,bg=background_theme)
f1.pack(fill=BOTH)

e=Entry(f1,width=35,font=FONT,bg=background_theme,fg='white',insertbackground='white',selectbackground=theme)
e.pack(side=LEFT,fill=X,padx=13)
e.bind('<Return>', lambda event: send())

round_button(f1, '➤')

w.mainloop()