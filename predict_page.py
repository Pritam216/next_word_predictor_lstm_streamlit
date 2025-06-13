import streamlit as st
import numpy as np
import pickle
from tensorflow.keras.utils import pad_sequences 
import time

def load_model():
    with open ('saved_model.pkl','rb') as file:
        data=pickle.load(file)
    return data

model = load_model()

def load_tokenizer():
    with open ('tokenizer.pkl','rb') as file:
        data=pickle.load(file)
    return data

tokenizer = load_tokenizer()

# Next Word Prediction Function

def predict_next_words(seed_text, num_words_to_generate, model, tokenizer, max_sequence_len):
    generated_text = seed_text
    print(f"\nSeed Text: {seed_text}")
    print("Generating...")

    for _ in range(num_words_to_generate):
        # Tokenize the current generated_text
        token_list = tokenizer.texts_to_sequences([generated_text])[0]

        # Pad the tokenized sequence
        padded_token_list = pad_sequences([token_list], maxlen=max_sequence_len - 1, padding='pre')

        # Predict the probabilities for the next word
        predicted_probabilities = model.predict(padded_token_list, verbose=0)[0]

        # Get the index of the word with the highest probability
        predicted_word_index = np.argmax(predicted_probabilities)

        # Find the word corresponding to the index
        output_word = ""
        for word, index in tokenizer.word_index.items():
            if index == predicted_word_index:
                output_word = word
                break

        if output_word == "":
            break

        generated_text += " " + output_word
        # print(generated_text)
        time.sleep(0.1)

    return generated_text

def predict_page_function():
    # Streamlit UI
    st.title("Next Word Predictor")
    st.markdown("### **Enter Seed Text**")
    seed_text = st.text_input("", " ")

    # Number of Words Slider
    st.markdown("### **How many words to generate?**")
    num_words = st.slider("", 1, 20, 5)

    max_sequence_len = model.input_shape[1] + 1

    if st.button("Predict"):
        result = predict_next_words(seed_text, num_words, model, tokenizer, max_sequence_len)
        st.markdown("### **Generated Text:**")
        st.markdown(f"<div style='font-size: 20px; font-weight: bold;'>{result}</div>", unsafe_allow_html=True)

