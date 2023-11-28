import streamlit as st
import time
from annotated_text import annotated_text
from components.app_components import *


def main():
    page_config()
    remove_white_space()
    import_fontawesome()
    selected_language = select_language()
    display_author(selected_language)
    set_header(selected_language)
    uploaded_file = upload_file(selected_language)
    set_title(selected_language)

    data = load_data(uploaded_file)
    text_placeholder(data, selected_language)
    check = check_columns(data)
    if check:
        mode = select_mode(data, selected_language)

        # Affichage en fonction du mode sélectionné
        if mode == "📚 Apprentissage" or mode == "📚 Learning":
            display_data(data, selected_language)

        elif mode == "🎲 Texte aléatoire" or mode == "🎲 Random text":
            user_translation, submit, clear = random_text(data, selected_language)
            if submit:
                post_submit(selected_language, user_translation)
            if clear:
                # Réinitialise les mots aléatoires
                (
                    st.session_state.random_word,
                    st.session_state.correct_translation,
                ) = get_random_word(data, selected_language)
                st.rerun()

        elif mode == "🏋️‍♂️ Entraînement" or mode == "🏋️‍♂️ Training session":
            if "index" not in st.session_state:
                st.session_state.index = 0
            if st.session_state.index >= len(data):
                st.session_state.index = 0
            if "score" not in st.session_state:
                st.session_state.score = 0
            if st.session_state.index == 0:
                st.session_state.score = 0
            check_session_state_train(data, selected_language)
            train_text_subheader(selected_language)
            user_translation_train, submit_train, clear_train = userform_train(
                selected_language
            )
            if submit_train:
                post_submit_train(selected_language, user_translation_train)
            index_writer_train(data, selected_language)
            score_writer_train(selected_language)
            if clear_train:
                # va chercher un nouveau mot
                (
                    st.session_state.next_word,
                    st.session_state.correct_translation_train,
                ) = get_next_word(data, selected_language)
                st.rerun()
            if st.session_state.index == len(data) - 1:
                final_scorer(data)
    else:
        if data is not None:
            if selected_language == "FR":
                st.write(
                    "> Les colonnes **French** ou **English** n'ont pas été trouvées dans le dataset."
                )
            else:
                st.write(
                    "> Sadly, no column **French** or **English** has been found in the dataset."
                )


if __name__ == "__main__":
    main()
