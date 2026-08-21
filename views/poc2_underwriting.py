import base64
import re
from datetime import date

import altair as alt
import pandas as pd
import streamlit as st

STEPS = [
    {
        "id": "projet",
        "label": "Projet",
    },
    {
        "id": "recommandation",
        "label": "Recommandation",
        "question": "Quel niveau d'accompagnement souhaitez-vous ?",
        "options": [
            "Pilotage automatique",
            "Conseil trimestriel",
            "Conseil annuel",
            "Gestion libre",
        ],
    },
    {
        "id": "souscription",
        "label": "Souscription",
        "question": "Quel rythme de versement préférez-vous ?",
        "options": [
            "Versement initial unique",
            "Versement mensuel",
            "Versement trimestriel",
            "Versement libre",
        ],
    },
    {
        "id": "justificatifs",
        "label": "Justificatifs",
        "question": "Comment souhaitez-vous transmettre vos justificatifs ?",
        "options": [
            "Dépôt sécurisé en ligne",
            "Envoi par email",
            "En agence",
            "Je le ferai plus tard",
        ],
    },
    {
        "id": "signature",
        "label": "Signature",
        "question": "Quel mode de signature préférez-vous ?",
        "options": [
            "Signature électronique immédiate",
            "Signature avec code SMS",
            "Signature en visio avec conseiller",
            "Signature en agence",
        ],
    },
]

PROJECT_QUESTIONS = [
    {
        "id": "q1_projet",
        "question": "Quel est votre projet d'investissement ?",
        "options": [
            "Faire fructifier mon épargne",
            "Épargner en cas de coup dur",
            "Préparer un achat important",
            "Prévoir ma retraite",
            "Transmettre mon patrimoine",
            "Ouvrir un compte enfant",
            "Organiser ma trésorerie pro",
        ],
    },
    {
        "id": "q2_montant_initial",
        "question": "Quel montant souhaitez-vous placer chez CNP ?",
        "options": ["10 000 €", "35 000 €", "50 000 €", "150 000 €", "500 000 €"],
        "free_input": True,
        "free_input_label": "Ou saisie libre :",
        "free_input_placeholder": "Ex : 75 000 €",
        "robot_info": "Avec CNP, votre épargne n'est pas bloquée : vous pouvez continuer d'investir dès votre compte ouvert et retirer à tout moment.",
    },
    {
        "id": "q3_montant_mensuel",
        "question": "Quel montant régulier souhaitez-vous placer chaque mois ?",
        "options": ["100 €", "200 €", "500 €", "1 000 €", "1 500 €"],
        "free_input": True,
        "free_input_label": "Ou saisie libre :",
        "free_input_placeholder": "Ex : 750 €",
        "robot_info": "Les versements sont modulables : placez le montant que vous souhaitez, à la fréquence que vous souhaitez. Ils sont modifiables à tout moment, et toujours sans frais !",
    },
    {
        "id": "q4_horizon",
        "question": "Dans combien de temps souhaitez-vous profiter de cet investissement ?",
        "options": [
            "Moins de 3 ans",
            "Entre 3 et 5 ans",
            "Entre 5 et 10 ans",
            "Plus de 10 ans",
        ],
        "free_input": True,
        "free_input_label": "Choix / Saisie renseignée :",
        "free_input_placeholder": "Ex : 7 ans",
        "robot_info": "Cette information nous permet de vous proposer une simulation en accord avec votre horizon d'investissement. Votre argent pourra être débloqué avant sans difficulté et sans frais.",
    },
    {
        "id": "q5_naissance",
        "question": "Quelle est votre date de naissance ?",
        "input_type": "date",
    },
    {
        "id": "q6_resident_fiscal",
        "question": "Êtes-vous résident fiscal français ?",
        "options": ["Oui", "Non"],
        "robot_info": "Si vous payez des impôts sur le revenu en France, DOM inclus, vous êtes résident fiscal français.",
    },
    {
        "id": "q7_durable",
        "question": "Avez-vous une préférence pour des investissements respectant les critères durables, environnementaux, sociaux et de gouvernance ?",
        "options": ["Oui", "Non"],
        "robot_info": "La durabilité désigne la capacité d'un système, d'une ressource ou d'une activité à se maintenir dans le temps, sans nuire à l'environnement. [Lire plus]",
        "sub_question": "Souhaitez-vous bénéficier de l'approche ESG CNP ou d'une approche personnalisée ?",
        "sub_options": ["Approche ESG CNP", "Approche personnalisée"],
        "sub_info": "L'ESG est un ensemble de critères utilisés pour évaluer les pratiques durables et socialement responsables des entreprises. [Lire plus]",
    },
    {
        "id": "q8_patrimoine_immo",
        "question": "Quelle est la valeur de votre patrimoine immobilier NET ?",
        "explain": "Additionnez la valeur de vos biens (appartement, maison) puis déduisez le montant qu'il vous reste à rembourser. Une estimation nous convient.",
        "options": ["10 000 €", "50 000 €", "100 000 €", "250 000 €", "500 000 €"],
        "free_input": True,
        "free_input_label": "Ou saisie libre :",
        "free_input_placeholder": "Ex : 100 000 €",
        "robot_info": "Par exemple, si vous êtes propriétaire d'un bien immobilier de 300 000 € et qu'il vous reste 200 000 € à rembourser sur votre crédit, renseignez la différence, soit 100 000 €.",
    },
    {
        "id": "q9_patrimoine_financier",
        "question": "Quel est le montant estimé de votre patrimoine financier ?",
        "explain": "Additionnez vos avoirs financiers : compte courant, livrets d'épargne, PEL, assurances-vie, PEA, comptes-titres, PEE, etc., hors patrimoine immobilier.",
        "options": ["30 000 €", "50 000 €", "100 000 €", "250 000 €", "500 000 €"],
        "free_input": True,
        "free_input_label": "Ou saisie libre :",
        "free_input_placeholder": "Ex : 80 000 €",
        "robot_info": "Vous aviez prévu de placer 35 000 € chez CNP. Si cette somme est supérieure à votre patrimoine financier, vérifiez qu'il n'y a pas une erreur.",
    },
    {
        "id": "q10_besoin_total_2_ans",
        "question": "Pourriez-vous avoir besoin de toute l'épargne placée chez CNP d'ici 2 ans ?",
        "options": ["Certainement pas", "Probablement pas", "Probablement", "Très probablement"],
    },
    {
        "id": "q11_besoin_moitie_10_ans",
        "question": "Pourriez-vous avoir besoin de la moitié de votre investissement avant 10 ans ?",
        "options": ["Certainement pas", "Probablement pas", "Probablement", "Très probablement"],
    },
    {
        "id": "q12_experience",
        "question": "Avez-vous déjà placé de l'argent sur un contrat d'assurance-vie, un compte-titres ou un PEA ?",
        "options": ["Oui", "Non"],
        "robot_info": "Cette question nous permet d'en savoir plus sur vos expériences précédentes en matière d'investissement.",
    },
    {
        "id": "q13_gain_risque",
        "question": "« Une perspective de gain élevé implique un risque de perte en capital fort » : cette affirmation vous semble-t-elle vraie ?",
        "options": ["Vrai", "Faux", "Je ne sais pas"],
        "feedback": {
            "Vrai": "Bonne réponse. Plus vous cherchez de hauts rendements et plus vous devez prendre des risques avec vos placements.",
            "Faux": "Cette affirmation est vraie : rendement élevé et risque élevé vont souvent ensemble.",
            "Je ne sais pas": "Cette affirmation est vraie : rendement élevé et risque élevé vont souvent ensemble.",
        },
    },
    {
        "id": "q14_etf",
        "question": "« Un ETF est un fonds à capital garanti » : cette affirmation vous semble-t-elle vraie ?",
        "options": ["Vrai", "Faux", "Je ne sais pas"],
        "feedback": {
            "Faux": "Bonne réponse. Un ETF est un fonds qui réplique un indice boursier. Il peut donc varier à la hausse comme à la baisse. Il ne s'agit pas d'un fonds à capital garanti.",
            "Vrai": "Mauvaise réponse. Un ETF réplique un indice et n'est pas un fonds à capital garanti.",
            "Je ne sais pas": "À retenir : un ETF réplique un indice et n'est pas un fonds à capital garanti.",
        },
    },
    {
        "id": "q15_gestion_delegatee",
        "question": "« En déléguant la gestion de mon portefeuille à une société de gestion, je renonce à prendre moi-même les décisions d'investissement sur celui-ci » : cette affirmation vous semble-t-elle vraie ?",
        "options": ["Vrai", "Faux", "Je ne sais pas"],
        "feedback": {
            "Vrai": "Bonne réponse. Confier votre portefeuille à CNP revient à laisser les manettes à nos gérants. Les dépôts et retraits restent à votre main.",
            "Faux": "Mauvaise réponse. En gestion déléguée, les arbitrages sont bien confiés aux gérants.",
            "Je ne sais pas": "En gestion déléguée, les arbitrages sont confiés aux gérants, et vos dépôts/retraits restent possibles.",
        },
    },
    {
        "id": "q16_pertes_subies",
        "question": "Avez-vous déjà subi des pertes sur vos placements financiers ?",
        "options": [
            "Non, je n'ai jamais subi de perte sur mes placements financiers",
            "Oui, de 10% maximum",
            "Oui, de 20% maximum",
            "Oui, de plus de 20%",
        ],
    },
    {
        "id": "q17_ratio_5_ans",
        "question": "Quel rapport gains / pertes êtes-vous prêt à accepter en investissant 10 000 € sur 5 ans ?",
        "explain": "Il n'y a pas de bonne ou de mauvaise réponse. Les montants proposés nous permettent de mieux comprendre votre attitude face au risque. Ils ne sont pas nécessairement représentatifs de la réalité.",
        "options": [
            "Gain potentiel 5 000 € / Perte potentielle 2 000 €",
            "Gain potentiel 2 000 € / Perte potentielle 1 000 €",
            "Gain potentiel 1 000 € / Perte potentielle 400 €",
            "Gain potentiel 500 € / Perte potentielle 0 €",
        ],
    },
    {
        "id": "q18_ratio_10_ans",
        "question": "Quel rapport gains / pertes êtes-vous prêt à accepter en investissant sur 10 ans ?",
        "explain": "Là encore, nous cherchons à comprendre votre attitude face au risque.",
        "options": [
            "Gain potentiel 8 000 € / Perte potentielle 3 500 €",
            "Gain potentiel 5 000 € / Perte potentielle 2 000 €",
            "Gain potentiel 3 000 € / Perte potentielle 1 000 €",
            "Gain potentiel 1 500 € / Perte potentielle 0 €",
        ],
    },
    {
        "id": "q19_crise",
        "question": "Si votre investissement perd 10% de sa valeur en 3 mois, que faites-vous ?",
        "explain": "Un dernier effort : votre comportement pendant une crise nous permet de définir votre profil.",
        "options": [
            "Je réinvestis pour profiter de cette opportunité",
            "Je patiente sans paniquer",
            "Je vends une partie pour limiter mes pertes potentielles",
            "Je vends tout",
            "Je ne sais pas",
        ],
    },
]

REGION_DISTRIBUTION = [
    {"label": "Amérique du nord", "value": 54.5, "color": "#102065"},
    {"label": "Europe", "value": 26.7, "color": "#36A3DE"},
    {"label": "Asie pacifique", "value": 9.8, "color": "#03AFA7"},
    {"label": "Japon", "value": 5.8, "color": "#D9016D"},
    {"label": "Amérique latine", "value": 0.8, "color": "#FFA92C"},
]

ASSET_COLORS = {
    "fonds_euros": "#102065",
    "obligations": "#03AFA7",
    "actions": "#D9016D",
}


def _img_base64(path: str):
    try:
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")
    except Exception:
        return None


def _init_state():
    if "poc2_step_idx" not in st.session_state:
        st.session_state.poc2_step_idx = 0
    if "poc2_answers" not in st.session_state:
        st.session_state.poc2_answers = {}
    if "poc2_done" not in st.session_state:
        st.session_state.poc2_done = False
    if "poc2_project_idx" not in st.session_state:
        st.session_state.poc2_project_idx = 0
    if "poc2_project_answers" not in st.session_state:
        st.session_state.poc2_project_answers = {}
    if "poc2_feedback" not in st.session_state:
        st.session_state.poc2_feedback = ""
    if "poc2_feedback_qid" not in st.session_state:
        st.session_state.poc2_feedback_qid = ""


def _advance_project_question():
    q_idx = st.session_state.poc2_project_idx
    if q_idx < len(PROJECT_QUESTIONS) - 1:
        st.session_state.poc2_project_idx = q_idx + 1
    else:
        st.session_state.poc2_step_idx = 1
        st.session_state.poc2_answers["projet"] = "Projet complété"


def _render_stepper(active_idx: int):
    parts = []
    for idx, step in enumerate(STEPS):
        if idx < active_idx:
            cls = "done"
        elif idx == active_idx:
            cls = "active"
        else:
            cls = "todo"

        parts.append(
            f"<div class='poc2-step {cls}'><span class='poc2-step-num'>{idx + 1}</span><span>{step['label']}</span></div>"
        )

    st.markdown(
        f"<div class='poc2-stepper'>{''.join(parts)}</div>",
        unsafe_allow_html=True,
    )


def _render_styles():
    st.markdown(
        """
        <style>
        .stApp {
            background: #F5F8FF !important;
        }

        .main .block-container {
            padding-top: 1.2rem;
            padding-bottom: 2rem;
        }

        .poc2-stepper {
            display: flex;
            gap: 10px;
            margin: 6px 0 18px 0;
            flex-wrap: wrap;
        }

        .poc2-step {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            border-radius: 999px;
            padding: 6px 12px;
            border: 1px solid #D8DEEB;
            background: #FFFFFF;
            color: #002261;
            font-weight: 600;
            font-size: 0.9rem;
        }

        .poc2-step-num {
            width: 22px;
            height: 22px;
            border-radius: 999px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 0.78rem;
            font-weight: 700;
            border: 1px solid #C9D5EE;
            background: #FFFFFF;
            color: #002261;
        }

        .poc2-step.active {
            border-color: #002261;
            background: #002261;
            color: #FFFFFF;
        }

        .poc2-step.active .poc2-step-num {
            border-color: #FFFFFF;
            color: #002261;
            background: #FFFFFF;
        }

        .poc2-step.done {
            border-color: #02ADA5;
            background: #E6F7F6;
            color: #027A74;
        }

        .poc2-step.done .poc2-step-num {
            border-color: #02ADA5;
            background: #02ADA5;
            color: #FFFFFF;
        }

        .poc2-card-head {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 20px;
            margin-bottom: 8px;
        }

        .poc2-head-left {
            color: #002261;
            font-size: 0.95rem;
            font-weight: 600;
        }

        .poc2-head-right {
            color: #002261;
            font-size: 0.9rem;
            font-weight: 600;
            white-space: nowrap;
        }

        .poc2-rec-head {
            color: #002261;
            font-size: 2rem;
            line-height: 1.15;
            font-weight: 800;
            margin: 2px 0 8px 0;
        }

        .poc2-rec-text {
            color: #4D5D80;
            font-size: 0.95rem;
            line-height: 1.45;
            margin: 0 0 12px 0;
        }

        .poc2-question {
            text-align: center;
            color: #002261;
            font-size: 1.85rem;
            line-height: 1.2;
            margin: 24px 0 18px 0;
            font-weight: 700;
        }

        .poc2-explain {
            text-align: center;
            color: #4D5D80;
            font-size: 0.92rem;
            margin: -8px 0 14px 0;
        }

        div[data-testid="stButton"] {
            background: transparent !important;
            background-color: transparent !important;
            margin-top: 0 !important;
            margin-bottom: 0 !important;
        }

        div[data-testid="stButton"] button *,
        div[data-testid="stButton"] button div,
        div[data-testid="stButton"] button p,
        div[data-testid="stButton"] button span {
            background: transparent !important;
            background-color: transparent !important;
            box-shadow: none !important;
            text-shadow: none !important;
            outline: none !important;
        }

        div[data-testid="stButton"] > button[kind="secondary"],
        div[data-testid="stButton"] > button[data-testid="baseButton-secondary"] {
            background-color: #FFFFFF !important;
            color: #002261 !important;
            border: 1px solid #D8DEEB !important;
            border-radius: 14px !important;
            min-height: 54px !important;
            font-weight: 600 !important;
            padding: 0.5rem 1rem !important;
            box-shadow: none !important;
            outline: none !important;
        }

        div[data-testid="stButton"] > button[kind="secondary"]:hover,
        div[data-testid="stButton"] > button[kind="secondary"]:focus,
        div[data-testid="stButton"] > button[kind="secondary"]:active,
        div[data-testid="stButton"] > button[kind="secondary"]:focus-visible,
        div[data-testid="stButton"] > button[data-testid="baseButton-secondary"]:hover,
        div[data-testid="stButton"] > button[data-testid="baseButton-secondary"]:focus,
        div[data-testid="stButton"] > button[data-testid="baseButton-secondary"]:active {
            background-color: rgba(2, 173, 165, 0.14) !important;
            color: #027A74 !important;
            border-color: #02ADA5 !important;
            box-shadow: none !important;
            outline: none !important;
        }

        div[data-testid="stButton"] > button[kind="primary"],
        div[data-testid="stButton"] > button[data-testid="baseButton-primary"] {
            background-color: #002261 !important;
            color: #FFFFFF !important;
            border: 1px solid #002261 !important;
            border-radius: 999px !important;
            min-height: 56px !important;
            font-weight: 700 !important;
            padding: 0.65rem 1rem !important;
            box-shadow: none !important;
            outline: none !important;
        }

        div[data-testid="stButton"] > button[kind="primary"]:hover,
        div[data-testid="stButton"] > button[kind="primary"]:focus,
        div[data-testid="stButton"] > button[kind="primary"]:active,
        div[data-testid="stButton"] > button[data-testid="baseButton-primary"]:hover,
        div[data-testid="stButton"] > button[data-testid="baseButton-primary"]:focus,
        div[data-testid="stButton"] > button[data-testid="baseButton-primary"]:active {
            background-color: #5E6778 !important;
            border-color: #5E6778 !important;
            color: #FFFFFF !important;
            box-shadow: none !important;
            outline: none !important;
        }

        div[data-testid="stLayoutWrapper"] > div[data-testid="stVerticalBlock"] {
            background-color: #FFFFFF !important;
            border: 1px solid #D8DEEB !important;
            border-radius: 18px !important;
            padding: 16px 20px 20px 20px !important;
            margin: 4px 0 20px 0 !important;
            box-shadow: none !important;
        }

        .poc2-nav-row {
            margin-top: 2px;
            margin-bottom: 8px;
        }

        div[data-testid="stProgressBar"] > div > div {
            background-color: #02ADA5;
        }

        .poc2-recap {
            background: #E6F7F6;
            border: 1px solid #9CDDD9;
            color: #027A74;
            border-radius: 12px;
            padding: 12px 14px;
            margin: 10px 0 6px 0;
            font-weight: 600;
        }

        .poc2-free-label {
            color: #002261;
            font-weight: 700;
            margin: 8px 0 6px 0;
            font-size: 0.95rem;
        }

        .poc2-robot-info {
            margin-top: 14px;
            margin-bottom: 14px;
            background: #F3F8FF;
            border: 1px solid #D3E1FA;
            border-radius: 14px;
            padding: 10px 12px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .poc2-robot-info img {
            width: 42px;
            height: 42px;
            object-fit: contain;
            flex: 0 0 auto;
        }

        .poc2-robot-info-text {
            color: #1F3E7A;
            font-size: 0.9rem;
            line-height: 1.35;
            font-weight: 600;
        }

        .poc2-profile-card {
            background: #002261;
            border: 1px solid #001A4A;
            border-radius: 14px;
            padding: 12px 14px;
            margin-top: 4px;
            margin-bottom: 12px;
        }

        .poc2-profile-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 10px;
            margin-bottom: 6px;
            color: #FFFFFF;
            font-size: 0.9rem;
        }

        .poc2-profile-title {
            font-weight: 800;
            color: #002261;
            font-size: 1.05rem;
            margin: 10px 0 6px 0;
        }

        .poc2-profile-text {
            color: #4B5A7B;
            font-size: 0.88rem;
            line-height: 1.4;
            margin-bottom: 10px;
        }

        .poc2-profile-score {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 28px;
            height: 28px;
            border-radius: 8px;
            border: 1px solid #E8DC9E;
            background: #FFF8DA;
            color: #7A6616;
            font-size: 0.95rem;
            font-weight: 800;
            margin-bottom: 6px;
        }

        .poc2-gauge {
            margin: 10px 0 12px 0;
        }

        .poc2-gauge-label {
            color: #002261;
            font-size: 0.82rem;
            font-weight: 700;
            margin-bottom: 4px;
        }

        .poc2-gauge-track {
            height: 7px;
            border-radius: 999px;
            background: #E6EDF8;
            overflow: hidden;
        }

        .poc2-gauge-fill {
            height: 100%;
            background: #002261;
            border-radius: 999px;
        }

        .poc2-gauge-ends {
            margin-top: 2px;
            display: flex;
            justify-content: space-between;
            color: #002261;
            font-size: 0.72rem;
            font-weight: 600;
        }

        .poc2-alert {
            margin-top: 8px;
            background: #FFF4E9;
            border: 1px solid #F1D6B5;
            border-radius: 10px;
            color: #7E4E12;
            font-size: 0.84rem;
            font-weight: 600;
            padding: 8px 10px;
        }

        .poc2-section-card {
            background: #FFFFFF;
            border: 1px solid #D8DEEB;
            border-radius: 16px;
            padding: 16px 16px 14px 16px;
            margin: 16px 0 14px 0;
        }

        .poc2-section-title {
            color: #002261;
            font-size: 1rem;
            font-weight: 800;
            margin-bottom: 14px;
        }

        .poc2-donut-wrap {
            display: flex;
            justify-content: center;
            margin-bottom: 0;
        }

        .poc2-donut-layout {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 18px;
            margin-bottom: 4px;
        }

        .poc2-donut-legend {
            display: grid;
            grid-template-columns: 1fr;
            gap: 8px;
            flex: 1 1 auto;
            min-width: 280px;
        }

        .poc2-donut-item {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
        }

        .poc2-donut-item-left {
            display: flex;
            align-items: center;
            gap: 10px;
            color: #002261;
            font-size: 0.92rem;
            font-weight: 700;
        }

        .poc2-donut-dot {
            width: 12px;
            height: 12px;
            border-radius: 999px;
            flex: 0 0 auto;
        }

        .poc2-donut-value {
            color: #4B5A7B;
            font-size: 0.9rem;
            font-weight: 700;
        }

        .poc2-donut-meta {
            display: flex;
            flex-direction: column;
            gap: 1px;
        }

        .poc2-donut-sub {
            color: #6E7FA5;
            font-size: 0.78rem;
            font-weight: 600;
            line-height: 1.2;
        }

        .poc2-geo-bars {
            display: grid;
            grid-template-columns: 1fr;
            gap: 10px;
        }

        .poc2-geo-row {
            display: grid;
            grid-template-columns: 220px 1fr 64px;
            align-items: center;
            gap: 10px;
        }

        .poc2-geo-label {
            display: flex;
            align-items: center;
            gap: 8px;
            color: #002261;
            font-size: 0.9rem;
            font-weight: 700;
        }

        .poc2-geo-track {
            width: 100%;
            height: 12px;
            border-radius: 999px;
            background: #E9EEF8;
            overflow: hidden;
        }

        .poc2-geo-fill {
            height: 100%;
            border-radius: 999px;
        }

        .poc2-geo-value {
            text-align: right;
            color: #4B5A7B;
            font-size: 0.9rem;
            font-weight: 700;
        }

        .poc2-sim-sub {
            color: #6E7FA5;
            font-size: 0.9rem;
            margin-top: -8px;
            margin-bottom: 8px;
        }

        .poc2-sim-chart-wrap {
            background: #FFFFFF;
            border: 1px solid #E6ECF8;
            border-radius: 14px;
            padding: 8px;
            margin-bottom: 10px;
        }

        .poc2-sim-legend {
            display: grid;
            grid-template-columns: 1fr;
            gap: 6px;
            margin-top: 6px;
        }

        .poc2-sim-leg-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 12px;
            color: #002261;
            font-size: 0.9rem;
            font-weight: 700;
        }

        .poc2-sim-leg-left {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .poc2-sim-note {
            margin-top: 10px;
            color: #5A6C92;
            font-size: 0.82rem;
            line-height: 1.4;
        }

        @media (max-width: 860px) {
            .poc2-donut-layout {
                flex-direction: column;
                align-items: center;
            }

            .poc2-donut-legend {
                width: 100%;
                min-width: 0;
            }

            .poc2-geo-row {
                grid-template-columns: 1fr;
                gap: 6px;
            }

            .poc2-geo-value {
                text-align: left;
            }
        }

        div[data-testid="stTextInput"] input,
        div[data-testid="stDateInput"] input {
            border-radius: 12px !important;
            border: 1px solid #C8D4EE !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _save_project_answer(qid: str, value: str):
    st.session_state.poc2_project_answers[qid] = value


def _parse_amount(value: str) -> float:
    if not value:
        return 0.0
    digits = re.findall(r"\d+", str(value).replace("\u202f", " "))
    if not digits:
        return 0.0
    return float("".join(digits))


def _extract_years(value: str) -> float | None:
    if not value:
        return None
    text = str(value).lower()
    if "moins" in text and "3" in text:
        return 2.0
    if "3" in text and "5" in text:
        return 4.0
    if "5" in text and "10" in text:
        return 7.0
    if "plus" in text and "10" in text:
        return 12.0
    nums = re.findall(r"\d+[\.,]?\d*", text)
    if nums:
        return float(nums[0].replace(",", "."))
    return None


def _map_q17_q18_risk(option: str) -> int:
    if not option:
        return 2
    if "5 000" in option or "8 000" in option:
        return 4
    if "2 000" in option or "5 000" in option:
        return 3
    if "1 000" in option or "3 000" in option:
        return 2
    return 1


def _compute_theoretical_profile(a: dict) -> int:
    score = 0.0
    max_score = 15.0

    score += 1 if a.get("q13_gain_risque") == "Vrai" else 0
    score += 1 if a.get("q14_etf") == "Faux" else 0
    score += 1 if a.get("q15_gestion_delegatee") == "Vrai" else 0

    q19 = a.get("q19_crise", "")
    if "réinvestis" in q19.lower() or "reinvestis" in q19.lower():
        score += 4
    elif "patiente" in q19.lower():
        score += 3
    elif "vends une partie" in q19.lower():
        score += 2
    elif "vends tout" in q19.lower():
        score += 1
    else:
        score += 1.5

    score += _map_q17_q18_risk(a.get("q17_ratio_5_ans", ""))
    score += _map_q17_q18_risk(a.get("q18_ratio_10_ans", ""))

    profile = round(1 + 9 * (score / max_score))
    return max(1, min(10, profile))


def _apply_profile_caps(profile: int, a: dict) -> tuple[int, list[str]]:
    caps = [10]
    alerts: list[str] = []

    q10 = (a.get("q10_besoin_total_2_ans", "") or "").lower()
    if "probablement" in q10:
        caps.append(2)
        alerts.append("Besoins de liquidité court terme détectés : profil plafonné à 2.")

    years = _extract_years(a.get("q4_horizon", ""))
    if years is not None and years < 3:
        caps.append(3)
        alerts.append("Horizon d'investissement inférieur à 3 ans : profil plafonné à 3.")

    q2 = _parse_amount(a.get("q2_montant_initial", ""))
    q9 = _parse_amount(a.get("q9_patrimoine_financier", ""))
    if q2 > 0 and q9 > 0 and q2 > q9:
        caps.append(4)
        alerts.append("Incohérence détectée : montant à placer supérieur au patrimoine financier (profil plafonné à 4).")

    return min(profile, min(caps)), alerts


def _profile_to_sri(profile: int) -> int:
    if profile <= 3:
        return 1 if profile <= 2 else 2
    if profile <= 6:
        return 3 if profile <= 5 else 4
    return 5 + round((profile - 7) * 2 / 3)


def _gauge_horizon(a: dict) -> int:
    years = _extract_years(a.get("q4_horizon", ""))
    if years is None:
        return 40
    if years < 3:
        return 20
    if years <= 5:
        return 40
    if years <= 8:
        return 60
    if years <= 12:
        return 80
    return 100


def _gauge_withdrawal(a: dict) -> int:
    mapping = {
        "certainement pas": 10,
        "probablement pas": 35,
        "probablement": 70,
        "très probablement": 95,
        "tres probablement": 95,
    }

    q10 = mapping.get((a.get("q10_besoin_total_2_ans", "") or "").lower(), 35)
    q11 = mapping.get((a.get("q11_besoin_moitie_10_ans", "") or "").lower(), 35)
    return max(q10, q11)


def _gauge_risk_attitude(a: dict) -> int:
    q17 = a.get("q17_ratio_5_ans", "")
    q18 = a.get("q18_ratio_10_ans", "")
    q19 = (a.get("q19_crise", "") or "").lower()

    if "5 000" in q17:
        s17 = 90
    elif "2 000" in q17:
        s17 = 65
    elif "1 000" in q17:
        s17 = 45
    else:
        s17 = 10

    if "8 000" in q18:
        s18 = 90
    elif "5 000" in q18:
        s18 = 65
    elif "3 000" in q18:
        s18 = 45
    else:
        s18 = 10

    if "réinvestis" in q19 or "reinvestis" in q19:
        s19 = 90
    elif "patiente" in q19:
        s19 = 50
    elif "vends une partie" in q19:
        s19 = 30
    elif "vends tout" in q19:
        s19 = 10
    else:
        s19 = 20

    return round((s17 + s18 + s19) / 3)


def _gauge_financial_capacity(a: dict) -> int:
    total = _parse_amount(a.get("q8_patrimoine_immo", "")) + _parse_amount(a.get("q9_patrimoine_financier", ""))
    if total < 20000:
        return 20
    if total < 80000:
        return 40
    if total < 250000:
        return 70
    return 95


def _render_gauge(label: str, value: int, left: str, right: str):
    st.markdown(
        f"""
        <div class="poc2-gauge">
            <div class="poc2-gauge-label">{label}</div>
            <div class="poc2-gauge-track"><div class="poc2-gauge-fill" style="width:{value}%;"></div></div>
            <div class="poc2-gauge-ends"><span>{left}</span><span>{right}</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_geo_donut():
    rows = []
    for item in REGION_DISTRIBUTION:
        rows.append(
            f'<div class="poc2-geo-row">'
            f'<div class="poc2-geo-label">'
            f'<span class="poc2-donut-dot" style="background:{item["color"]};"></span>'
            f'<span>{item["label"]}</span>'
            f'</div>'
            f'<div class="poc2-geo-track"><div class="poc2-geo-fill" style="width:{item["value"]}%;background:{item["color"]};"></div></div>'
            f'<div class="poc2-geo-value">{str(item["value"]).replace(".", ",")}%</div>'
            f'</div>'
        )

    st.markdown(
        (
            f'<div class="poc2-section-card">'
            f'<div class="poc2-section-title">Diversification géographique (hors Fonds Euro)</div>'
            f'<div class="poc2-geo-bars">'
            f'{"".join(rows)}'
            f'</div>'
            f'</div>'
        ),
        unsafe_allow_html=True,
    )


def _asset_distribution_from_sri(sri: int) -> list[dict]:
    sri_map = {
        1: (70.0, 25.0, 5.0),
        2: (60.0, 30.0, 10.0),
        3: (50.0, 32.0, 18.0),
        4: (40.0, 31.5, 28.5),
        5: (30.0, 35.0, 35.0),
        6: (20.0, 35.0, 45.0),
        7: (10.0, 30.0, 60.0),
    }

    fonds_euros, obligations, actions = sri_map.get(sri, sri_map[4])

    return [
        {
            "label": "Fonds euros",
            "sub": "Actifs garantis",
            "value": fonds_euros,
            "color": ASSET_COLORS["fonds_euros"],
        },
        {
            "label": "Obligations",
            "sub": "Actifs a risques moderes",
            "value": obligations,
            "color": ASSET_COLORS["obligations"],
        },
        {
            "label": "Actions",
            "sub": "Actifs risques",
            "value": actions,
            "color": ASSET_COLORS["actions"],
        },
    ]


def _render_asset_donut(sri: int):
    distribution = _asset_distribution_from_sri(sri)
    radius = 52
    ring_width = 24
    circumference = 2 * 3.141592653589793 * radius
    total = sum(item["value"] for item in distribution) or 1
    offset = 0.0
    segments = []

    for item in distribution:
        share = item["value"] / total
        dash = share * circumference
        segments.append(
            f'<circle cx="70" cy="70" r="{radius}" fill="none" stroke="{item["color"]}" '
            f'stroke-width="{ring_width}" stroke-linecap="round" '
            f'stroke-dasharray="{dash:.2f} {circumference - dash:.2f}" stroke-dashoffset="{-offset:.2f}" />'
        )
        offset += dash

    legend = []
    for item in distribution:
        legend.append(
            f'<div class="poc2-donut-item">'
            f'<div class="poc2-donut-item-left">'
            f'<span class="poc2-donut-dot" style="background:{item["color"]};"></span>'
            f'<div class="poc2-donut-meta">'
            f'<span>{item["label"]}</span>'
            f'<span class="poc2-donut-sub">({item["sub"]})</span>'
            f'</div>'
            f'</div>'
            f'<div class="poc2-donut-value">{str(item["value"]).replace(".", ",")}%</div>'
            f'</div>'
        )

    st.markdown(
        (
            f'<div class="poc2-section-card">'
            f'<div class="poc2-section-title">Répartition par type d\'actifs</div>'
            f'<div class="poc2-donut-layout">'
            f'<div class="poc2-donut-wrap">'
            f'<svg width="170" height="170" viewBox="0 0 140 140" aria-label="Répartition par type d\'actifs">'
            f'<g transform="rotate(-90 70 70)">'
            f'<circle cx="70" cy="70" r="{radius}" fill="none" stroke="#E7EDF8" stroke-width="{ring_width}" />'
            f'{"".join(segments)}'
            f'</g>'
            f'<circle cx="70" cy="70" r="28" fill="#FFFFFF" />'
            f'<text x="70" y="64" text-anchor="middle" font-size="11" font-weight="700" fill="#7A8BAF">Allocation</text>'
            f'<text x="70" y="80" text-anchor="middle" font-size="18" font-weight="800" fill="#002261">SRI {sri}</text>'
            f'</svg>'
            f'</div>'
            f'<div class="poc2-donut-legend">{"".join(legend)}</div>'
            f'</div>'
            f'</div>'
        ),
        unsafe_allow_html=True,
    )


def _projection_rates_from_sri(sri: int) -> tuple[float, float, float]:
    expected = 0.018 + (sri - 1) * 0.007
    favorable = expected + 0.02
    unfavorable = max(-0.012, expected - (0.02 + (sri - 1) * 0.004))
    return favorable, expected, unfavorable


def _build_projection_series(a: dict, sri: int) -> dict:
    initial = _parse_amount(a.get("q2_montant_initial", ""))
    monthly = _parse_amount(a.get("q3_montant_mensuel", ""))

    if initial <= 0:
        initial = 10000.0
    if monthly < 0:
        monthly = 0.0

    years_raw = _extract_years(a.get("q4_horizon", ""))
    horizon_years = int(round(years_raw)) if years_raw is not None else 6
    horizon_years = max(3, min(12, horizon_years))

    favorable_r, expected_r, unfavorable_r = _projection_rates_from_sri(sri)
    yearly_contrib = monthly * 12
    start_year = date.today().year

    labels = [str(start_year + i) for i in range(horizon_years + 1)]
    favorable_vals = [initial]
    expected_vals = [initial]
    unfavorable_vals = [initial]
    cumulative_vals = [initial]

    fav = initial
    exp = initial
    unf = initial
    cum = initial

    for _ in range(horizon_years):
        fav = (fav + yearly_contrib) * (1 + favorable_r)
        exp = (exp + yearly_contrib) * (1 + expected_r)
        unf = max(0.0, (unf + yearly_contrib) * (1 + unfavorable_r))
        cum = cum + yearly_contrib

        favorable_vals.append(fav)
        expected_vals.append(exp)
        unfavorable_vals.append(unf)
        cumulative_vals.append(cum)

    return {
        "labels": labels,
        "favorable": favorable_vals,
        "expected": expected_vals,
        "unfavorable": unfavorable_vals,
        "cumulative": cumulative_vals,
    }


def _fmt_k_eur(value: float) -> str:
    return f"{value / 1000:.1f}".replace(".", ",") + " kEUR"


def _render_projection_chart(a: dict, sri: int):
    data = _build_projection_series(a, sri)
    labels = data["labels"]
    favorable = data["favorable"]
    expected = data["expected"]
    unfavorable = data["unfavorable"]
    cumulative = data["cumulative"]

    years = [int(y) for y in labels]
    def _rng_text(series: list[float], idx: int) -> str:
        if idx == 0:
            return _fmt_k_eur(series[idx])
        lo = min(series[idx - 1], series[idx])
        hi = max(series[idx - 1], series[idx])
        return f"{_fmt_k_eur(lo)} - {_fmt_k_eur(hi)}"

    def _make_band(series: list[float], scenario: str) -> pd.DataFrame:
        lows = [series[0]]
        highs = [series[0]]
        for i in range(1, len(series)):
            lows.append(min(series[i - 1], series[i]))
            highs.append(max(series[i - 1], series[i]))
        return pd.DataFrame({"year": years, "scenario": scenario, "low": lows, "high": highs})

    bands_df = pd.concat(
        [
            _make_band(unfavorable, "Defavorable"),
            _make_band(expected, "Attendu"),
            _make_band(favorable, "Favorable"),
        ],
        ignore_index=True,
    )

    scen_df = pd.DataFrame(
        {
            "year": years * 3,
            "scenario": ["Favorable"] * len(years)
            + ["Attendu"] * len(years)
            + ["Defavorable"] * len(years),
            "value": favorable + expected + unfavorable,
        }
    )

    cum_df = pd.DataFrame({"year": years, "value": cumulative})

    y_max = max(favorable + expected + unfavorable + cumulative) * 1.08
    y_axis = alt.Axis(title=None, format="~s", orient="right")
    x_axis = alt.Axis(title=None, labelAngle=0)

    areas = alt.Chart(bands_df).mark_area(opacity=0.24).encode(
        x=alt.X("year:O", axis=x_axis),
        y=alt.Y("low:Q", axis=y_axis),
        y2="high:Q",
        color=alt.Color(
            "scenario:N",
            scale=alt.Scale(
                domain=["Favorable", "Attendu", "Defavorable"],
                range=["#03AFA7", "#102065", "#D9016D"],
            ),
            legend=None,
        ),
    )

    lines = alt.Chart(scen_df).mark_line(strokeWidth=2).encode(
        x=alt.X("year:O", axis=x_axis),
        y=alt.Y("value:Q", axis=y_axis),
        color=alt.Color(
            "scenario:N",
            scale=alt.Scale(
                domain=["Favorable", "Attendu", "Defavorable"],
                range=["#03AFA7", "#102065", "#D9016D"],
            ),
            legend=None,
        ),
    )

    cumulative_line = alt.Chart(cum_df).mark_line(
        color="#111111", strokeWidth=2, strokeDash=[6, 6]
    ).encode(
        x=alt.X("year:O", axis=x_axis),
        y=alt.Y("value:Q", axis=y_axis),
    )

    summary_df = pd.DataFrame(
        {
            "year": years,
            "low": [0.0 for _ in years],
            "high": [y_max for _ in years],
            "tooltip_favorable": [_rng_text(favorable, i) for i in range(len(years))],
            "tooltip_attendu": [_rng_text(expected, i) for i in range(len(years))],
            "tooltip_defavorable": [_rng_text(unfavorable, i) for i in range(len(years))],
            "tooltip_cumules": [_fmt_k_eur(cumulative[i]) for i in range(len(years))],
            "anchor": expected,
        }
    )

    nearest = alt.selection_point(nearest=True, on="pointerover", fields=["year"], empty=False)
    selectors = alt.Chart(summary_df).mark_rect(opacity=0).encode(
        x=alt.X("year:O", axis=x_axis),
        y=alt.Y("low:Q", axis=y_axis),
        y2="high:Q",
        tooltip=[
            alt.Tooltip("year:O", title="Annee"),
            alt.Tooltip("tooltip_favorable:N", title="Favorable"),
            alt.Tooltip("tooltip_attendu:N", title="Attendu"),
            alt.Tooltip("tooltip_defavorable:N", title="Defavorable"),
            alt.Tooltip("tooltip_cumules:N", title="Cumules"),
        ],
    ).add_params(nearest)

    hover_rule = alt.Chart(summary_df).mark_rule(color="#8FA3C7", strokeWidth=2).encode(
        x=alt.X("year:O", axis=x_axis)
    ).transform_filter(nearest)

    chart = (
        (areas + lines + cumulative_line + selectors + hover_rule)
        .properties(height=300)
        .configure_view(stroke=None)
        .configure_axis(gridColor="#EEF2FA", domainColor="#8FA3C7", tickColor="#9FB0CF")
    )

    with st.container(border=True):
        st.markdown('<div class="poc2-section-title">Simulation de votre projet</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="poc2-sim-sub">Projection estimee selon votre horizon, vos versements et votre profil SRI. Survolez le graphe pour voir les details par annee.</div>',
            unsafe_allow_html=True,
        )
        st.markdown('<div class="poc2-sim-chart-wrap">', unsafe_allow_html=True)
        st.altair_chart(chart, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="poc2-sim-legend">'
            '<div class="poc2-sim-leg-row"><div class="poc2-sim-leg-left"><span class="poc2-donut-dot" style="background:#03AFA7;"></span><span>Favorable</span></div></div>'
            '<div class="poc2-sim-leg-row"><div class="poc2-sim-leg-left"><span class="poc2-donut-dot" style="background:#102065;"></span><span>Attendu</span></div></div>'
            '<div class="poc2-sim-leg-row"><div class="poc2-sim-leg-left"><span class="poc2-donut-dot" style="background:#D9016D;"></span><span>Defavorable</span></div></div>'
            '<div class="poc2-sim-leg-row"><div class="poc2-sim-leg-left"><span style="display:inline-block;width:14px;height:0;border-top:2px dashed #111111;"></span><span>Vos versements</span></div></div>'
            '</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="poc2-sim-note">Les supports d\'investissement presentent un risque de perte en capital. Les performances passees ne prejudgent pas des performances futures.</div>',
            unsafe_allow_html=True,
        )


def _render_recommendation_dashboard(a: dict):
    initial_amount = a.get("q2_montant_initial", "-")
    monthly_amount = a.get("q3_montant_mensuel", "-")
    horizon = a.get("q4_horizon", "-")

    profile_theoretical = _compute_theoretical_profile(a)
    profile_final, alerts = _apply_profile_caps(profile_theoretical, a)
    sri = _profile_to_sri(profile_final)

    st.session_state.poc2_answers["recommandation"] = f"Profil {profile_final}/10"

    st.markdown(
        f"""
        <div class="poc2-profile-card">
            <div class="poc2-profile-row"><strong>Votre projet</strong><span>Modifier</span></div>
            <div class="poc2-profile-row"><span>Versement initial</span><strong>{initial_amount}</strong></div>
            <div class="poc2-profile-row"><span>Versement mensuel</span><strong>{monthly_amount}</strong></div>
            <div class="poc2-profile-row"><span>Horizon de placement</span><strong>{horizon}</strong></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="poc2-profile-title">Profil {profile_final} (SRI {sri}/7)</div>
        <div class="poc2-profile-text">
            Le profil est déterminé par votre score de risque, puis plafonné par les règles de sécurité client (liquidité, horizon et cohérence patrimoniale).
        </div>
        """,
        unsafe_allow_html=True,
    )

    _render_gauge("Horizon de placement", _gauge_horizon(a), "Court", "Long")
    _render_gauge("Probabilité de retrait", _gauge_withdrawal(a), "Faible", "Forte")
    _render_gauge("Attitude face au risque", _gauge_risk_attitude(a), "Prudent", "Dynamique")
    _render_gauge("Capacité financière", _gauge_financial_capacity(a), "Réduite", "Élevée")

    if alerts:
        for alert in alerts:
            st.markdown(f"<div class='poc2-alert'>{alert}</div>", unsafe_allow_html=True)

    _render_asset_donut(sri)
    _render_geo_donut()
    _render_projection_chart(a, sri)


def _render_project_question(robot_b64: str | None):
    q_idx = st.session_state.poc2_project_idx
    q = PROJECT_QUESTIONS[q_idx]

    st.markdown(f"<div class='poc2-question'>{q['question']}</div>", unsafe_allow_html=True)

    if q.get("explain"):
        st.markdown(f"<div class='poc2-explain'>{q['explain']}</div>", unsafe_allow_html=True)

    if q.get("input_type") == "date":
        selected_date = st.date_input(
            "Date de naissance",
            key=f"{q['id']}_date",
            min_value=date(1900, 1, 1),
            max_value=date.today(),
        )
        val_col, _ = st.columns([1, 3])
        with val_col:
            if st.button("Valider", key=f"{q['id']}_validate", use_container_width=True, type="secondary"):
                _save_project_answer(q["id"], selected_date.strftime("%d/%m/%Y"))
                _advance_project_question()
                st.rerun()
        return

    cols = st.columns(2, gap="medium")
    for i, option in enumerate(q.get("options", [])):
        with cols[i % 2]:
            if st.button(option, key=f"{q['id']}_opt_{i}", use_container_width=True, type="secondary"):
                _save_project_answer(q["id"], option)
                if q.get("feedback"):
                    st.session_state.poc2_feedback = q["feedback"].get(option, "")
                    st.session_state.poc2_feedback_qid = q["id"]
                elif q["id"] == "q7_durable" and option == "Oui":
                    # On reste sur la question pour afficher la sous-question ESG.
                    pass
                else:
                    _advance_project_question()
                st.rerun()

    if q.get("free_input"):
        st.markdown(f"<div class='poc2-free-label'>{q['free_input_label']}</div>", unsafe_allow_html=True)
        input_col, action_col = st.columns([4, 1])
        with input_col:
            free_amount = st.text_input(
                "Saisie libre",
                key=f"{q['id']}_free",
                placeholder=q.get("free_input_placeholder", "Ex : 75 000 €"),
                label_visibility="collapsed",
            )
        with action_col:
            if st.button("Valider", key=f"{q['id']}_free_validate", use_container_width=True, type="secondary"):
                if free_amount.strip():
                    _save_project_answer(q["id"], free_amount.strip())
                    _advance_project_question()
                    st.rerun()

    if q["id"] == "q7_durable" and st.session_state.poc2_project_answers.get("q7_durable") == "Oui":
        st.markdown("<div class='poc2-free-label'>Sous-question :</div>", unsafe_allow_html=True)
        sub_choice = st.selectbox(
            q["sub_question"],
            options=["Sélectionner"] + q["sub_options"],
            key="q7_sub_choice",
            label_visibility="visible",
        )
        if sub_choice != "Sélectionner":
            _save_project_answer("q7_sub_choice", sub_choice)

        if q.get("sub_info"):
            robot_logo = (
                f'<img src="data:image/png;base64,{robot_b64}" alt="Robot CNP" />'
                if robot_b64
                else ""
            )
            st.markdown(
                f"""
                <div class="poc2-robot-info">
                    {robot_logo}
                    <div class="poc2-robot-info-text">{q['sub_info']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        return

    if q.get("robot_info"):
        robot_logo = (
            f'<img src="data:image/png;base64,{robot_b64}" alt="Robot CNP" />'
            if robot_b64
            else ""
        )
        st.markdown(
            f"""
            <div class="poc2-robot-info">
                {robot_logo}
                <div class="poc2-robot-info-text">{q['robot_info']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if st.session_state.poc2_feedback_qid == q["id"] and st.session_state.poc2_feedback:
        robot_logo = (
            f'<img src="data:image/png;base64,{robot_b64}" alt="Robot CNP" />'
            if robot_b64
            else ""
        )
        st.markdown(
            f"""
            <div class="poc2-robot-info">
                {robot_logo}
                <div class="poc2-robot-info-text">{st.session_state.poc2_feedback}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

def show_poc2():
    _init_state()
    _render_styles()
    robot_b64 = _img_base64("images/robot-CNP.png")

    step_idx = st.session_state.poc2_step_idx
    current = STEPS[step_idx]
    answers = st.session_state.poc2_answers

    if current["id"] == "projet":
        q_idx = st.session_state.poc2_project_idx
        project_total = len(PROJECT_QUESTIONS)
        progress = (q_idx + 1) / project_total
        head_right = f"Question {q_idx + 1} sur {project_total}"
    else:
        progress = (step_idx + 1) / len(STEPS)
        head_right = f"Question {step_idx + 1} sur {len(STEPS)}"

    with st.container(border=True):
        _render_stepper(step_idx)

        if current["id"] == "recommandation":
            st.markdown(
                """
                <div class='poc2-rec-head'>Recommendation CNP</div>
                <div class='poc2-rec-text'>
                    Suite a l'analyse de vos informations, nos experts vous proposent un investissement adapte a vos besoins. D'ailleurs, plus de 87% de nos utilisateurs ont suivi la recommandation de CNP.
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div class='poc2-card-head'>
                    <div class='poc2-head-left'>Parlons de votre projet</div>
                    <div class='poc2-head-right'>{head_right}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.progress(progress)

        if current["id"] == "projet":
            _render_project_question(robot_b64)
        elif current["id"] == "recommandation":
            _render_recommendation_dashboard(st.session_state.poc2_project_answers)
        else:
            st.markdown(
                f"<div class='poc2-question'>{current['question']}</div>",
                unsafe_allow_html=True,
            )

            cols = st.columns(2, gap="medium")
            for i, option in enumerate(current["options"]):
                with cols[i % 2]:
                    if st.button(
                        option,
                        key=f"poc2_opt_{step_idx}_{i}",
                        use_container_width=True,
                        type="secondary",
                    ):
                        st.session_state.poc2_answers[current["id"]] = option
                        if step_idx < len(STEPS) - 1:
                            st.session_state.poc2_step_idx = step_idx + 1
                            st.session_state.poc2_done = False
                        else:
                            st.session_state.poc2_done = True
                        st.rerun()

    st.markdown("<div class='poc2-nav-row'></div>", unsafe_allow_html=True)
    prev_col, spacer_col, next_col = st.columns([1, 4, 1])

    with prev_col:
        if current["id"] == "projet":
            prev_disabled = st.session_state.poc2_project_idx == 0
            prev_clicked = st.button(
                "Précédent",
                key="poc2_prev_project",
                use_container_width=True,
                disabled=prev_disabled,
                type="primary",
            )
            if prev_clicked:
                st.session_state.poc2_project_idx -= 1
                st.session_state.poc2_done = False
                st.rerun()
        else:
            prev_clicked = st.button(
                "Précédent",
                key="poc2_prev",
                use_container_width=True,
                disabled=step_idx == 0,
                type="primary",
            )
            if prev_clicked:
                st.session_state.poc2_step_idx -= 1
                st.session_state.poc2_done = False
                st.rerun()

    with next_col:
        if current["id"] == "projet":
            can_go_next = st.session_state.poc2_project_idx < len(PROJECT_QUESTIONS) - 1
            next_clicked = st.button(
                "Suivant",
                key="poc2_next_project",
                use_container_width=True,
                disabled=not can_go_next,
                type="primary",
            )
            if next_clicked:
                qid = PROJECT_QUESTIONS[st.session_state.poc2_project_idx]["id"]
                if st.session_state.poc2_feedback_qid == qid and st.session_state.poc2_feedback:
                    st.session_state.poc2_feedback = ""
                    st.session_state.poc2_feedback_qid = ""
                st.session_state.poc2_project_idx += 1
                st.rerun()
        else:
            has_answer = current["id"] in st.session_state.poc2_answers
            if step_idx < len(STEPS) - 1:
                next_clicked = st.button(
                    "Suivant",
                    key="poc2_next",
                    use_container_width=True,
                    disabled=not has_answer,
                    type="primary",
                )
                if next_clicked:
                    st.session_state.poc2_step_idx += 1
                    st.session_state.poc2_done = False
                    st.rerun()
            else:
                finish_clicked = st.button(
                    "Terminer",
                    key="poc2_finish",
                    use_container_width=True,
                    disabled=not has_answer,
                    type="primary",
                )
                if finish_clicked:
                    st.session_state.poc2_step_idx = 0
                    st.session_state.poc2_project_idx = 0
                    st.session_state.poc2_done = False
                    st.success("Parfait. Le parcours test est complété.")

    if st.session_state.poc2_done:
        st.success("Parfait. Le parcours test est complété.")

    if st.session_state.poc2_project_answers:
        recap_lines = []
        for q in PROJECT_QUESTIONS:
            value = st.session_state.poc2_project_answers.get(q["id"])
            if value:
                recap_lines.append(f"<li><b>{q['question']}</b> : {value}</li>")
        sub_value = st.session_state.poc2_project_answers.get("q7_sub_choice")
        if sub_value:
            recap_lines.append(f"<li><b>Sous-question ESG</b> : {sub_value}</li>")

        if recap_lines:
            st.markdown(
                "<div class='poc2-recap'>Réponses projet en cours :</div><ul>"
                + "".join(recap_lines)
                + "</ul>",
                unsafe_allow_html=True,
            )
