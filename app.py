import base64
import streamlit as st

# Import des vues modulaires
from views.poc1_geo import show_poc1
from views.poc2_underwriting import show_poc2
from views.poc3_advisor import show_poc3

st.set_page_config(
    page_title="CNP Assurances - Patrimoine & Épargne",
    page_icon="🛡️",
    layout="wide",
)

PAGE_LABELS = {
    "poc1": "POC 1",
    "poc2": "POC 2",
    "poc3": "POC 3",
}


def _query_param_value(value):
    if isinstance(value, (list, tuple)):
        return value[0] if value else None
    return value


def _normalize_page(value):
    raw = _query_param_value(value)
    if raw is None:
        return None

    page = str(raw).strip()
    if not page:
        return None

    lowered = page.lower().replace("+", " ")

    if lowered in PAGE_LABELS:
        return PAGE_LABELS[lowered]

    if lowered in {"poc 1", "poc 2", "poc 3"}:
        return lowered.upper()

    if page in PAGE_LABELS.values():
        return page

    return None


# Sync de la navigation via l'URL (Query Params)
if "page" in st.query_params:
    page_value = _normalize_page(st.query_params["page"])
    if page_value:
        st.session_state.current_page = page_value

if "current_page" not in st.session_state:
    st.session_state.current_page = "POC 1"


def get_svg_base64(file_path):
    try:
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    except Exception:
        return None


svg_b64 = get_svg_base64("images/logo-cnp.svg")

# --- CSS CHARTE STRICTE ---
st.markdown(
    """
    <style>
    :root {
        --cnp-blue: #002261;
        --cnp-rose: #D50065;
        --cnp-rose-hover: #B00053;
        --cnp-green: #02ADA5;
        --cnp-green-soft: #E6F7F6;
        --cnp-blue-soft: #EBF2FA;
        --cnp-pill-radius: 999px;
    }

    .stApp {
        background-color: #FFFFFF;
    }

    .block-container {
        padding-top: 1.6rem;
        padding-bottom: 2.2rem;
    }
    
    [data-testid="stSidebar"] {
        display: none;
    }
    
    /* Bannière supérieure */
    .banner-box {
        background-color: var(--cnp-blue);
        padding: 20px 30px;
        border-radius: 8px;
        color: white;
        margin-bottom: 25px;
        display: flex;
        align-items: center;
        gap: 20px;
    }
    
    .logo-square {
        background-color: #FFFFFF;
        width: 75px;
        height: 75px;
        min-width: 75px;
        border-radius: 6px;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 6px;
    }
    .logo-square img {
        width: 100%;
        height: 100%;
        object-fit: contain;
    }
    
    .banner-text h2 {
        color: #FFFFFF !important;
        margin: 0;
        font-size: 1.6rem;
        font-weight: 700;
    }
    .banner-text p {
        color: #F8F9FA;
        margin: 4px 0 0 0;
        font-size: 0.95rem;
    }
    
    /* NAVIGATION EN HTML PUR */
    .nav-container {
        display: flex;
        justify-content: center;
        gap: 15px;
        margin-bottom: 34px;
    }
    .nav-item {
        display: inline-block;
        padding: 10px 22px;
        border-radius: var(--cnp-pill-radius);
        text-decoration: none !important;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.2s ease;
        text-align: center;
    }
    .nav-item.active {
        background-color: var(--cnp-blue) !important;
        color: #FFFFFF !important;
        border: 2px solid var(--cnp-blue) !important;
    }
    .nav-item.inactive {
        background-color: #FFFFFF !important;
        color: var(--cnp-blue) !important;
        border: 2px solid var(--cnp-blue) !important;
    }
    .nav-item.inactive:hover {
        background-color: var(--cnp-blue) !important;
        color: #FFFFFF !important;
    }

    .nav-item.active,
    .nav-item.active:visited,
    .nav-item.active:hover,
    .nav-item.active:focus,
    .nav-item.active:active {
        color: #FFFFFF !important;
    }

    .nav-item.inactive:hover,
    .nav-item.inactive:hover:visited,
    .nav-item.inactive:focus,
    .nav-item.inactive:active {
        color: #FFFFFF !important;
        border-color: var(--cnp-blue) !important;
    }

    /* BOUTON ROSE EN HTML PUR */
    .btn-rose-container {
        text-align: center;
        margin: 15px 0 5px 0;
    }
    .btn-rose {
        display: inline-block;
        width: 60%;
        background-color: var(--cnp-rose) !important;
        color: #FFFFFF !important;
        padding: 12px 20px;
        border-radius: var(--cnp-pill-radius);
        text-decoration: none !important;
        font-weight: 600;
        font-size: 1rem;
        transition: background-color 0.2s ease;
    }
    .btn-rose:link,
    .btn-rose:visited,
    .btn-rose:hover,
    .btn-rose:active,
    .btn-rose:focus {
        color: #FFFFFF !important;
        text-decoration: none !important;
    }
    .btn-rose:hover,
    .btn-rose:active,
    .btn-rose:focus {
        background-color: var(--cnp-rose-hover) !important;
    }

    .sub-cta-text {
        text-align: center;
        color: var(--cnp-blue);
        font-size: 1rem;
        margin-top: 18px;
        margin-bottom: 22px;
    }

    .sub-cta-text b {
        color: var(--cnp-green);
    }

    .feature-chip {
        display: inline-block;
        background: var(--cnp-green-soft);
        border: 1px solid #9CDDD9;
        color: #027A74;
        padding: 4px 10px;
        border-radius: 999px;
        font-size: 0.85rem;
        font-weight: 700;
        margin: 0 8px 8px 0;
    }

    .feature-row {
        text-align: center;
        margin-top: 6px;
        margin-bottom: 28px;
    }

    div[data-testid="stFormSubmitButton"] > button {
        border-radius: var(--cnp-pill-radius) !important;
        font-weight: 600 !important;
    }

    div[data-testid="stInfo"] {
        border-left: 6px solid var(--cnp-green);
        background: var(--cnp-green-soft);
    }

    .stMarkdown a,
    .stMarkdown a:visited {
        color: var(--cnp-blue) !important;
    }

    .stMarkdown a.btn-rose,
    .stMarkdown a.btn-rose:visited,
    .stMarkdown a.btn-rose:hover,
    .stMarkdown a.btn-rose:active,
    .stMarkdown a.btn-rose:focus {
        color: #FFFFFF !important;
    }
    
    hr {
        display: none !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- BANNIÈRE HAUT DE PAGE ---
logo_html = (
    f'<div class="logo-square"><img src="data:image/svg+xml;base64,{svg_b64}"/></div>'
    if svg_b64
    else ""
)

st.markdown(
    f"""
    <div class="banner-box">
        {logo_html}
        <div class="banner-text">
            <h2>CNP Patrimoine & Épargne</h2>
            <p>L'assurance-vie nouvelle génération, guidée par l'intelligence artificielle</p>
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

# --- ONGLETS DE NAVIGATION CENTRÉS (BLEU) ---
p1_cls = "active" if st.session_state.current_page == "POC 1" else "inactive"
p2_cls = "active" if st.session_state.current_page == "POC 2" else "inactive"
p3_cls = "active" if st.session_state.current_page == "POC 3" else "inactive"

st.markdown(
    f"""
    <div class="nav-container">
        <a href="?page=poc1" target="_self" class="nav-item {p1_cls}">Vitrine & Offres (POC 1)</a>
        <a href="?page=poc2" target="_self" class="nav-item {p2_cls}">Souscription Dynamique (POC 2)</a>
        <a href="?page=poc3" target="_self" class="nav-item {p3_cls}">Conseiller IA & Alertes (POC 3)</a>
    </div>
""",
    unsafe_allow_html=True,
)

# --- ROUTEUR ---
if st.session_state.current_page == "POC 1":
    show_poc1()
elif st.session_state.current_page == "POC 2":
    show_poc2()
elif st.session_state.current_page == "POC 3":
    show_poc3()