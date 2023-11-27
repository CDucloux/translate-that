import streamlit as st
import pandas as pd
import numpy as np
import time
from annotated_text import annotated_text
from app_components import *


def progress_bar_timer():
    # Bouton pour démarrer le timer
    # Par défaut, configurer le timer pour avoir 20 secondes par mot.
    col1, col2 = st.columns([1, 1])
    success_container = st.empty()
    with col1:
        if st.button("Démarrer le timer"):
            # Barre de progression pendant 2 minutes
            with col2:
                progress_bar = st.progress(0)
                timer_text = st.empty()

                for i in range(121):  # 2 minutes = 120 secondes
                    # Mettre à jour la barre de progression et le timer toutes les secondes
                    progress_bar.progress(i / 120)
                    timer_text.text(f"Temps restant : {120 - i} secondes")
                    time.sleep(1)
                success_container.success("⏲ La session d'apprentissage est terminée.")


# with st.sidebar:
#    progress_bar_timer()

page_config()
remove_white_space()
selected_language = select_language()
nlp_fr = load_fr_model()
nlp_en = load_en_model()
set_header(selected_language)
uploaded_file = upload_file(selected_language)
set_title(selected_language)

data = load_data(uploaded_file)
text_placeholder(data, selected_language)
mode = select_mode(data, selected_language)

# Affichage en fonction du mode sélectionné
if mode == "📚 Apprentissage" or mode == "📚 Learning":
    display_data(data, selected_language)

elif mode == "🎲 Texte aléatoire" or mode == "🎲 Random text":
    user_translation, submit, clear = random_text(data, selected_language)
    if submit:
        post_submit(selected_language, user_translation, nlp_fr, nlp_en)
    if clear:
        # Réinitialise les mots aléatoires
        (
            st.session_state.random_word,
            st.session_state.correct_translation,
        ) = get_random_word(data, selected_language)
        st.rerun()

elif mode == "🏋️‍♂️ Entraînement" or mode == "🏋️‍♂️ Training session":
    ...
