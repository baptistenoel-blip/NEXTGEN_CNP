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


def _fmt_eur(value: float) -> str:
    return f"{value:,.0f}".replace(",", " ") + " EUR"


def _render_styles() -> None:
    st.markdown(
        """
        <style>
        .stApp {
            background:
                radial-gradient(950px 420px at -10% -20%, rgba(3, 43, 246, 0.08), transparent 65%),
                radial-gradient(900px 460px at 115% -10%, rgba(2, 173, 165, 0.07), transparent 62%),
                linear-gradient(180deg, #F4F7FC 0%, #EBF0F9 100%) !important;
        }

        .st-key-poc3-copilot-card,
        .st-key-poc3-perf-card,
        .st-key-poc3-risk-card,
        .st-key-poc3-allocation-card {
            background: #FFFFFF !important;
            border: 1px solid #E1E8F5 !important;
            border-radius: 16px !important;
            box-shadow: 0 4px 14px rgba(3, 43, 246, 0.045) !important;
            padding: 16px !important;
        }

        .st-key-poc3-copilot-card {
            padding: 14px 16px 28px 16px !important;
        }

        .st-key-poc3-perf-card {
            min-height: 596px;
        }

        .st-key-poc3-perf-card *,
        .st-key-poc3-risk-card *,
        .st-key-poc3-allocation-card * {
            background-color: transparent !important;
        }

        .poc3-title {
            color: #032BF6;
            font-size: 2.1rem;
            font-weight: 850;
            margin: 0;
            line-height: 1.05;
            letter-spacing: 0.01em;
        }

        .poc3-sub {
            color: #566A98;
            font-size: 0.94rem;
            margin-top: 5px;
            margin-bottom: 16px;
        }

        .poc3-copilot-title {
            color: #09286F;
            font-size: 1.16rem;
            font-weight: 860;
            letter-spacing: 0.01em;
            margin: 0;
        }

        .poc3-copilot-subtitle {
            color: #2D4FB4;
            font-size: 0.8rem;
            font-weight: 780;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-top: 4px;
            margin-bottom: 8px;
        }

        .poc3-copilot-text {
            color: #4B5F8F;
            font-size: 0.9rem;
            line-height: 1.42;
            margin: 0 0 10px 0;
            max-width: 680px;
        }

        .poc3-alert-link {
            display: block;
            text-decoration: none !important;
        }

        .poc3-alert-link:hover {
            text-decoration: none !important;
        }

        .poc3-copilot-alert-card {
            background: #FFFFFF !important;
            border: 1px solid #E4EAF9;
            border-radius: 14px;
            padding: 12px 14px;
            box-shadow: 0 4px 12px rgba(16, 43, 117, 0.06);
            margin-top: 2px;
            transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
        }

        .poc3-alert-link:hover .poc3-copilot-alert-card {
            transform: translateY(-1px);
            border-color: #CFDAF7;
            box-shadow: 0 8px 18px rgba(16, 43, 117, 0.10);
        }

        .poc3-copilot-alert-head {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 8px;
        }

        .poc3-alert-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: linear-gradient(90deg, #FF3A5C 0%, #E41C53 100%) !important;
            color: #FFFFFF !important;
            border: 1px solid #C51338;
            border-radius: 999px;
            padding: 5px 11px;
            font-size: 0.74rem;
            font-weight: 820;
            letter-spacing: 0.04em;
            box-shadow: 0 5px 12px rgba(227, 29, 82, 0.23);
        }

        .poc3-alert-dot {
            width: 7px;
            height: 7px;
            border-radius: 999px;
            background: #FFFFFF;
            animation: poc3AlertPulse 1.2s infinite;
        }

        @keyframes poc3AlertPulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.52; transform: scale(0.7); }
        }

        .poc3-alert-title {
            color: #A11453;
            font-size: 0.92rem;
            font-weight: 820;
            margin: 0;
        }

        .poc3-alert-text {
            color: #4F618E;
            font-size: 0.84rem;
            line-height: 1.4;
            margin: 0;
        }

        .poc3-alert-meta {
            display: flex;
            flex-wrap: wrap;
            gap: 7px;
            margin-top: 9px;
        }

        .poc3-alert-chip {
            border-radius: 999px;
            padding: 4px 9px;
            font-size: 0.72rem;
            font-weight: 780;
            letter-spacing: 0.01em;
        }

        .poc3-alert-chip.blue {
            background: #EAF0FF !important;
            border: 1px solid #C7D5FF;
            color: #24439E;
        }

        .poc3-alert-chip.pink {
            background: #FFEAF3 !important;
            border: 1px solid #FFC9DE;
            color: #A11453;
        }

        .poc3-kpi-tile {
            background: #FFFFFF !important;
            border: 1px solid #E1E8F5;
            border-radius: 16px;
            padding: 14px 16px;
            min-height: 98px;
            box-shadow: 0 3px 10px rgba(3, 43, 246, 0.035);
        }

        .poc3-kpi-label {
            color: #5C6C95;
            font-size: 0.76rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }

        .poc3-kpi-value {
            color: #12317F;
            font-size: 1.75rem;
            font-weight: 840;
            line-height: 1;
            margin-top: 8px;
        }

        .poc3-kpi-delta {
            margin-top: 7px;
            font-size: 0.79rem;
            font-weight: 760;
            color: #107A73;
        }

        .poc3-kpi-delta.negative {
            color: #A11453;
        }

        .poc3-module-title {
            color: #0E2E87;
            font-size: 1.05rem;
            font-weight: 820;
            margin-bottom: 2px;
        }

        .poc3-module-sub {
            color: #5C6C95;
            font-size: 0.82rem;
            margin-bottom: 8px;
        }

        .poc3-chip-row {
            display: flex;
            flex-wrap: wrap;
            gap: 7px;
            margin-top: 6px;
        }

        .poc3-chip {
            border-radius: 999px;
            padding: 3px 9px;
            font-size: 0.74rem;
            font-weight: 800;
        }

        .poc3-chip.blue {
            background: #EAF0FF !important;
            border: 1px solid #CBD8FF;
            color: #284AA8;
        }

        .poc3-chip.pink {
            background: #FFEAF5 !important;
            border: 1px solid #FFC9E3;
            color: #9A0F52;
        }

        .poc3-account-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 10px;
            margin-bottom: 12px;
        }

        .poc3-accounts-dark {
            background: linear-gradient(180deg, #082A73 0%, #05225F 100%) !important;
            border: 1px solid rgba(255, 255, 255, 0.16);
            border-radius: 14px;
            padding: 16px;
        }

        .poc3-account-title {
            color: #FFFFFF !important;
            font-size: 1.08rem;
            font-weight: 820;
            margin: 0;
        }

        .poc3-account-sub {
            color: #C8D8FF !important;
            font-size: 0.82rem;
            margin: 0;
        }

        .poc3-list-row {
            background: #FFFFFF !important;
            border: 1px solid #E6EEFA !important;
            border-radius: 12px;
            padding: 12px 14px;
            margin-bottom: 10px;
            transition: all 0.2s ease;
        }

        .poc3-list-row:hover {
            border-color: #CBD8FF !important;
            box-shadow: 0 4px 12px rgba(3, 43, 246, 0.05);
        }

        .poc3-list-top {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 10px;
        }

        .poc3-list-name {
            color: #12317F !important;
            font-size: 0.92rem;
            font-weight: 780;
            margin: 0;
        }

        .poc3-list-cat {
            color: #6475A0 !important;
            font-size: 0.77rem;
            margin-top: 2px;
            margin-bottom: 0;
        }

        .poc3-list-right {
            text-align: right;
            min-width: 132px;
        }

        .poc3-list-value {
            color: #133381 !important;
            font-size: 0.9rem;
            font-weight: 780;
            margin: 0;
        }

        .poc3-list-perf {
            font-size: 0.79rem;
            font-weight: 760;
            margin-top: 1px;
            margin-bottom: 0;
        }

        .poc3-list-bar-track {
            width: 100%;
            height: 7px;
            border-radius: 999px;
            background: #EEF3FE !important;
            overflow: hidden;
            margin-top: 10px;
        }

        .poc3-list-bar-fill {
            height: 100%;
            border-radius: 999px;
        }

        .poc3-list-foot {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 6px;
            color: #66779F !important;
            font-size: 0.75rem;
            font-weight: 700;
        }

        div[data-testid="stPlotlyChart"],
        div[data-testid="stPlotlyChart"] > div {
            background: #FFFFFF !important;
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

    y_min = min(float(df["apports"].min()), float(df["valorisation"].min()))
    y_max = max(float(df["apports"].max()), float(df["valorisation"].max()))
    y_floor = y_min - max(180.0, (y_max - y_min) * 0.08)

    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=[y_floor] * len(df),
            mode="lines",
            line={"width": 0},
            hoverinfo="skip",
            showlegend=False,
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["valorisation"],
            mode="lines",
            name="Valorisation réelle",
            line={"color": "#032BF6", "width": 3.2, "shape": "spline"},
            fill="tonexty",
            fillcolor="rgba(3, 43, 246, 0.18)",
            hovertemplate="%{x|%d/%m/%Y}<br>Valorisation: %{y:,.0f} EUR<extra></extra>",
        )
    )

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

    fig.add_vrect(
        x0=df["date"].iloc[-24],
        x1=df["date"].iloc[-1],
        fillcolor="rgba(255, 1, 102, 0.08)",
        line_width=0,
    )

    fig.update_layout(
        height=470,
        margin={"l": 0, "r": 0, "t": 10, "b": 0},
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        hovermode="x unified",
        font={"color": "#40527E"},
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
        range=[y_floor, y_max + (y_max - y_min) * 0.06],
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
        font={"color": "#40527E"},
    )
    fig.update_yaxes(range=[0, 7.2], dtick=1, gridcolor="#F0F4FC", title=None, zeroline=False)
    fig.update_xaxes(title=None, showgrid=False)

    return fig


def _allocation_donut_figure() -> go.Figure:
    fig = go.Figure(
        data=[
            go.Pie(
                labels=["Fonds Euro", "Unités de compte"],
                values=[68, 32],
                hole=0.67,
                sort=False,
                marker={"colors": ["#032BF6", "#FF2B70"]},
                textinfo="percent",
                textfont={"size": 17, "color": "#FFFFFF"},
                domain={"x": [0.0, 0.78], "y": [0.0, 1.0]},
                hovertemplate="%{label}<br>%{value}%<extra></extra>",
            )
        ]
    )

    fig.update_layout(
        height=200,
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        showlegend=True,
        legend={
            "orientation": "v",
            "x": 0.82,
            "xanchor": "left",
            "y": 0.5,
            "yanchor": "middle",
            "font": {"size": 12, "color": "#40527E"},
        },
    )

    return fig


def _render_kpi_tile(label: str, value: str, delta: str, negative: bool = False) -> None:
    delta_cls = "poc3-kpi-delta negative" if negative else "poc3-kpi-delta"
    st.markdown(
        f"""
        <div class="poc3-kpi-tile">
            <div class="poc3-kpi-label">{label}</div>
            <div class="poc3-kpi-value">{value}</div>
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
        rows_html.append(
            f'<div class="poc3-list-row">'
            f'<div class="poc3-list-top">'
            f'<div>'
            f'<p class="poc3-list-name">{row["name"]}</p>'
            f'<p class="poc3-list-cat">{row["category"]}</p>'
            f'</div>'
            f'<div class="poc3-list-right">'
            f'<p class="poc3-list-value">{_fmt_eur(row["value"])}</p>'
            f'<p class="poc3-list-perf" style="color:{perf_color};">{perf_sign}{row["perf"]:.2f}%</p>'
            f'</div>'
            f'</div>'
            f'<div class="poc3-list-bar-track">'
            f'<div class="poc3-list-bar-fill" style="width:{row["weight"]}%;background:{row["color"]};"></div>'
            f'</div>'
            f'<div class="poc3-list-foot">'
            f'<span>Poids portefeuille: {row["weight"]:.2f}%</span>'
            f'<span>SRI {row["risk"]}/7</span>'
            f'</div>'
            f'</div>'
        )
    return "".join(rows_html)


def _render_top_bento() -> None:
    with st.container(border=True, key="poc3-copilot-card"):
        st.markdown('<p class="poc3-copilot-title">Co-pilote CNP Patrimoine</p>', unsafe_allow_html=True)
        st.markdown('<p class="poc3-copilot-subtitle">Alerte et recommandations</p>', unsafe_allow_html=True)
        st.markdown(
            '<p class="poc3-copilot-text">Retrouvez vos signaux critiques et arbitrages conseillés en temps réel.</p>',
            unsafe_allow_html=True,
        )
        st.markdown(
            (
                '<a href="?page=bot_diagnostic" target="_self" class="poc3-alert-link">'
                '<div class="poc3-copilot-alert-card">'
                '<div class="poc3-copilot-alert-head">'
                '<span class="poc3-alert-badge"><span class="poc3-alert-dot"></span>ALERTE ACTIVE</span>'
                '</div>'
                '<p class="poc3-alert-title">Ralentissement secteur automobile européen</p>'
                '<p class="poc3-alert-text">Impact potentiel sur vos UC CNP Actions Climat ESG. '
                'Ouvrir le diagnostic copilote pour lancer le protocole d\'arbitrage.</p>'
                '<div class="poc3-alert-meta">'
                '<span class="poc3-alert-chip blue">Priorité: Élevée</span>'
                '<span class="poc3-alert-chip pink">UC exposées: Actions Europe</span>'
                '</div>'
                '</div>'
                '</a>'
            ),
            unsafe_allow_html=True,
        )

    st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4, gap="small")
    with c1:
        _render_kpi_tile("Valorisation", "50 000 EUR", "+803 EUR")
    with c2:
        _render_kpi_tile("Performance mensuelle", "+2,4%", "Evolution positive")
    with c3:
        _render_kpi_tile("Risque observe", "5/7", "+2 niveaux vs cible", negative=True)
    with c4:
        _render_kpi_tile("Allocation UC", "32%", "-8 pts vs cible", negative=True)

    st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)

    chart_col, side_col = st.columns([2.18, 1.0], gap="medium")

    with chart_col:
        with st.container(border=True, key="poc3-perf-card"):
            st.markdown('<div class="poc3-module-title">Performance portefeuille</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="poc3-module-sub">Apports/Retraits cumulés vs valorisation réelle. Zone rose : choc récent.</div>',
                unsafe_allow_html=True,
            )
            st.plotly_chart(_performance_figure(_build_performance_df()), width="stretch", key="poc3_perf_bento")

    with side_col:
        with st.container(border=True, key="poc3-risk-card"):
            st.markdown('<div class="poc3-module-title">Niveau de risque (SRI)</div>', unsafe_allow_html=True)
            st.markdown('<div class="poc3-module-sub">Barres verticales avec seuil contractuel.</div>', unsafe_allow_html=True)
            st.plotly_chart(_risk_figure(), width="stretch", key="poc3_risk_bento")

        with st.container(border=True, key="poc3-allocation-card"):
            st.markdown('<div class="poc3-module-title">Répartition</div>', unsafe_allow_html=True)
            st.markdown('<div class="poc3-module-sub">Allocation globale du portefeuille.</div>', unsafe_allow_html=True)
            st.plotly_chart(_allocation_donut_figure(), width="stretch", key="poc3_alloc_donut")


def _render_bottom_accounts(df_accounts: pd.DataFrame) -> None:
    st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)
    rows_html = _render_account_rows(df_accounts)
    st.markdown(
        f"""
        <div class="poc3-accounts-dark">
            <div class="poc3-account-header">
                <div>
                    <p class="poc3-account-title">Détail compte par compte</p>
                    <p class="poc3-account-sub">Vue vérité des positions, exposition et performance.</p>
                </div>
                <div class="poc3-chip-row">
                    <span class="poc3-chip blue">6 lignes</span>
                    <span class="poc3-chip pink">Focus actions</span>
                </div>
            </div>
            {rows_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_poc3() -> None:
    _render_styles()

    st.markdown('<h1 class="poc3-title">Mon espace</h1>', unsafe_allow_html=True)
    st.markdown(
        '<div class="poc3-sub">Retrouvez la synthèse de vos contrats d\'assurance-vie et le suivi de vos arbitrages en temps réel</div>',
        unsafe_allow_html=True,
    )

    df_accounts = pd.DataFrame(ACCOUNTS)
    _render_top_bento()
    _render_bottom_accounts(df_accounts)


if __name__ == "__main__":
    show_poc3()
