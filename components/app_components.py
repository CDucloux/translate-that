"""
app_components
==============
⚙ This module holds all the components of `translate-that` streamlit app
"""

import streamlit as st
import pandas as pd
import numpy as np
from streamlit.delta_generator import DeltaGenerator


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


def import_fontawesome():
    """Importe Font Awesome as a Stylesheet."""
    fa_import = """<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">"""
    return st.write(fa_import, unsafe_allow_html=True)


def select_language() -> str:
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


def check_columns(data: pd.DataFrame) -> bool:
    """Permet de vérifier que les colonnes French & English existent dans le fichier."""
    valid_col_1 = "French"
    valid_col_2 = "English"
    if data is not None:
        if valid_col_1 and valid_col_2 not in data.columns:
            return False
        else:
            return True
    return False


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


def select_mode(data: pd.DataFrame, selected_language: str) -> str | None:
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


def display_author(selected_language: str):
    if selected_language == "FR":
        text = "**:blue[Auteur]** : [CDucloux](https://corentinducloux.fr/)"
    else:
        text = "**:blue[Author]** : [CDucloux](https://corentinducloux.fr/)"
    return st.sidebar.write(
        f'| 💻 {text} &#160;  <i class="fa-solid fa-external-link"></i>',
        unsafe_allow_html=True,
    )


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


def get_random_word(data: pd.DataFrame, selected_language: str) -> tuple[str, str]:
    """Récupère un mot aléatoire grâce à un index aléatoire dans le dataframe."""
    if selected_language == "FR":
        random_index = np.random.randint(len(data))
        return data.iloc[random_index]["French"], data.iloc[random_index]["English"]
    else:
        random_index = np.random.randint(len(data))
        return data.iloc[random_index]["English"], data.iloc[random_index]["French"]


def check_session_state(data: pd.DataFrame, selected_language: str) -> None:
    if "random_word" not in st.session_state:
        (
            st.session_state.random_word,
            st.session_state.correct_translation,
        ) = get_random_word(data, selected_language)


def userform(selected_language: str) -> tuple[str, bool, bool]:
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
    else:
        type_fr, type_en = "de la phrase", "from the sentence"
    if selected_language == "FR":
        subheader = "🎲 Traduction de texte aléatoire"
        markdown = f"> Veuillez entrer la traduction {type_fr} : `{st.session_state.random_word}` en **Anglais**"
    else:
        subheader = "🎲 Random text translation"
        markdown = f"> Please enter the translation {type_en} : `{st.session_state.random_word}` in **French**"
    return st.subheader(subheader), st.markdown(markdown)


def post_submit(selected_language: str, user_translation: str) -> DeltaGenerator:
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
    else:
        if user_translation.strip() == "":
            response = st.warning("🤷‍♀️ No translation has been detected...")
        elif user_translation.strip() == st.session_state.correct_translation:
            response = st.success("✅ Correct translation!")
        else:
            response = st.error(
                f"❌ Incorrect translation! The **expected translation** was : *{st.session_state.correct_translation}*"
            )
    return response


def random_text(
    data: pd.DataFrame, selected_language: str
) -> tuple[str, bool, bool] | None:
    """Orchestre l'ensemble des fonctions pour générer du texte aléatoire."""
    if data is not None:
        check_session_state(data, selected_language)
        rand_text_subheader(selected_language)
        user_translation, submit, clear = userform(selected_language)
        return user_translation, submit, clear
    else:
        return None


def increment_index():
    st.session_state.index += 1


def get_next_word(data: pd.DataFrame, selected_language: str) -> tuple[str, str]:
    """Récupère le prochain mot grâce à un index dans le dataframe."""
    if selected_language == "FR":
        return (
            data.iloc[st.session_state.index]["French"],
            data.iloc[st.session_state.index]["English"],
        )
    else:
        return (
            data.iloc[st.session_state.index]["English"],
            data.iloc[st.session_state.index]["French"],
        )


def check_session_state_train(data: pd.DataFrame, selected_language: str) -> None:
    """Cette fonction permet de vérifier les différents states de la session active en session d'entrainement.

    Plus précisément :

    - `next_word` => le prochain mot obtenu grâce à l'index
    - `index` => l'index du dataframe
    - `score` => le score en session d'entrainement
    """
    if "next_word" not in st.session_state:
        (
            st.session_state.next_word,
            st.session_state.correct_translation_train,
        ) = get_next_word(data, selected_language)


def train_text_subheader(selected_language: str):
    """Crée le texte du mode train text."""
    if st.session_state.next_word.count(" ") == 0:
        type_fr, type_en = "du mot", "from the word"
    elif st.session_state.next_word.count(" ") < 4:
        type_fr, type_en = "de l'expression", "from the expression"
    else:
        type_fr, type_en = "de la phrase", "from the sentence"
    if selected_language == "FR":
        subheader = "🏋️‍♂️ Session d'entraînement"
        markdown = f"> Veuillez entrer la traduction {type_fr} : `{st.session_state.next_word}` en **Anglais**"
    else:
        subheader = "🏋️‍♂️ Training session"
        markdown = f"> Please enter the translation {type_en} : `{st.session_state.next_word}` in **French**"
    return st.subheader(subheader), st.markdown(markdown)


def userform_train(selected_language: str) -> tuple[str, bool, bool]:
    """Crée la userform permettant à l'utilisateur d'entrer sa réponse et de changer pour obtenir un nouveau mot."""
    if selected_language == "FR":
        with st.form("myform", clear_on_submit=True):
            user_translation = st.text_input("🖍 Ma traduction en anglais", key="trad")
            col1, col2 = st.columns([1, 1])
            with col1:
                submit = st.form_submit_button(label="📤 Envoyer ma réponse")
            with col2:
                clear = st.form_submit_button(
                    label="🆕 Obtenir le prochain texte", on_click=increment_index
                )
    else:
        with st.form("myform", clear_on_submit=True):
            user_translation = st.text_input("🖍 My translation in french", key="trad")
            col1, col2 = st.columns([1, 1])
            with col1:
                submit = st.form_submit_button(label="📤 Send my answer")
            with col2:
                clear = st.form_submit_button(
                    label="🆕 Get the next text", on_click=increment_index
                )
    return user_translation, submit, clear


def post_submit_train(
    selected_language: str, user_translation_train: str
) -> DeltaGenerator:
    """Affiche un message selon que la traduction soit bonne ou non."""
    if selected_language == "FR":
        if user_translation_train.strip() == "":
            response = st.warning("🤷‍♀️ Aucune traduction n'a été entrée...")
        elif (
            user_translation_train.strip() == st.session_state.correct_translation_train
        ):
            response = st.success("✅ Traduction correcte !")
            st.session_state.score += 1
        else:
            response = st.error(
                f"❌ Traduction incorrecte ! La **traduction attendue** était : *{st.session_state.correct_translation_train}*"
            )
    else:
        if user_translation_train.strip() == "":
            response = st.warning("🤷‍♀️ No translation has been detected...")
        elif (
            user_translation_train.strip() == st.session_state.correct_translation_train
        ):
            response = st.success("✅ Correct translation!")
            st.session_state.score += 1
        else:
            response = st.error(
                f"❌ Incorrect translation! The **expected translation** was : *{st.session_state.correct_translation_train}*"
            )
    return response


def index_writer_train(data: pd.DataFrame, selected_language: str) -> DeltaGenerator:
    """Permet d'écrire l'index en cours d'utilisation dans le mode train."""
    if selected_language == "FR":
        text = "Indice actuel"
    else:
        text = "Current index"
    return st.write(
        f"⚙ {text} $\Rightarrow$ {st.session_state.index}/**{len(data)-1}**"
    )


def score_writer_train(selected_language: str) -> DeltaGenerator:
    """Permet d'écrire le score en cours d'incrémentation dans le mode train."""
    if selected_language == "FR":
        text = "Score actuel"
    else:
        text = "Current score"
    return st.write(f"🏆 {text} $\Rightarrow$ `{st.session_state.score}`")


def final_scorer(data: pd.DataFrame):
    """Permet de générer le score final /20."""
    score_20 = round(st.session_state.score / len(data) * 20, 2)
    if score_20 < 1.7:
        st.error(
            f"🔫 Score final : {score_20}/20 $-$ **Affligeant**. Même *Anne Hidalgo* a eu un meilleur score aux présidentielles 😂"
        )
    elif score_20 < 4:
        st.error(
            f"🚨 Score final : {score_20}/20 $-$ **Lamentable**. Si peu d'effort a été fourni que je ne peux même pas en rire. Quoique."
        )
    elif score_20 < 6:
        st.error(
            f"🧨 Score final : {score_20}/20 $-$ **Horreur**. Même moi en maternelle je faisais mieux..."
        )
    elif score_20 < 8:
        st.error(
            f"😤 Score final : {score_20}/20 $-$ **Minable**. Il faudra pas venir pleurer quand le conseil de classe viendra..."
        )
    elif score_20 < 10:
        st.error(
            f"🤐 Score final : {score_20}/20 $-$ **Médiocre**. Un score à la hauteur de ton quotient intellectuel ."
        )
    elif score_20 < 11:
        st.warning(
            f"😑 Score final : {score_20}/20 $-$ **Insuffisant**. Des erreurs impardonnables."
        )
    elif score_20 < 12:
        st.warning(
            f"😐 Score final : {score_20}/20 $-$ **Moyen**. Compte tenu du manque de travail, pas étonnant."
        )
    elif score_20 < 14:
        st.success(
            f"🥴 Score final : {score_20}/20 $-$ **Potable**. Pourquoi pas 20 ? Ahah, parce que ce n'est pas à ta portée."
        )
    elif score_20 < 16:
        st.success(
            f"🥱 Score final : {score_20}/20 $-$ **Correct**. Ne prends pas tes grands airs, si tu as cette note c'est parce qu'il n'y a pas de concurrence."
        )
    elif score_20 < 18:
        st.success(
            f"🥉 Score final : {score_20}/20 $-$ **Bien**. Quelques étourderies. Quand on est cadre sup on peut pas se permettre."
        )
    elif score_20 < 20:
        st.success(
            f"🥈 Score final : {score_20}/20 $-$ **Très Bien**. Presque parfait, mais tu es destiné à être un éternel second 😇."
        )
    else:
        st.success(
            f"🥇 Score final : {score_20}/20 $-$ **Excellent**. Aussi bon que moi, mais pas meilleur."
        )
