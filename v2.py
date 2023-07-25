import psycopg2
from psycopg2 import Error
import speech_recognition as sr
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import pyttsx3
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

hostname = ""
username = ""
port_id = 
pwd = ""
database = ""

# Connect to the database
try:
    connection = psycopg2.connect(user=username,
                                  password=pwd,
                                  host=hostname,
                                  port=port_id,
                                  database=database)
    cursor = connection.cursor()
    print("Connected to PostgreSQL database")

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
    exit()

# Find a document by name
def searchItem(name: str):
    cursor.execute("SELECT id FROM product WHERE name=%s", (name,))
    record = cursor.fetchone()
    if record:
        engine = pyttsx3.init()
        engine.say(name+" can be found in isle " + str(record[0]))
        engine.runAndWait()
        print(name,"can be found in isle ",record[0])
        return record[0]
    else:
        # Check if the name ends in 's' and remove it if it does
        if name.endswith('s'):
            name = name[:-1]
        cursor.execute("SELECT id FROM product WHERE name=%s", (name,))
        record = cursor.fetchone()
        if record:
            engine = pyttsx3.init()
            engine.say(name+" can be found in isle " + str(record[0]))
            engine.runAndWait()
            print(name,"can be found in isle ",record[0])
            return record[0]
        else:
            engine = pyttsx3.init()
            engine.say("Sorry, item not found")
            engine.runAndWait()
            print("Sorry, item not found")
            return None


# Start the voice recognition loop
r =  sr.Recognizer()
while True: 
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=1)
            print("Say something")
            audio = r.listen(source)
            print("Recognizing")
            text = r.recognize_google(audio)
            text = text.lower()
            
            # Extract the noun from the text
            noun = None
            words = word_tokenize(text)
            tagged_words = pos_tag(words)
            for word, tag in tagged_words:
                if word == "i":
                    continue
                elif tag == 'NN' or tag == 'NNS':
                    noun = word
                    break
            print(noun)
            
            # Search for the item and exit if requested
            if noun == "quit":
                print("Exiting voice recognition loop")
                break
            searchItem(noun)
            
    except sr.UnknownValueError:
        r = sr.Recognizer()
        continue

# Close the database connection
cursor.close()
connection.close()
print("PostgreSQL connection is closed")
