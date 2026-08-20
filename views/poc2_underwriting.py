import streamlit as st

STEPS = [
    {
        "id": "projet",
        "label": "Projet",
        "question": "Quel est votre projet d'investissement ?",
        "options": [
            "Faire fructifier mon épargne",
            "Épargner en cas de coup dur",
            "Préparer un achat important",
            "Prévoir ma retraite",
        ],
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


def _init_state():
    if "poc2_step_idx" not in st.session_state:
        st.session_state.poc2_step_idx = 0
    if "poc2_answers" not in st.session_state:
        st.session_state.poc2_answers = {}
    if "poc2_done" not in st.session_state:
        st.session_state.poc2_done = False


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
            font-size: 2rem;
            line-height: 1.2;
            margin: 24px 0 18px 0;
            font-weight: 700;
        }

        /* --- STYLES DES BOUTONS - CORRECTION FINALE DU FOND DU TEXTE --- */
        div[data-testid="stButton"] {
            background: transparent !important;
            background-color: transparent !important;
            margin-top: 0 !important;
            margin-bottom: 0 !important;
        }

        /* Neutralisation de TOUS les conteneurs internes de texte sous le bouton */
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

        /* Options secondaires (Boutons de réponse) */
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

        /* Navigation principale (Précédent / Suivant / Terminer) */
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

        /* Conteneur principal de la question */
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
        </style>
        """,
        unsafe_allow_html=True,
    )


def show_poc2():
    _init_state()
    _render_styles()

    step_idx = st.session_state.poc2_step_idx
    current = STEPS[step_idx]
    answers = st.session_state.poc2_answers
    progress = (step_idx + 1) / len(STEPS)

    with st.container(border=True):
        _render_stepper(step_idx)

        st.markdown(
            f"""
            <div class='poc2-card-head'>
                <div class='poc2-head-left'>Parlons de votre projet</div>
                <div class='poc2-head-right'>Question {step_idx + 1} sur {len(STEPS)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.progress(progress)
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
                st.session_state.poc2_done = False
                st.success("Parfait. Le parcours test est complété.")

    if st.session_state.poc2_done:
        st.success("Parfait. Le parcours test est complété.")

    if answers:
        recap_lines = []
        for step in STEPS:
            value = answers.get(step["id"])
            if value:
                recap_lines.append(f"<li><b>{step['label']}:</b> {value}</li>")
        if recap_lines:
            st.markdown(
                "<div class='poc2-recap'>Réponses en cours:</div><ul>"
                + "".join(recap_lines)
                + "</ul>",
                unsafe_allow_html=True,
            )