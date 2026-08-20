import base64
from datetime import date

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
