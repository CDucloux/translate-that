import streamlit as st
import pandas as pd
import numpy as np


def main():
    st.title("Application de traduction français-anglais")

    words = {
        "French": ["Bonjour", "Chat", "Maison", "Livre", "Ordinateur"],
        "English": ["Hello", "Cat", "House", "Book", "Computer"],
    }
    df = pd.DataFrame(words)

    # Initialise les mots aléatoires dans la session_state
    if "french_word" not in st.session_state:
        (
            st.session_state.french_word,
            st.session_state.correct_translation,
        ) = get_random_word(df)

    st.write(
        f"Traduisez le mot suivant du français à l'anglais : **{st.session_state.french_word}**"
    )
    # st.write(st.session_state.french_word)
    # st.write(st.session_state.correct_translation)
    with st.form("myform", clear_on_submit=True):
        user_translation = st.text_input("Votre traduction en anglais :")
        col1, col2 = st.columns([1, 1])
        with col1:
            submit = st.form_submit_button(label="📤 Envoyer ma réponse")
        with col2:
            new_word = st.form_submit_button("🆕 Nouveau mot")

        if new_word:
            # Réinitialise les mots aléatoires
            (
                st.session_state.french_word,
                st.session_state.correct_translation,
            ) = get_random_word(df)

            st.experimental_rerun()

        if submit:
            if (
                user_translation.lower() == st.session_state.correct_translation.lower()
                and user_translation != ""
            ):
                st.success("Bonne traduction !")
            elif user_translation != "":
                st.error(
                    f"Mauvaise traduction. La traduction correcte était : **{st.session_state.correct_translation}**"
                )


def get_random_word(df):
    """Récupère un mot aléatoire grâce à un index aléatoire dans le dataframe."""
    random_index = np.random.randint(len(df))
    return df.iloc[random_index]["French"], df.iloc[random_index]["English"]


if __name__ == "__main__":
    main()
