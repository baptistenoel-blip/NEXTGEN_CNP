import base64
import html
import streamlit as st

FUNDS = [
    {
        "name": "CNP Actions Climat ESG",
        "type": "Actions internationales",
        "risk": "4/7",
        "perf": "+8.5%",
        "key": "poc3_fund_1",
        "prompt": "Analyse le fonds CNP Actions Climat ESG et dis-moi ses points forts et risques.",
    },
    {
        "name": "CNP Immobilier Rendement",
        "type": "OPCI / Pierre-papier",
        "risk": "2/7",
        "perf": "+3.1%",
        "key": "poc3_fund_2",
        "prompt": "Le fonds CNP Immobilier Rendement est-il adapté à un profil prudent ?",
    },
    {
        "name": "CNP Obligations Europe",
        "type": "Obligataire diversification",
        "risk": "3/7",
        "perf": "+4.2%",
        "key": "poc3_fund_3",
        "prompt": "Compare CNP Obligations Europe avec mon portefeuille actuel.",
    },
]

MARKET_ALERTS = [
    {
        "title": "Le marche automobile europeen ralentit fortement",
        "impact": "Impact potentiel sur les valeurs industrielles et cycliques presentes dans CNP Actions Climat ESG.",
        "fund": "CNP Actions Climat ESG",
        "tone": "negative",
        "url": "https://www.lesechos.fr/industrie-services/automobile",
    },
    {
        "title": "Nouveau plan d'Etat pour accelerer l'eolien",
        "impact": "Signal favorable pour la transition energetique et certains actifs ESG du portefeuille.",
        "fund": "CNP Actions Climat ESG",
        "tone": "positive",
        "url": "https://www.ecologie.gouv.fr/politiques-publiques/energies-renouvelables",
    },
    {
        "title": "Les taux long terme se detendent en zone euro",
        "impact": "Contexte potentiellement constructif pour CNP Obligations Europe et certains arbitrages defensifs.",
        "fund": "CNP Obligations Europe",
        "tone": "neutral",
        "url": "https://www.ecb.europa.eu/press/pressconf/html/index.en.html",
    },
]


def _img_base64(path: str):
    try:
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")
    except Exception:
        return None


def _init_state():
    if "poc3_messages" not in st.session_state:
        st.session_state.poc3_messages = [
            {
                "role": "assistant",
                "content": "Bonjour ! Je suis votre assistant CNP. Je peux analyser vos placements, évaluer les risques et vous guider dans vos arbitrages.",
            }
        ]


def _push_ai_exchange(user_prompt: str):
    st.session_state.poc3_messages.append({"role": "user", "content": user_prompt})
    st.session_state.poc3_messages.append(
        {
            "role": "assistant",
            "content": "Voici mon analyse : ce fonds offre une bonne diversification. Pour optimiser votre profil, un suivi mensuel et un rééquilibrage progressif sont conseillés.",
        }
    )


def _render_styles():
    st.markdown(
        """
        <style>
        .stApp {
            background: #F5F8FF !important;
        }

        .main .block-container {
            padding-top: 1rem;
            padding-bottom: 2rem;
        }

        /* En-tête de tableau de bord */
        .poc3-dash-header {
            margin-bottom: 20px;
        }

        .poc3-dash-title {
            color: #002261;
            font-size: 1.8rem;
            font-weight: 800;
            margin: 0;
        }

        .poc3-dash-sub {
            color: #5D6E97;
            font-size: 0.95rem;
            margin-top: 4px;
        }

        /* Cartes de métriques */
        .poc3-metric-card {
            background: #FFFFFF !important;
            border: 1px solid #D8DEEB;
            border-radius: 18px;
            padding: 16px 18px;
            margin-bottom: 12px;
        }

        .poc3-metric-label {
            color: #5D6E97;
            font-size: 0.8rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }

        .poc3-metric-value {
            color: #002261;
            font-size: 1.6rem;
            font-weight: 800;
            margin-top: 4px;
        }

        .poc3-metric-delta {
            color: #02ADA5;
            font-weight: 700;
            margin-top: 4px;
            font-size: 0.88rem;
        }

        .poc3-section-title {
            color: #002261;
            font-size: 1.15rem;
            font-weight: 800;
            margin: 8px 0 12px 2px;
        }

        .poc3-alert-strip {
            background: #FFFFFF;
            border: 1px solid #D8DEEB;
            border-radius: 14px;
            padding: 10px 12px;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
        }

        .poc3-alert-main {
            display: flex;
            align-items: center;
            gap: 10px;
            min-width: 0;
        }

        .poc3-alert-dot {
            width: 9px;
            height: 9px;
            border-radius: 999px;
            flex: 0 0 auto;
        }

        .poc3-alert-dot.negative {
            background: #D64545;
        }

        .poc3-alert-dot.positive {
            background: #18A56B;
        }

        .poc3-alert-dot.neutral {
            background: #3F74C8;
        }

        .poc3-alert-pill {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 999px;
            font-size: 0.67rem;
            font-weight: 800;
            letter-spacing: 0.03em;
            text-transform: uppercase;
            margin-right: 6px;
        }

        .poc3-alert-pill.negative {
            background: #FDECEC;
            color: #B42828;
            border: 1px solid #F5C7C7;
        }

        .poc3-alert-pill.positive {
            background: #EAF8F1;
            color: #157A43;
            border: 1px solid #BFEAD2;
        }

        .poc3-alert-pill.neutral {
            background: #EEF4FF;
            color: #1F4E9A;
            border: 1px solid #CADAF8;
        }

        .poc3-alert-title {
            color: #002261;
            font-size: 0.9rem;
            font-weight: 700;
            line-height: 1.3;
            margin: 0;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .poc3-alert-text {
            color: #41567F;
            font-size: 0.82rem;
            line-height: 1.35;
            margin: 2px 0 0 0;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .poc3-alert-fund {
            color: #02ADA5;
            font-size: 0.75rem;
            font-weight: 700;
            margin-top: 2px;
        }

        .poc3-alert-link {
            color: #002261;
            border: 1px solid #C8D4EE;
            border-radius: 999px;
            font-size: 0.78rem;
            font-weight: 700;
            text-decoration: none;
            padding: 6px 10px;
            white-space: nowrap;
            flex: 0 0 auto;
            background: #FFFFFF;
        }

        .poc3-alert-link:hover {
            border-color: #02ADA5;
            color: #027A74;
            background: #EAF8F7;
        }

        /* Force le fond BLANC strict sur tous les blocs/conteneurs */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background: #FFFFFF !important;
            background-color: #FFFFFF !important;
            border: 1px solid #D8DEEB !important;
            border-radius: 18px !important;
            padding: 14px 16px 16px 16px !important;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] > div,
        div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stVerticalBlock"],
        div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stHorizontalBlock"],
        div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="column"],
        div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stMarkdownContainer"] {
            background: #FFFFFF !important;
            background-color: #FFFFFF !important;
            opacity: 1 !important;
        }

        /* Style des boutons */
        div[data-testid="stButton"] > button[kind="secondary"] {
            background: #FFFFFF !important;
            color: #002261 !important;
            border: 1px solid #C8D4EE !important;
            border-radius: 999px !important;
            font-weight: 700 !important;
            min-height: 42px !important;
        }

        div[data-testid="stButton"] > button[kind="secondary"]:hover {
            background: #EAF8F7 !important;
            color: #027A74 !important;
            border-color: #02ADA5 !important;
        }

        /* Header du Chatbot avec Logo grand et sans fond blanc */
        .poc3-chat-head {
            background: #002261;
            border-radius: 24px;
            color: #FFFFFF;
            padding: 20px 22px;
            display: flex;
            align-items: center;
            gap: 18px;
            margin-bottom: 14px;
        }

        .poc3-chat-head img {
            width: 118px;
            height: 118px;
            object-fit: contain;
            background: transparent !important;
            padding: 0 !important;
            border-radius: 0 !important;
        }

        .poc3-chat-head-title {
            font-weight: 800;
            font-size: 1.15rem;
            margin: 0;
            color: #FFFFFF !important;
        }

        .poc3-chat-head-sub {
            margin: 4px 0 0 0;
            color: #C9DAFF;
            font-size: 0.85rem;
        }

        .poc3-chat-box {
            background: #FFFFFF;
            border: 1px solid #D8DEEB;
            border-radius: 22px;
            padding: 14px;
            height: 400px;
            overflow-y: auto;
        }

        .poc3-bubble-row {
            display: flex;
            margin-bottom: 12px;
            align-items: flex-end;
            gap: 8px;
        }

        .poc3-bubble-row.user {
            justify-content: flex-end;
        }

        .poc3-bubble-avatar {
            width: 38px;
            height: 38px;
            object-fit: contain;
            border-radius: 12px;
            background: transparent;
            flex: 0 0 auto;
        }

        .poc3-bubble {
            max-width: 84%;
            padding: 11px 14px;
            border-radius: 18px;
            line-height: 1.45;
            font-size: 0.95rem;
            font-weight: 500;
        }

        .poc3-bubble.assistant {
            background: #EFF4FF;
            border: 1px solid #D0DDFC;
            color: #002261;
            border-radius: 18px 18px 18px 6px;
        }

        .poc3-bubble.user {
            background: #002261;
            border: 1px solid #002261;
            color: #FFFFFF;
            border-radius: 18px 18px 6px 18px;
        }

        .poc3-white-card {
            background: #FFFFFF !important;
            border: 1px solid #D8DEEB !important;
            border-radius: 18px !important;
            padding: 14px 16px 16px 16px !important;
            margin-bottom: 12px;
        }

        .poc3-white-card h1,
        .poc3-white-card h2,
        .poc3-white-card h3,
        .poc3-white-card p,
        .poc3-white-card span,
        .poc3-white-card div {
            background: transparent !important;
        }

        /* Alerte */
        div[data-testid="stAlert"] {
            border-radius: 16px;
            border: 1px solid #CDEDEA;
            background: #E6F7F6 !important;
            color: #027A74 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _render_metric_card(label: str, value: str, delta: str):
    st.markdown(
        f"""
        <div class="poc3-metric-card">
            <div class="poc3-metric-label">{label}</div>
            <div class="poc3-metric-value">{value}</div>
            <div class="poc3-metric-delta">{delta}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_market_alerts():
    st.markdown(
        '<div class="poc3-section-title">Alerte Marché</div>',
        unsafe_allow_html=True,
    )

    for alert in MARKET_ALERTS:
        st.markdown(
            f"""
            <div class="poc3-alert-strip">
                <div class="poc3-alert-main">
                    <span class="poc3-alert-dot {alert['tone']}"></span>
                    <div>
                        <div>
                            <span class="poc3-alert-pill {alert['tone']}">{alert['tone']}</span>
                            <span class="poc3-alert-title">{alert['title']}</span>
                        </div>
                        <p class="poc3-alert-text">{alert['impact']}</p>
                        <div class="poc3-alert-fund">{alert['fund']}</div>
                    </div>
                </div>
                <a class="poc3-alert-link" href="{alert['url']}" target="_blank" rel="noopener">Article</a>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _render_chat_bubbles(robot_b64: str | None):
    rows = []
    robot_img = (
        f'<img class="poc3-bubble-avatar" src="data:image/png;base64,{robot_b64}" alt="Robot CNP" />'
        if robot_b64
        else ""
    )
    for msg in st.session_state.poc3_messages:
        safe_text = html.escape(msg["content"])
        if msg["role"] == "assistant":
            rows.append(
                f'<div class="poc3-bubble-row assistant">{robot_img}<div class="poc3-bubble assistant">{safe_text}</div></div>'
            )
        else:
            rows.append(
                f'<div class="poc3-bubble-row user"><div class="poc3-bubble user">{safe_text}</div></div>'
            )

    st.markdown(
        '<div class="poc3-chat-box">' + "".join(rows) + "</div>",
        unsafe_allow_html=True,
    )


def show_poc3():
    _init_state()
    _render_styles()

    robot_b64 = _img_base64("images/robot-CNP.png")
    robot_img = (
        f'<img src="data:image/png;base64,{robot_b64}" alt="Robot CNP" />'
        if robot_b64
        else ""
    )

    # Titre classique de page de compte
    st.markdown(
        """
        <div class="poc3-dash-header">
            <h1 class="poc3-dash-title">Espace Client - Portefeuille & Épargne</h1>
            <div class="poc3-dash-sub">Vue d'ensemble de vos fonds, performance et alertes d'arbitrage en temps réel.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    m1, m2, m3 = st.columns(3)
    with m1:
        _render_metric_card("Valorisation globale", "50 000 EUR", "+2.4% ce mois")
    with m2:
        _render_metric_card("Répartition UC", "40%", "+5 pts")
    with m3:
        _render_metric_card("Profil risque", "Équilibré 3/7", "Stable")

    _render_market_alerts()

    col_left, col_right = st.columns([6, 5], gap="large")

    with col_left:
        st.markdown(
            '<div class="poc3-section-title">Vos placements en watchlist</div>',
            unsafe_allow_html=True,
        )

        for fund in FUNDS:
            with st.container(border=True):
                st.markdown(f"**{fund['name']}**")
                st.caption(f"{fund['type']}")
                c1, c2, c3 = st.columns([1, 1, 1.2], vertical_alignment="center")
                c1.markdown(f"Risque: **{fund['risk']}**")
                c2.markdown(f"Perf 1 an: **{fund['perf']}**")
                if c3.button(
                    "Analyser ce fonds",
                    key=fund["key"],
                    type="secondary",
                    use_container_width=True,
                ):
                    _push_ai_exchange(fund["prompt"])
                    st.rerun()

    with col_right:
        st.markdown(
            '<div class="poc3-section-title">Conseiller IA</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
            <div class="poc3-chat-head">
                {robot_img}
                <div>
                    <p class="poc3-chat-head-title">Co-pilote CNP Patrimoine</p>
                    <p class="poc3-chat-head-sub">Analyse instantanée et recommandations sur vos UC</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.info("Alerte : vous pouvez optimiser votre poche de liquidités avec une UC obligataire ciblée à +4%.")

        _render_chat_bubbles(robot_b64)

        user_text = st.chat_input("Posez une question au conseiller CNP...")
        if user_text:
            _push_ai_exchange(user_text)
            st.rerun()