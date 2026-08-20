import streamlit as st

def show_poc1():
    left, center, right = st.columns([1, 6, 1])
    with center:
        if st.button("Je souscris", key="subscribe_cta", use_container_width=True, type="primary"):
            st.session_state.current_page = "POC 2"
            st.query_params["page"] = "poc2"
            st.rerun()

    st.markdown("""
        <p class="sub-cta-text">
            Découvrez notre parcours de souscription sur-mesure en <b>moins de 3 minutes</b> avec profilage intelligent.
        </p>
        <div class="feature-row">
            <span class="feature-chip">Profil investisseur</span>
            <span class="feature-chip">Parcours 100% digital</span>
            <span class="feature-chip">Validation temps réel</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Zone Contenu GEO
    st.markdown('<h3 style="color:#002261;">Pourquoi choisir l\'Assurance-Vie CNP Patrimoine ?</h3>', unsafe_allow_html=True)
    st.info("Zone réservée au POC 1 (GEO) : Contenu explicatif optimisé pour le référencement IA.")