import streamlit as st
import pickle
import pandas as pd
import re
import nltk
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem import PorterStemmer

nltk.download('punkt')
nltk.download('stopwords')

#store saved models into variables - Best model cleaned BOW and MNB
model = pickle.load(open('references/models/cleaned_BoW-MNB.pkl','rb'))
vectorizer = pickle.load(open('references/vectorizers/BoW_vectorizer-MNB.pkl','rb'))

#app variables
inputTextLimit = 75

#helper functions
def clean_tweets_with_stem(tweet): # clean up text
    tweet = tweet.lower()
    tweet = re.sub(r'[^\w\s]', '', tweet)
    words = word_tokenize(tweet)
    tweet = " ".join([word for word in words if word not in stopwords.words('english') ])
    words = word_tokenize(tweet)
    porter = PorterStemmer()
    tweet = " ".join([ porter.stem(word) for word in words])
    return tweet

def clean_tweets_without_nlp(tweet):
    tweet = tweet.lower()
    tweet = re.sub(r'[^\w\s]', '', tweet)
    words = word_tokenize(tweet)
    tweet = " ".join([ word for word in words])
    return tweet

def findEmotion(text): # Find emotion behind text
    emotions = ['sadness','joy','love','anger','fear','surprise']
    text = clean_tweets_without_nlp(text)
    text = vectorizer.transform([text])
    idx = model.predict(text)[0]
    return emotions[idx]

def getEmotionProb(text):
    emotions = ['sadness','joy','love','anger','fear','surprise']
    text = clean_tweets_without_nlp(text)
    text = vectorizer.transform([text])
    d = {
        "emotion": emotions,
        "probability": model.predict_proba(text)[0]
    }
    df = pd.DataFrame(d)
    df = df.set_index('emotion')
    return df


#app below

st.set_page_config( # head tag
    page_title="Emotion Prediction Model Demo", 
    page_icon="📝",
    layout="centered",
    menu_items={
        'Get Help': 'https://github.com/112523chen/CTP-Fall-2022-Project',
        'Report a bug': "https://github.com/112523chen/CTP-Fall-2022-Project/issues/new",
        'About': """
                ***Streamlit app*** that predicts the emotion behind text
                """ 
    })


agree = st.sidebar.checkbox('See Probability Estimates')

c1, c2, c3 = st.columns([1, 6, 1]) # establish margin
with c2:
    st.title('Emotion Analysis Model') #header tag
    text = st.text_input('Text Sample', '') # message, default
    if text is not '': #check if text var is an actually input 
        prediction = findEmotion(text) # finds the emotion behind the user input
        prediction_df = getEmotionProb(text)
        if len(text) > inputTextLimit:
            st.header(f"The text has the {prediction} emotion behind it") #presents prediction
            st.write(text)
        else:
            st.header(f"The text above has the {prediction} emotion behind it") #presents prediction
        if agree:
            st.subheader("Emotion Probabilities")
            st.table(prediction_df)
    else:
        st.info(
                f"""
                    ⬆️ Enter text first.
                    """
            )
        st.stop()