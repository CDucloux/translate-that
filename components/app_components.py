import streamlit as st
import pandas as pd
import numpy as np
from streamlit.delta_generator import DeltaGenerator
from annotated_text import annotated_text
import spacy
from spacy.language import Language


def page_config() -> None:
    """Configure la page avec un favicon et un titre."""
    return st.set_page_config(
        page_title="Streamlit Translate",
        page_icon="🗺",
        layout="wide",
    )


def remove_white_space():
    """Utilise du CSS pour retirer de l'espace non-utilisé."""
    return st.markdown(
        """
        <style>
                .block-container {
                    padding-top: 2rem;
                    padding-bottom: 0rem;
                    padding-left: 3rem;
                    padding-right: 3rem;
                }
                .st-emotion-cache-16txtl3{
                    padding-top: 2rem;
                    padding-right: 0rem;
                    padding-bottom: 1rem;
                    padding-left: 0rem;
                }
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_resource
def load_en_model() -> Language:
    """Load en nlp."""
    return spacy.load("en_core_web_sm")


@st.cache_resource
def load_fr_model() -> Language:
    """Load fr nlp."""
    return spacy.load("fr_core_news_sm")


def select_language():
    """Permet de sélectionner la langue de l'appli et de changer le fonctionnement des widgets."""
    lang = st.sidebar.toggle("Langue / Language")

    if lang:
        st.sidebar.write("*Selected language* : :flag-gb:")
        selected_language = "GB"
    else:
        st.sidebar.write("*Langage sélectionné* : :flag-fr:")
        selected_language = "FR"
    return selected_language


def set_header(selected_language: str):
    """Configure le header de la sidebar."""
    if selected_language == "FR":
        header = "*Paramétrage et import*"
    else:
        header = "*Parameters and import*"
    return st.sidebar.header(header)


def upload_file(selected_language: str):
    """Permet d'uploader son fichier au format excel ou csv."""
    if selected_language == "FR":
        import_header = "Charger un fichier CSV ou Excel"
        import_help = "Intrigué(e) ? Il suffit juste de charger un fichier .xlsx ou .csv avec 2 colonnes : French & English"
    else:
        import_header = "Upload a CSV or Excel file"
        import_help = "Intrigued? You just need to upload a .xlsx or .csv with 2 columns : French & English"
    return st.sidebar.file_uploader(
        label=import_header,
        type=["csv", "xlsx", "xls"],
        help=import_help,
    )


def set_title(selected_language: str) -> DeltaGenerator:
    """Permet d'afficher le titre de l'application en français et en anglais."""
    if selected_language == "FR":
        title = ":blue[Translate] :red[*That*] $\Rightarrow$ :flag-fr: to :flag-gb:"
    else:
        title = ":blue[Translate] :red[*That*] $\Rightarrow$ :flag-gb: to :flag-fr:"
    return st.title(title)


def load_data(file) -> pd.DataFrame | None:
    """Permet de charger les données qui ont été uploadées."""
    if file is not None:
        if file.name.endswith(".csv"):
            data = pd.read_csv(file)
        elif file.name.endswith(".xlsx") or file.name.endswith(".xls"):
            data = pd.read_excel(file)
        else:
            st.error(
                "Format de fichier non pris en charge. Veuillez utiliser un fichier CSV ou Excel."
            )
            return None
        return data
    return None


def text_placeholder(data: pd.DataFrame, selected_language: str):
    """Affiche des instructions quand aucun fichier n'est importé."""
    if data is None:
        if selected_language == "FR":
            text = "👋 Salut ! Tu es prêt pour faire un peu de traduction ?"
            info = "ℹ️ Avant de commencer, il faut importer un fichier de travail qui doit comporter une colonne **French** et **English**."
            expander_label = "*Exemple* de fichier :green[Excel]"
        else:
            text = "👋 Hey ! Ready for some translation work?"
            info = "ℹ️ To begin with, you need to import a file containing *at the very least* a **French** and **English** column."
            expander_label = ":green[Excel] file *example*"
        return (
            st.write(text),
            st.info(info),
            st.divider(),
            st.expander(expander_label).image("img/example.PNG"),
        )
    else:
        return None


def select_mode(data: pd.DataFrame, selected_language: str):
    """Permet de choisir entre 3 modes : apprentissage, texte aléatoire, et session d'entrainement."""
    if data is None:
        return None
    else:
        if selected_language == "FR":
            label = "Sélectionner le mode"
            options = ("📚 Apprentissage", "🎲 Texte aléatoire", "🏋️‍♂️ Entraînement")
        else:
            label = "Select a mode"
            options = ("📚 Learning", "🎲 Random text", "🏋️‍♂️ Training session")
        return st.sidebar.selectbox(label, options)


def display_data(data: pd.DataFrame, selected_language: str):
    """Permet d'afficher les données sous forme de table."""
    if data is not None:
        if selected_language == "FR":
            subheader = "📚 Mode Apprentissage"
            caption = "Apprendre vite, apprendre efficacement, et surtout : **ludiquement** ! Un mot ? Une expression ? Une phrase ? Sa traduction."
            text = f"- Nombre total d'expressions à apprendre : *{len(data)}*"
            column_order = ["French", "English"]
        else:
            subheader = "📚 Learning Mode"
            caption = "Learn faster, more effectively, and **joyfully**! A word? An expression? A sentence? Its translation."
            text = f"- Total number of expressions : *{len(data)}*"
            column_order = ["English", "French"]
        return (
            st.subheader(subheader),
            st.caption(caption),
            st.write(text),
            st.data_editor(data, column_order=column_order, hide_index=True),
        )


def get_random_word(data: pd.DataFrame, selected_language: str):
    """Récupère un mot aléatoire grâce à un index aléatoire dans le dataframe."""
    if selected_language == "FR":
        random_index = np.random.randint(len(data))
        return data.iloc[random_index]["French"], data.iloc[random_index]["English"]
    else:
        random_index = np.random.randint(len(data))
        return data.iloc[random_index]["English"], data.iloc[random_index]["French"]


def check_session_state(data: pd.DataFrame, selected_language: str):
    if "random_word" not in st.session_state:
        (
            st.session_state.random_word,
            st.session_state.correct_translation,
        ) = get_random_word(data, selected_language)


def userform(selected_language: str):
    """Crée la userform permettant à l'utilisateur d'entrer sa réponse et de changer pour obtenir un nouveau mot."""
    if selected_language == "FR":
        with st.form("myform", clear_on_submit=True):
            user_translation = st.text_input("🖍 Ma traduction en anglais", key="trad")
            col1, col2 = st.columns([1, 1])
            with col1:
                submit = st.form_submit_button(label="📤 Envoyer ma réponse")
            with col2:
                clear = st.form_submit_button(
                    label="🆕 Obtenir un nouveau texte aléatoire"
                )
    else:
        with st.form("myform", clear_on_submit=True):
            user_translation = st.text_input("🖍 My translation in french", key="trad")
            col1, col2 = st.columns([1, 1])
            with col1:
                submit = st.form_submit_button(label="📤 Send my answer")
            with col2:
                clear = st.form_submit_button(label="🆕 Get a new random text")
    return user_translation, submit, clear


def rand_text_subheader(selected_language: str):
    """Crée le texte du mode random text."""
    if st.session_state.random_word.count(" ") == 0:
        type_fr, type_en = "du mot", "from the word"
    elif st.session_state.random_word.count(" ") < 4:
        type_fr, type_en = "de l'expression", "from the expression"
    elif st.session_state.random_word.count(" ") >= 4:
        type_fr, type_en = "de la phrase", "from the sentence"
    if selected_language == "FR":
        subheader = "🎲 Traduction de texte aléatoire"
        markdown = f"> Veuillez entrer la traduction {type_fr} : `{st.session_state.random_word}` en **Anglais**"
    else:
        subheader = "🎲 Random text translation"
        markdown = f"> Please enter the translation {type_en} : `{st.session_state.random_word}` in **French**"
    return st.subheader(subheader), st.markdown(markdown)


def post_submit(
    selected_language: str, user_translation: str, nlp_fr: Language, nlp_en: Language
):
    """Affiche un message selon que la traduction soit bonne ou non."""
    if selected_language == "FR":
        if user_translation.strip() == "":
            response = st.warning("🤷‍♀️ Aucune traduction n'a été entrée...")
        elif user_translation.strip() == st.session_state.correct_translation:
            response = st.success("✅ Traduction correcte !")
        else:
            response = st.error(
                f"❌ Traduction incorrecte ! La **traduction attendue** était : *{st.session_state.correct_translation}*"
            )
            # doc = nlp_en(st.session_state.correct_translation)
            # sentence = [(str(token), token.pos_) for token in doc]
            st.divider()
            # annotated_text(sentence)

    else:
        if user_translation.strip() == "":
            response = st.warning("🤷‍♀️ No translation has been detected...")
        elif user_translation.strip() == st.session_state.correct_translation:
            response = st.success("✅ Correct translation!")
        else:
            response = st.error(
                f"❌ Incorrect translation! The **expected translation** was : *{st.session_state.correct_translation}*"
            )
            # doc = nlp_fr(st.session_state.correct_translation)
            # sentence = [(str(token), token.pos_) for token in doc]
            st.divider()
            # annotated_text(sentence)
    return response


def random_text(data: pd.DataFrame, selected_language: str):
    """Orchestre l'ensemble des fonctions pour générer du texte aléatoire."""
    if data is not None:
        check_session_state(data, selected_language)
        rand_text_subheader(selected_language)
        user_translation, submit, clear = userform(selected_language)
        return user_translation, submit, clear
