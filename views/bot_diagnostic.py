from __future__ import annotations

import base64
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


ACCOUNT_TOUCHED = "CNP Actions Climat ESG"
ACCOUNT_TOUCHED_VALUE = 13_635.0
ACCOUNT_TARGET = "CNP Obligations Europe"
ACCOUNT_TARGET_VALUE = 2_995.0
PORTFOLIO_TOTAL = 50_000.0


def _init_state() -> None:
    if "bot_diagnostic_decision" not in st.session_state:
        st.session_state.bot_diagnostic_decision = None


def _render_styles() -> None:
    st.markdown(
        """
        <style>
        .stApp {
            background:
                radial-gradient(900px 420px at -10% -20%, rgba(3, 43, 246, 0.08), transparent 65%),
                linear-gradient(180deg, #F4F7FC 0%, #EBF0F9 100%) !important;
        }

        .st-key-botdiag-hero,
        .st-key-botdiag-xai,
        .st-key-botdiag-reco {
            background: #FFFFFF !important;
            border: 1px solid #E1E8F5 !important;
            border-radius: 18px !important;
            box-shadow: 0 6px 18px rgba(12, 56, 170, 0.05) !important;
            padding: 16px !important;
        }

        .st-key-botdiag-hero {
            padding: 18px 18px 24px !important;
        }

        .botdiag-title {
            color: #032BF6;
            font-size: 2rem;
            font-weight: 850;
            margin: 0;
            line-height: 1.05;
        }

        .botdiag-sub {
            color: #566A98;
            font-size: 0.95rem;
            margin-top: 6px;
            margin-bottom: 16px;
        }

        .botdiag-step-kicker {
            color: #2D4FB4;
            font-size: 0.78rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin: 0 0 4px 0;
        }

        .botdiag-step-title {
            color: #0E2E87;
            font-size: 1.08rem;
            font-weight: 840;
            margin: 0 0 6px 0;
        }

        .botdiag-step-text {
            color: #536792;
            font-size: 0.92rem;
            line-height: 1.45;
            margin: 8px 0 0 0;
        }

        .botdiag-hero-top {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            flex-wrap: wrap;
        }

        .botdiag-hero-tag {
            background: #EAF0FF !important;
            border: 1px solid #CBD8FF;
            color: #274AA7;
            border-radius: 999px;
            padding: 4px 10px;
            font-size: 0.76rem;
            font-weight: 790;
        }

        .botdiag-hero-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 10px;
            margin-top: 12px;
        }

        .botdiag-hero-kpi {
            background: #F7FAFF !important;
            border: 1px solid #DCE7FD;
            border-radius: 12px;
            padding: 10px 12px;
        }

        .botdiag-hero-kpi-label {
            color: #6073A0;
            font-size: 0.74rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-weight: 780;
            margin: 0;
        }

        .botdiag-hero-kpi-value {
            color: #12317F;
            font-size: 1.05rem;
            font-weight: 840;
            margin: 5px 0 0 0;
        }

        .botdiag-hero-kpi-value.warning {
            color: #A11453;
        }

        .botdiag-xai-card {
            background: #FFFFFF !important;
            border: 1px solid #E6EDF9;
            border-radius: 16px;
            padding: 16px;
            min-height: 152px;
        }

        .botdiag-xai-card.red {
            background: #FFF5F9 !important;
            border-color: #FFC6D8;
        }

        .botdiag-xai-card.green {
            background: #F1FCF8 !important;
            border-color: #BFE9DC;
        }

        .botdiag-card-chip {
            display: inline-block;
            border-radius: 999px;
            padding: 4px 9px;
            font-size: 0.72rem;
            font-weight: 780;
            letter-spacing: 0.02em;
            margin-bottom: 10px;
        }

        .botdiag-card-chip.red {
            background: #FFE7EE !important;
            color: #B21E52;
            border: 1px solid #FFC9D8;
        }

        .botdiag-card-chip.green {
            background: #EAF9F3 !important;
            color: #107A73;
            border: 1px solid #C7EBDD;
        }

        .botdiag-card-title {
            color: #14357F;
            font-size: 0.98rem;
            font-weight: 800;
            margin: 0;
        }

        .botdiag-card-text {
            color: #596D98;
            font-size: 0.84rem;
            line-height: 1.4;
            margin: 8px 0 0 0;
        }

        .botdiag-xai-info {
            margin-top: 12px;
        }

        .botdiag-reco-title {
            color: #0E2E87;
            font-size: 1rem;
            font-weight: 820;
            margin: 4px 0 10px 0;
        }

        .botdiag-reco-box {
            background: #FFFFFF !important;
            border: 1px solid #E4EAF9;
            border-radius: 14px;
            padding: 12px;
            min-height: 108px;
        }

        .botdiag-reco-label {
            color: #5A6D97;
            font-size: 0.76rem;
            font-weight: 760;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .botdiag-reco-value {
            color: #12317F;
            font-size: 1.24rem;
            font-weight: 840;
            margin-top: 6px;
        }

        .botdiag-reco-sub {
            color: #5A6D97;
            font-size: 0.82rem;
            margin-top: 4px;
        }

        .botdiag-flow-row {
            display: flex;
            align-items: stretch;
            gap: 14px;
            margin-top: 10px;
            margin-bottom: 12px;
        }

        .botdiag-flow-box {
            flex: 1;
            background: #FFFFFF !important;
            border: 1px solid #E4EAF9;
            border-radius: 14px;
            padding: 12px;
            min-height: 112px;
        }

        .botdiag-flow-box.source {
            border-color: #002261;
            background: #002261 !important;
        }

        .botdiag-flow-box.target {
            border-color: #002261;
            background: #002261 !important;
        }

        .botdiag-flow-label {
            color: #5A6D97;
            font-size: 0.75rem;
            font-weight: 760;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .botdiag-flow-name {
            color: #12317F;
            font-size: 1.05rem;
            font-weight: 840;
            margin-top: 7px;
            line-height: 1.2;
        }

        .botdiag-flow-sub {
            color: #5A6D97;
            font-size: 0.82rem;
            margin-top: 6px;
        }

        .botdiag-flow-box.source .botdiag-flow-label,
        .botdiag-flow-box.source .botdiag-flow-name,
        .botdiag-flow-box.source .botdiag-flow-sub,
        .botdiag-flow-box.target .botdiag-flow-label,
        .botdiag-flow-box.target .botdiag-flow-name,
        .botdiag-flow-box.target .botdiag-flow-sub {
            color: #FFFFFF !important;
        }

        .botdiag-flow-arrow {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-width: 164px;
            gap: 6px;
        }

        .botdiag-flow-amount {
            color: #A11453;
            font-size: 0.9rem;
            font-weight: 820;
            background: #FFEAF3 !important;
            border: 1px solid #FFC9DE;
            border-radius: 999px;
            padding: 4px 10px;
        }

        .botdiag-flow-arrowline {
            color: #24439E;
            font-size: 1.75rem;
            line-height: 1;
            font-weight: 800;
        }

        .botdiag-reco-box.risk-banner {
            min-height: 0;
            padding: 9px 14px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
            flex-wrap: wrap;
            margin-top: 10px;
            transition: background 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
        }

        .botdiag-reco-box.risk-banner .botdiag-reco-label,
        .botdiag-reco-box.risk-banner .botdiag-reco-value,
        .botdiag-reco-box.risk-banner .botdiag-reco-sub {
            margin: 0;
        }

        .botdiag-reco-box.risk-banner .botdiag-reco-value {
            font-size: 1.02rem;
            white-space: nowrap;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }

        .botdiag-risk-arrow {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 22px;
            height: 22px;
            border-radius: 999px;
            font-size: 0.9rem;
            font-weight: 900;
        }

        .botdiag-reco-box.risk-warning {
            background: #FFF8CC !important;
            border-color: #F0D451;
            box-shadow: 0 0 0 2px rgba(240, 212, 81, 0.28);
        }

        .botdiag-reco-box.risk-warning .botdiag-reco-label,
        .botdiag-reco-box.risk-warning .botdiag-reco-value,
        .botdiag-reco-box.risk-warning .botdiag-reco-sub {
            color: #6A5200 !important;
        }

        .botdiag-reco-box.risk-warning .botdiag-risk-arrow {
            background: rgba(240, 212, 81, 0.42);
            color: #6A5200;
            border: 1px solid rgba(106, 82, 0, 0.2);
        }

        .botdiag-reco-box.risk-ok {
            background: #E9FFF1 !important;
            border-color: #56C982;
            box-shadow: 0 0 0 2px rgba(86, 201, 130, 0.22);
        }

        .botdiag-reco-box.risk-ok .botdiag-reco-label,
        .botdiag-reco-box.risk-ok .botdiag-reco-value,
        .botdiag-reco-box.risk-ok .botdiag-reco-sub {
            color: #0F6A36 !important;
        }

        .botdiag-reco-box.risk-ok .botdiag-risk-arrow {
            background: rgba(86, 201, 130, 0.3);
            color: #0F6A36;
            border: 1px solid rgba(15, 106, 54, 0.2);
        }

        .botdiag-decision-result {
            background: #EFF5FF !important;
            border: 1px solid #D6E1FB;
            color: #16377E;
            border-radius: 14px;
            padding: 12px 14px;
            font-size: 0.9rem;
            font-weight: 700;
            margin-top: 12px;
        }

        .st-key-botdiag-btn-validate button,
        .st-key-botdiag-btn-refuse button,
        .st-key-botdiag-btn-advisor button {
            color: #FFFFFF !important;
            border: none !important;
            font-weight: 760 !important;
        }

        .st-key-botdiag-btn-validate button {
            background: #02ADA5 !important;
        }

        .st-key-botdiag-btn-refuse button {
            background: #D92063 !important;
        }

        .st-key-botdiag-btn-advisor button {
            background: #002261 !important;
        }

        .st-key-botdiag-btn-validate button:hover,
        .st-key-botdiag-btn-refuse button:hover,
        .st-key-botdiag-btn-advisor button:hover {
            filter: brightness(0.95);
        }

        .botdiag-targeted-reco {
            background: #F4F8FF !important;
            border: 1px solid #D8E4FF;
            border-radius: 12px;
            padding: 10px 12px;
            margin-top: 10px;
        }

        .botdiag-targeted-reco-title {
            color: #21408F;
            font-size: 0.84rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            margin: 0 0 4px 0;
        }

        .botdiag-targeted-reco-text {
            color: #314A83;
            font-size: 0.9rem;
            margin: 0;
            line-height: 1.35;
        }

        .botdiag-chat-wrap {
            display: flex;
            align-items: flex-start;
            gap: 12px;
            margin-top: 10px;
            margin-bottom: 10px;
            margin-left: -8px;
        }

        .botdiag-chat-avatar {
            width: 62px;
            height: 62px;
            flex-shrink: 0;
            object-fit: contain;
            image-rendering: auto;
        }

        .botdiag-chat-bubble {
            background: #EAF2FF !important;
            border: 1px solid #CFE0FF;
            border-radius: 14px;
            padding: 12px 14px;
            color: #224283;
            line-height: 1.4;
            font-size: 0.9rem;
            flex: 1;
            width: 100%;
        }

        .botdiag-chat-title {
            color: #173A81;
            font-size: 0.82rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            margin: 0 0 4px 0;
        }

        .botdiag-chat-text {
            margin: 0;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _decision_message(decision: str) -> str:
    messages = {
        "validate": "Arbitrage valide: transfert prioritaire vers CNP Obligations Europe prepare.",
        "refuse": "Refus enregistre: maintien temporaire de l'allocation actuelle et suivi renforce.",
        "advisor": "Mise en relation demandee: un conseiller CNP vous recontacte pour arbitrage assiste.",
    }
    return messages[decision]


def _fmt_eur(value: float) -> str:
    return f"{value:,.0f}".replace(",", " ") + " EUR"


def _bot_avatar_base64() -> str:
    avatar_path = Path(__file__).resolve().parent.parent / "images" / "robot-CNP.png"
    return base64.b64encode(avatar_path.read_bytes()).decode("ascii")


def _render_bot_chat_message(title: str, text: str) -> None:
    avatar_b64 = _bot_avatar_base64()
    st.markdown(
        f"""
        <div class="botdiag-chat-wrap">
            <img class="botdiag-chat-avatar" src="data:image/png;base64,{avatar_b64}" alt="Bot CNP" />
            <div class="botdiag-chat-bubble">
                <p class="botdiag-chat-title">{title}</p>
                <p class="botdiag-chat-text">{text}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _impact_figure(transfer_eur: float) -> go.Figure:
    before_actions = ACCOUNT_TOUCHED_VALUE
    after_actions = max(0.0, ACCOUNT_TOUCHED_VALUE - transfer_eur)

    before_bonds = ACCOUNT_TARGET_VALUE
    after_bonds = ACCOUNT_TARGET_VALUE + transfer_eur

    df = pd.DataFrame(
        {
            "poste": [f"{ACCOUNT_TOUCHED} (compte touche)", f"{ACCOUNT_TARGET} (destination)"],
            "Avant": [before_actions, before_bonds],
            "Apres": [after_actions, after_bonds],
        }
    )

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=df["poste"],
            y=df["Avant"],
            name="Avant",
            marker_color="#02ADA5",
            text=[_fmt_eur(v) for v in df["Avant"]],
            textposition="outside",
        )
    )
    fig.add_trace(
        go.Bar(
            x=df["poste"],
            y=df["Apres"],
            name="Apres",
            marker_color="#002261",
            text=[_fmt_eur(v) for v in df["Apres"]],
            textposition="outside",
        )
    )

    fig.update_layout(
        barmode="group",
        height=290,
        margin={"l": 0, "r": 0, "t": 18, "b": 0},
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        legend={"orientation": "h", "x": 0, "y": 1.15},
        font={"color": "#40527E"},
        hovermode="x unified",
    )
    fig.update_yaxes(gridcolor="#EEF3FE", title=None, tickformat=",.0f", separatethousands=True)
    fig.update_xaxes(title=None, showgrid=False)
    return fig


def show_bot_diagnostic() -> None:
    _init_state()
    _render_styles()

    observed_risk = 5.0
    target_risk = 3.7
    risk_gap = observed_risk - target_risk

    st.markdown('<h1 class="botdiag-title">Diagnostic copilote</h1>', unsafe_allow_html=True)

    with st.container(border=True, key="botdiag-hero"):
        st.markdown(
            '<div class="botdiag-hero-top"><p class="botdiag-step-title">Derive de risque detectee</p><span class="botdiag-hero-tag">Alerte active</span></div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<p class="botdiag-step-text">Votre portefeuille depasse le profil cible. Priorite: reduire la concentration actions cycliques.</p>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
            <div class="botdiag-hero-grid">
                <div class="botdiag-hero-kpi">
                    <p class="botdiag-hero-kpi-label">Risque observe</p>
                    <p class="botdiag-hero-kpi-value warning">{observed_risk:.1f}/7</p>
                </div>
                <div class="botdiag-hero-kpi">
                    <p class="botdiag-hero-kpi-label">Cible profil</p>
                    <p class="botdiag-hero-kpi-value">{target_risk:.1f}/7</p>
                </div>
                <div class="botdiag-hero-kpi">
                    <p class="botdiag-hero-kpi-label">Ecart a corriger</p>
                    <p class="botdiag-hero-kpi-value warning">+{risk_gap:.1f}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)

    with st.container(border=True, key="botdiag-xai"):
        st.markdown('<p class="botdiag-step-title">Pourquoi cette alerte</p>', unsafe_allow_html=True)
        st.markdown('<div style="height:2px;"></div>', unsafe_allow_html=True)

        _, col1, col2, _ = st.columns([0.09, 1, 1, 0.09], gap="large")
        with col1:
            st.markdown(
                """
                <div class="botdiag-xai-card red">
                    <span class="botdiag-card-chip red">Risque principal</span>
                    <p class="botdiag-card-title">Actions cycliques trop exposees</p>
                    <p class="botdiag-card-text">La poche actions europeennes amplifie la volatilite du portefeuille.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with col2:
            st.markdown(
                """
                <div class="botdiag-xai-card green">
                    <span class="botdiag-card-chip green">Action recommandee</span>
                    <p class="botdiag-card-title">Renforcer l'obligataire</p>
                    <p class="botdiag-card-text">CNP Obligations Europe aide a lisser le risque a court terme.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        _render_bot_chat_message(
            "Detail explicatif",
            "Votre risque observe depasse la cible du profil car la poche actions cycliques est devenue dominante dans le contexte de marche actuel. Le moteur compare la cible, l'allocation reelle et les expositions sectorielles, puis recommande un reequilibrage progressif vers CNP Obligations Europe afin de reduire la volatilite et de converger vers le niveau de risque attendu.",
        )

    st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)

    with st.container(border=True, key="botdiag-reco"):
        st.markdown('<p class="botdiag-step-title">Recommendation et mouvement propose</p>', unsafe_allow_html=True)

        transfer_eur = float(st.session_state.get("botdiag_transfer", 5000))

        before_risk = observed_risk
        after_risk = max(3.6, before_risk - (transfer_eur / 10000) * 1.4)
        risk_is_above_profile = after_risk > target_risk
        risk_state_class = "risk-warning" if risk_is_above_profile else "risk-ok"
        risk_state_text = "Au-dessus du profil" if risk_is_above_profile else "Au niveau du profil"

        st.markdown(
            f"""
            <div class="botdiag-flow-row">
                <div class="botdiag-flow-box source">
                    <div class="botdiag-flow-label">Compte touche</div>
                    <div class="botdiag-flow-name">{ACCOUNT_TOUCHED}</div>
                    <div class="botdiag-flow-sub">Valeur actuelle: {_fmt_eur(ACCOUNT_TOUCHED_VALUE)}</div>
                </div>
                <div class="botdiag-flow-arrow">
                    <div class="botdiag-flow-amount">{_fmt_eur(transfer_eur)}</div>
                    <div class="botdiag-flow-arrowline">→</div>
                </div>
                <div class="botdiag-flow-box target">
                    <div class="botdiag-flow-label">Compte destination</div>
                    <div class="botdiag-flow-name">{ACCOUNT_TARGET}</div>
                    <div class="botdiag-flow-sub">Valeur actuelle: {_fmt_eur(ACCOUNT_TARGET_VALUE)}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<p class="botdiag-reco-title">Simulez</p>', unsafe_allow_html=True)
        transfer_eur = st.slider(
            "Montant a transferer vers CNP Obligations Europe",
            min_value=1000,
            max_value=10000,
            step=500,
            value=int(transfer_eur),
            key="botdiag_transfer",
        )
        st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)

        st.markdown('<p class="botdiag-reco-title">Impact avant / apres du mouvement</p>', unsafe_allow_html=True)
        st.plotly_chart(_impact_figure(float(transfer_eur)), width="stretch", key="botdiag_impact_chart")
        st.markdown('<div style="height:10px;"></div>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="botdiag-reco-box risk-banner {risk_state_class}">
                <div class="botdiag-reco-label">Risque estime</div>
                <div class="botdiag-reco-value">{before_risk:.1f}/7 <span class="botdiag-risk-arrow">➜</span> {after_risk:.1f}/7</div>
                <div class="botdiag-reco-sub">{risk_state_text} | Objectif profil: {target_risk:.1f}/7</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        _render_bot_chat_message(
            "Targeted Support | People Like You",
            "85 % des epargnants dans une situation similaire a la votre ont valide ce reequilibrage de 5 000 EUR vers CNP Obligations Europe pour mieux proteger leur capital.",
        )
        st.markdown('<div style="height:10px;"></div>', unsafe_allow_html=True)
        st.markdown('<p class="botdiag-step-title">Decision</p>', unsafe_allow_html=True)

        d1, d2, d3 = st.columns(3, gap="small")

        with d1:
            with st.container(key="botdiag-btn-validate"):
                if st.button("Valider", key="botdiag_validate", width="stretch"):
                    st.session_state.bot_diagnostic_decision = "validate"
        with d2:
            with st.container(key="botdiag-btn-refuse"):
                if st.button("Refuser", key="botdiag_refuse", width="stretch"):
                    st.session_state.bot_diagnostic_decision = "refuse"
        with d3:
            with st.container(key="botdiag-btn-advisor"):
                if st.button("Echanger avec mon conseiller", key="botdiag_advisor", width="stretch"):
                    st.session_state.bot_diagnostic_decision = "advisor"

        if st.session_state.bot_diagnostic_decision:
            st.markdown(
                f'<div class="botdiag-decision-result">{_decision_message(st.session_state.bot_diagnostic_decision)}</div>',
                unsafe_allow_html=True,
            )
        st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)


if __name__ == "__main__":
    show_bot_diagnostic()
