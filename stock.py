from __future__ import annotations

from datetime import date, timedelta
import math

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


ACCOUNTS = [
    {
        "name": "CNP Actions Climat ESG",
        "category": "Actions Etats-Unis",
        "weight": 27.27,
        "value": 13635.0,
        "perf": 11.25,
        "risk": 5,
        "color": "#FF2B70",
    },
    {
        "name": "CNP Actions US Couvertes",
        "category": "Actions Etats-Unis couvertes",
        "weight": 13.63,
        "value": 6815.0,
        "perf": 1.57,
        "risk": 4,
        "color": "#D92063",
    },
    {
        "name": "CNP Obligations Monde Diversifiees",
        "category": "Obligations monde",
        "weight": 9.39,
        "value": 4695.0,
        "perf": 2.07,
        "risk": 3,
        "color": "#2C47A9",
    },
    {
        "name": "CNP Actions Pays Emergents",
        "category": "Actions Emergents",
        "weight": 8.87,
        "value": 4435.0,
        "perf": 27.22,
        "risk": 6,
        "color": "#B31957",
    },
    {
        "name": "CNP Actions Europe Couvertes",
        "category": "Actions Europe",
        "weight": 6.10,
        "value": 3050.0,
        "perf": 14.13,
        "risk": 4,
        "color": "#F34080",
    },
    {
        "name": "CNP Obligations Euro IG",
        "category": "Obligations Europe",
        "weight": 5.99,
        "value": 2995.0,
        "perf": 0.84,
        "risk": 2,
        "color": "#415FC8",
    },
]


def _fmt_eur(v: float) -> str:
    return f"{v:,.0f}".replace(",", " ") + " EUR"


def _init_state() -> None:
    if "poc4_shock_messages" not in st.session_state:
        st.session_state.poc4_shock_messages = [
            {
                "role": "assistant",
                "content": (
                    "⚠️ Alerte rééquilibrage: la baisse récente du secteur automobile a créé une dérive de risque."
                ),
            },
            {
                "role": "assistant",
                "content": (
                    "Plan d'action en 5 étapes activé: notification, explication XAI, support ciblé, "
                    "décision utilisateur, escalade humaine si nécessaire."
                ),
            },
        ]


def _render_styles() -> None:
    st.markdown(
        """
        <style>
        /* Fond global pastel épuré */
        .stApp {
            background:
                radial-gradient(950px 420px at -10% -20%, rgba(3, 43, 246, 0.08), transparent 65%),
                radial-gradient(900px 460px at 115% -10%, rgba(2, 173, 165, 0.07), transparent 62%),
                linear-gradient(180deg, #F4F7FC 0%, #EBF0F9 100%) !important;
        }

        /* FORCER FOND BLANC SUR LES CONTENEURS BENTO STREAMLIT */
        div[data-testid="stColumn"] > div[data-testid="stVerticalBlockBorderWrapper"],
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background-color: #FFFFFF !important;
            border: 1px solid #E1E8F5 !important;
            border-radius: 16px !important;
            box-shadow: 0px 4px 12px rgba(3, 43, 246, 0.03) !important;
        }

        /* Nettoyage des sous-couches internes */
        div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stVerticalBlock"],
        div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stMarkdownContainer"] {
            background-color: transparent !important;
        }

        .poc4-title {
            color: #032BF6;
            font-size: 2.1rem;
            font-weight: 850;
            margin: 0;
            line-height: 1.05;
            letter-spacing: 0.01em;
        }

        .poc4-sub {
            color: #566A98;
            font-size: 0.94rem;
            margin-top: 5px;
            margin-bottom: 16px;
        }

        .poc4-alert {
            background: linear-gradient(90deg, rgba(255, 1, 102, 0.12), rgba(255, 1, 102, 0.04)) !important;
            border: 1px solid rgba(255, 1, 102, 0.3);
            border-left: 5px solid #FF0166;
            color: #7E0E44;
            border-radius: 12px;
            padding: 12px 16px;
            font-size: 0.89rem;
            font-weight: 760;
            margin-bottom: 14px;
        }

        /* Tuiles Bento KPI */
        .poc4-kpi-tile {
            background-color: #FFFFFF !important;
            border: 1px solid #E1E8F5;
            border-radius: 16px;
            padding: 14px 16px;
            min-height: 98px;
            box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.02);
        }

        .poc4-kpi-label {
            color: #5C6C95;
            font-size: 0.76rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }

        .poc4-kpi-value {
            color: #12317F;
            font-size: 1.75rem;
            font-weight: 840;
            line-height: 1;
            margin-top: 8px;
        }

        .poc4-kpi-delta {
            margin-top: 7px;
            font-size: 0.79rem;
            font-weight: 760;
            color: #107A73;
        }

        .poc4-kpi-delta.negative {
            color: #A11453;
        }

        .poc4-module-title {
            color: #0E2E87;
            font-size: 1.05rem;
            font-weight: 820;
            margin-bottom: 2px;
        }

        .poc4-module-sub {
            color: #5C6C95;
            font-size: 0.82rem;
            margin-bottom: 8px;
        }

        .poc4-chip-row {
            display: flex;
            flex-wrap: wrap;
            gap: 7px;
            margin-top: 6px;
        }

        .poc4-chip {
            border-radius: 999px;
            padding: 3px 9px;
            font-size: 0.74rem;
            font-weight: 800;
        }

        .poc4-chip.blue {
            background: #EAF0FF;
            border: 1px solid #CBD8FF;
            color: #284AA8;
        }

        .poc4-chip.pink {
            background: #FFEAF5;
            border: 1px solid #FFC9E3;
            color: #9A0F52;
        }

        .poc4-account-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 10px;
            margin-bottom: 12px;
        }

        .poc4-accounts-dark {
            background: linear-gradient(180deg, #082A73 0%, #05225F 100%);
            border: 1px solid rgba(255, 255, 255, 0.16);
            border-radius: 14px;
            padding: 12px;
        }

        .poc4-accounts-dark .poc4-account-title {
            color: #F4F7FF;
        }

        .poc4-accounts-dark .poc4-account-sub {
            color: #C8D8FF;
        }

        .poc4-accounts-dark .poc4-chip.blue {
            background: rgba(234, 240, 255, 0.12);
            border: 1px solid rgba(203, 216, 255, 0.45);
            color: #EAF0FF;
        }

        .poc4-accounts-dark .poc4-chip.pink {
            background: rgba(255, 234, 245, 0.12);
            border: 1px solid rgba(255, 201, 227, 0.45);
            color: #FFD4EA;
        }

        .poc4-accounts-dark .poc4-list-row {
            background: #FFFFFF !important;
            border: 1px solid #DCE7FB !important;
            box-shadow: 0px 3px 10px rgba(5, 34, 95, 0.08);
        }

        .poc4-accounts-dark .poc4-list-row:hover {
            border-color: #C8D8FF !important;
            box-shadow: 0px 5px 14px rgba(5, 34, 95, 0.12);
        }

        .poc4-accounts-dark .poc4-list-name,
        .poc4-accounts-dark .poc4-list-value,
        .poc4-accounts-dark .poc4-list-foot {
            color: #12317F;
        }

        .poc4-accounts-dark .poc4-list-cat {
            color: #6475A0;
        }

        .poc4-accounts-dark .poc4-list-perf {
            color: #127A73;
        }

        .poc4-accounts-dark .poc4-list-bar-track {
            background: #EEF3FE;
        }

        .poc4-account-title {
            color: #0E2E87;
            font-size: 1.08rem;
            font-weight: 820;
            margin: 0;
        }

        .poc4-account-sub {
            color: #5C6C95;
            font-size: 0.82rem;
            margin: 0;
        }

        /* Cartes de fonds individuelles */
        .poc4-list-row {
            background-color: #FFFFFF !important;
            border: 1px solid #E6EEFA !important;
            border-radius: 12px;
            padding: 12px 14px;
            margin-bottom: 10px;
            transition: all 0.2s ease;
        }

        .poc4-list-row:hover {
            border-color: #CBD8FF !important;
            box-shadow: 0px 4px 12px rgba(3, 43, 246, 0.05);
        }

        .poc4-list-top {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 10px;
        }

        .poc4-list-name {
            color: #12317F;
            font-size: 0.92rem;
            font-weight: 780;
            line-height: 1.2;
            margin: 0;
        }

        .poc4-list-cat {
            color: #6475A0;
            font-size: 0.77rem;
            margin-top: 2px;
            margin-bottom: 0;
        }

        .poc4-list-right {
            text-align: right;
            min-width: 132px;
        }

        .poc4-list-value {
            color: #133381;
            font-size: 0.9rem;
            font-weight: 780;
            margin: 0;
        }

        .poc4-list-perf {
            color: #127A73;
            font-size: 0.79rem;
            font-weight: 760;
            margin-top: 1px;
            margin-bottom: 0;
        }

        .poc4-list-bar-track {
            width: 100%;
            height: 7px;
            border-radius: 999px;
            background: #EEF3FE;
            overflow: hidden;
            margin-top: 10px;
        }

        .poc4-list-bar-fill {
            height: 100%;
            border-radius: 999px;
        }

        .poc4-list-foot {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 6px;
            color: #66779F;
            font-size: 0.75rem;
            font-weight: 700;
        }

        .poc4-decisions-title {
            color: #0E2E87;
            font-size: 0.98rem;
            font-weight: 800;
            margin-top: 2px;
            margin-bottom: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _build_performance_df() -> pd.DataFrame:
    end_day = date.today()
    start_day = end_day - timedelta(days=180)
    dates = pd.date_range(start=start_day, end=end_day, freq="D")

    points = len(dates)
    apports = []
    valorisation = []

    for i in range(points):
        t = i / max(1, points - 1)
        apport = 45000 + 5000 * t
        apports.append(apport)

        surplus = 90 + 2100 * (t**1.12) + 120 * math.sin(9 * t)
        valorisation.append(apport + surplus)

    shock_days = 26
    shock_loss = 1700.0
    for j in range(shock_days):
        idx = points - shock_days + j
        ratio = (j + 1) / shock_days
        valorisation[idx] -= shock_loss * ratio
        valorisation[idx] = max(apports[idx] + 220, valorisation[idx])

    return pd.DataFrame({"date": dates, "apports": apports, "valorisation": valorisation})


def _performance_figure(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["apports"],
            mode="lines",
            name="Apports/Retraits cumulés",
            line={"color": "#8AA5D3", "width": 2, "dash": "dash"},
            hovertemplate="%{x|%d/%m/%Y}<br>Apports: %{y:,.0f} EUR<extra></extra>",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["valorisation"],
            mode="lines",
            name="Valorisation réelle",
            line={"color": "#032BF6", "width": 3, "shape": "spline"},
            fill="tonexty",
            fillcolor="rgba(3, 43, 246, 0.08)",
            hovertemplate="%{x|%d/%m/%Y}<br>Valorisation: %{y:,.0f} EUR<extra></extra>",
        )
    )

    fig.add_vrect(
        x0=df["date"].iloc[-24],
        x1=df["date"].iloc[-1],
        fillcolor="rgba(255, 1, 102, 0.08)",
        line_width=0,
    )

    fig.update_layout(
        height=320,
        margin={"l": 0, "r": 0, "t": 10, "b": 0},
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        hovermode="x unified",
        hoverlabel={"bgcolor": "#FFFFFF", "bordercolor": "#C9D7F8", "font_color": "#15347E"},
        legend={"orientation": "h", "x": 0, "y": 1.15},
    )
    fig.update_xaxes(
        showgrid=False,
        title=None,
        showline=False,
        showspikes=True,
        spikecolor="#16377E",
        spikethickness=1,
        spikedash="solid",
    )
    fig.update_yaxes(
        gridcolor="#F0F4FC",
        zeroline=False,
        title=None,
        tickformat=",.0f",
        separatethousands=True,
    )

    return fig


def _risk_figure() -> go.Figure:
    target = 3
    observed = 5
    fig = go.Figure(
        data=[
            go.Bar(
                x=["Profil cible", "Observé"],
                y=[target, observed],
                marker_color=["#2D4FB4", "#FF2B70"],
                width=0.4,
                text=["3/7", "5/7"],
                textposition="outside",
            )
        ]
    )

    fig.add_hline(
        y=target,
        line_dash="dash",
        line_color="#02ADA5",
        line_width=1.5,
        annotation_text="Seuil choisi",
        annotation_position="top left",
        annotation_font_color="#117D76",
    )

    fig.update_layout(
        height=200,
        margin={"l": 0, "r": 0, "t": 20, "b": 0},
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        showlegend=False,
    )
    fig.update_yaxes(range=[0, 7.2], dtick=1, gridcolor="#F0F4FC", title=None)
    fig.update_xaxes(title=None)

    return fig


def _allocation_donut_figure() -> go.Figure:
    labels = ["Fonds Euro", "Unités de compte"]
    values = [68, 32]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.72,
                sort=False,
                marker={"colors": ["#032BF6", "#FF2B70"]},
                textinfo="percent",
                hovertemplate="%{label}<br>%{value}%<extra></extra>",
            )
        ]
    )

    fig.update_layout(
        height=200,
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
        paper_bgcolor="#FFFFFF",
        showlegend=False,
    )

    fig.add_annotation(
        x=0.5,
        y=0.5,
        text="UC<br><b>32%</b>",
        showarrow=False,
        font={"size": 14, "color": "#12317F", "family": "sans-serif"},
    )

    return fig


def _render_kpi_tile(label: str, value: str, delta: str, negative: bool = False) -> None:
    delta_cls = "poc4-kpi-delta negative" if negative else "poc4-kpi-delta"
    st.markdown(
        f"""
        <div class="poc4-kpi-tile">
            <div class="poc4-kpi-label">{label}</div>
            <div class="poc4-kpi-value">{value}</div>
            <div class="{delta_cls}">{delta}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_account_rows(df: pd.DataFrame) -> str:
    rows_html = []
    for row in df.to_dict("records"):
        perf_color = "#127A73" if row["perf"] >= 0 else "#A11453"
        perf_sign = "+" if row["perf"] >= 0 else ""

        row_html = (
            f'<div class="poc4-list-row">'
            f'<div class="poc4-list-top">'
            f'<div>'
            f'<p class="poc4-list-name">{row["name"]}</p>'
            f'<p class="poc4-list-cat">{row["category"]}</p>'
            f'</div>'
            f'<div class="poc4-list-right">'
            f'<p class="poc4-list-value">{_fmt_eur(row["value"])}</p>'
            f'<p class="poc4-list-perf" style="color:{perf_color};">{perf_sign}{row["perf"]:.2f}%</p>'
            f'</div>'
            f'</div>'
            f'<div class="poc4-list-bar-track">'
            f'<div class="poc4-list-bar-fill" style="width:{row["weight"]}%;background:{row["color"]};"></div>'
            f'</div>'
            f'<div class="poc4-list-foot">'
            f'<span>Poids portefeuille: {row["weight"]:.2f}%</span>'
            f'<span>SRI {row["risk"]}/7</span>'
            f'</div>'
            f'</div>'
        )
        rows_html.append(row_html)
    return "".join(rows_html)


def _render_top_bento(df_accounts: pd.DataFrame) -> None:
    st.markdown(
        '<div class="poc4-alert">🚨 Choc de marché détecté: ralentissement brusque du secteur automobile européen. '
        'Impact direct sur vos UC CNP Actions Climat ESG.</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4, gap="small")
    with c1:
        _render_kpi_tile("Valorisation", "50 000 EUR", "+803 EUR")
    with c2:
        _render_kpi_tile("Performance mensuelle", "+2,4%", "Évolution positive")
    with c3:
        _render_kpi_tile("Risque observé", "5/7", "+2 niveaux vs cible", negative=True)
    with c4:
        _render_kpi_tile("Allocation UC", "32%", "-8 pts vs cible", negative=True)

    st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)

    chart_col, side_col = st.columns([2.18, 1.0], gap="medium")

    with chart_col:
        with st.container(border=True):
            st.markdown('<div class="poc4-module-title">Performance portefeuille</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="poc4-module-sub">Apports/Retraits cumulés vs valorisation réelle. Zone rose: choc récent.</div>',
                unsafe_allow_html=True,
            )
            st.plotly_chart(_performance_figure(_build_performance_df()), use_container_width=True, key="poc4_perf_bento")

    with side_col:
        with st.container(border=True):
            st.markdown('<div class="poc4-module-title">Niveau de risque (SRI)</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="poc4-module-sub">Barres verticales avec seuil contractuel.</div>',
                unsafe_allow_html=True,
            )
            st.plotly_chart(_risk_figure(), use_container_width=True, key="poc4_risk_bento")

        with st.container(border=True):
            st.markdown('<div class="poc4-module-title">Répartition</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="poc4-module-sub">Allocation globale du portefeuille.</div>',
                unsafe_allow_html=True,
            )
            st.plotly_chart(_allocation_donut_figure(), use_container_width=True, key="poc4_alloc_donut")


def _render_bottom_accounts(df_accounts: pd.DataFrame) -> None:
    st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)
    rows_html = _render_account_rows(df_accounts)
    st.markdown(
        (
            '<div class="poc4-accounts-dark">'
            '<div class="poc4-account-header">'
            '<div>'
            '<p class="poc4-account-title">Détail compte par compte</p>'
            '<p class="poc4-account-sub">Vue vérité des positions, exposition et performance.</p>'
            '</div>'
            '<div class="poc4-chip-row">'
            '<span class="poc4-chip blue">6 lignes</span>'
            '<span class="poc4-chip pink">Focus actions</span>'
            '</div>'
            '</div>'
            f'{rows_html}'
            '</div>'
        ),
        unsafe_allow_html=True,
    )


def _render_decisions() -> None:
    st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown('<div class="poc4-decisions-title">Décision rapide (protocole choc)</div>', unsafe_allow_html=True)

        d1, d2, d3, d4 = st.columns(4, gap="small")

        if d1.button("Rééquilibrer", key="poc4_decision_1", type="primary", use_container_width=True):
            st.session_state.poc4_shock_messages.append(
                {
                    "role": "assistant",
                    "content": "Rééquilibrage lancé: réduction progressive UC et renforcement Fonds Euro.",
                }
            )
            st.rerun()

        if d2.button("Conserver 7 jours", key="poc4_decision_2", use_container_width=True):
            st.session_state.poc4_shock_messages.append(
                {
                    "role": "assistant",
                    "content": "Conservation 7 jours enregistrée. Monitoring renforcé actif.",
                }
            )
            st.rerun()

        if d3.button("Réduire UC 8%", key="poc4_decision_3", use_container_width=True):
            st.session_state.poc4_shock_messages.append(
                {
                    "role": "assistant",
                    "content": "Arbitrage préparé: UC -8% vers poches défensives obligataires.",
                }
            )
            st.rerun()

        if d4.button("Escalade humaine", key="poc4_decision_4", use_container_width=True):
            st.session_state.poc4_shock_messages.append(
                {
                    "role": "assistant",
                    "content": "Escalade confirmée: un conseiller vous contacte sous 24h.",
                }
            )
            st.rerun()

        for msg in st.session_state.poc4_shock_messages[-3:]:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])


def show_poc4() -> None:
    _init_state()
    _render_styles()

    st.markdown('<h1 class="poc4-title">Mon espace</h1>', unsafe_allow_html=True)
    st.markdown(
        '<div class="poc4-sub">Dashboard Bento utile en haut, détail des comptes en dessous.</div>',
        unsafe_allow_html=True,
    )

    df_accounts = pd.DataFrame(ACCOUNTS)

    _render_top_bento(df_accounts)
    _render_bottom_accounts(df_accounts)
    _render_decisions()


if __name__ == "__main__":
    show_poc4()