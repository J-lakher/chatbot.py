import nltk


from nltk.tag import pos_tag
from nltk.chunk import ne_chunk
from training import lemmatize
import string

import pickle
import numpy as np

from keras.models import load_model
model = load_model('chatbot_model.h5')



import json
import random
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))



def clean_up_sentence(sentence):
   
    sentence_words = sentence.split()
    
    # Remove punctuation
    sentence_words = [word for word in sentence_words if word not in string.punctuation]
    sentence_words = [lemmatize(word.lower()) for word in sentence_words]
    
    return sentence_words


def bow(sentence, words, show_details=True):
    
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
              bag[i] = 1
               
    return(np.array(bag))

def predict_class(sentence, model):
    
    p = bow(sentence, words)
    res = model.predict(np.array([p]))[0]
  
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
   
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list




def named_entity_recognition(sentence):
    words = sentence.split()
    tagged_words = pos_tag(words)
    named_entities = ne_chunk(tagged_words)
    return named_entities

def extract_named_entities(chunked_words):
    named_entities = []
    for entity in chunked_words:
        if isinstance(entity, nltk.tree.Tree):
            named_entities.append(' '.join([word for word, _ in entity.leaves()]))
    return ', '.join(named_entities)
    
def getResponse(ints, intents_json,msg):
    if not ints:
       return random.choice(intents_json['fallback_responses'])
    
    if 'intent' in ints[0]:
        tag = ints[0]['intent']
        list_of_intents = intents_json['intents']
        for i in list_of_intents:
            if i['tag'] == tag:
                result = random.choice(i['responses'])
                named_entities = named_entity_recognition(msg)
                named_entities_str = extract_named_entities(named_entities)
                result = result.replace('{named_entity}', named_entities_str)
                
                return result

  
    return "Sorry! I don't have a response for that at the moment."






def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents,msg)
    return res

