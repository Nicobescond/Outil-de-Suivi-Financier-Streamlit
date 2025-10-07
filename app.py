import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Configuration de la page
st.set_page_config(
    page_title="Suivi Financier & Forecast",
    page_icon="📊",
    layout="wide"
)

# Styles CSS personnalisés
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .positive { color: #28a745; }
    .negative { color: #dc3545; }
    </style>
""", unsafe_allow_html=True)

# Titre principal
st.title("📊 Suivi Financier & Forecast 2025")

# Sidebar pour la navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Aller à", [
    "🏠 Dashboard",
    "🔷 Facturation Certification",
    "🔶 Facturation Autres",
    "💸 Charges & Coûts",
    "📈 Forecast",
    "📤 Import/Export"
])

# Initialisation des données en session state
if 'facturation_certif' not in st.session_state:
    st.session_state.facturation_certif = pd.DataFrame({
        'Date': pd.date_range(start='2025-01-01', periods=8, freq='M'),
        'Client': ['LIDL', 'Client A', 'LIDL', 'Client B', 'LIDL', 'Client C', 'Client A', 'LIDL'],
        'Référentiel': ['IFS FOOD', 'BRC FOOD', 'IFS FOOD', 'IFS LOGISTICS', 'IFS FOOD', 'BRC FOOD', 'IFS FOOD', 'IFS FOOD'],
        'Durée': [1.5, 2, 1, 1.5, 1.5, 2, 1, 1.5],
        'Montant_Facturation': [2000, 2200, 1350, 1800, 2000, 2400, 1350, 2000],
        'Frais_Mission': [250, 180, 200, 150, 220, 300, 180, 240],
        'Cout_Auditeur': [800, 900, 600, 750, 800, 1000, 600, 800],
        'Statut': ['Facturé'] * 5 + ['Prévu'] * 3
    })

if 'facturation_autres' not in st.session_state:
    st.session_state.facturation_autres = pd.DataFrame({
        'Date': pd.date_range(start='2025-01-01', periods=6, freq='M'),
        'Type': ['Formation', 'Conseil', 'Prêt auditeur', 'Formation', 'Conseil', 'Prêt auditeur'],
        'Client': ['ITM', 'Client D', 'KIWA', 'Client E', 'LIDL', 'SGS'],
        'Description': ['IFS Food', 'Mise en conformité', 'Audit 1 jour', 'BRC', 'Optimisation process', 'Audit 1.5 jours'],
        'Montant_Facturation': [1200, 1500, 750, 1000, 1800, 1125],
        'Frais_Mission': [100, 150, 80, 120, 200, 100],
        'Cout_Auditeur': [400, 600, 500, 350, 700, 750],
        'Statut': ['Facturé'] * 4 + ['Prévu'] * 2
    })

if 'charges_diverses' not in st.session_state:
    st.session_state.charges_diverses = pd.DataFrame({
        'Date': pd.date_range(start='2025-01-01', periods=8, freq='M'),
        'Catégorie': ['Frais généraux', 'Marketing', 'Informatique', 'Assurance', 'Frais généraux', 'Formation', 'Informatique', 'Marketing'],
        'Description': ['Loyer bureau', 'Publicité Google', 'Abonnement logiciel', 'RC Pro', 'Fournitures', 'Formation continue', 'Cloud', 'LinkedIn Ads'],
        'Montant': [800, 300, 150, 450, 200, 500, 180, 250],
        'Statut': ['Payé'] * 6 + ['Prévu'] * 2
    })

# Fonction pour calculer les marges
def calculer_marge(df, type_fact='certification'):
    df_copy = df.copy()
    df_copy['Marge_Brute'] = df_copy['Montant_Facturation'] - df_copy['Frais_Mission'] - df_copy['Cout_Auditeur']
    df_copy['Taux_Marge'] = (df_copy['Marge_Brute'] / df_copy['Montant_Facturation'] * 100).round(1)
    return df_copy

# =========================
# PAGE: DASHBOARD
# =========================
if page == "🏠 Dashboard":
    st.header("Tableau de Bord Principal")
    
    # Calculs des KPIs globaux
    ca_certif = st.session_state.facturation_certif['Montant_Facturation'].sum()
    ca_autres = st.session_state.facturation_autres['Montant_Facturation'].sum()
    ca_total = ca_certif + ca_autres
    
    frais_mission_certif = st.session_state.facturation_certif['Frais_Mission'].sum()
    frais_mission_autres = st.session_state.facturation_autres['Frais_Mission'].sum()
    frais_mission_total = frais_mission_certif + frais_mission_autres
    
    cout_auditeur_certif = st.session_state.facturation_certif['Cout_Auditeur'].sum()
    cout_auditeur_autres = st.session_state.facturation_autres['Cout_Auditeur'].sum()
    cout_auditeur_total = cout_auditeur_certif + cout_auditeur_autres
    
    charges_diverses_total = st.session_state.charges_diverses['Montant'].sum()
    
    charges_total = frais_mission_total + cout_auditeur_total + charges_diverses_total
    resultat = ca_total - charges_total
    
    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💰 CA Total", f"{ca_total:,.0f} €")
        st.caption(f"Certif: {ca_certif:,.0f} € | Autres: {ca_autres:,.0f} €")
    
    with col2:
        st.metric("💸 Charges Totales", f"{charges_total:,.0f} €")
        st.caption(f"Mission: {frais_mission_total:,.0f} € | Audit: {cout_auditeur_total:,.0f} €")
    
    with col3:
        st.metric("📊 Résultat", f"{resultat:,.0f} €",
                 delta_color="normal" if resultat > 0 else "inverse")
    
    with col4:
        marge = (resultat / ca_total * 100) if ca_total > 0 else 0
        st.metric("📈 Marge Nette", f"{marge:.1f}%")
    
    st.divider()
    
    # Graphiques principaux
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("CA: Certification vs Autres")
        
        fig = go.Figure(data=[
            go.Bar(name='Certification', x=['Facturé', 'Prévu'], 
                   y=[
                       st.session_state.facturation_certif[st.session_state.facturation_certif['Statut']=='Facturé']['Montant_Facturation'].sum(),
                       st.session_state.facturation_certif[st.session_state.facturation_certif['Statut']=='Prévu']['Montant_Facturation'].sum()
                   ],
                   marker_color='#3498DB'),
            go.Bar(name='Autres', x=['Facturé', 'Prévu'],
                   y=[
                       st.session_state.facturation_autres[st.session_state.facturation_autres['Statut']=='Facturé']['Montant_Facturation'].sum(),
                       st.session_state.facturation_autres[st.session_state.facturation_autres['Statut']=='Prévu']['Montant_Facturation'].sum()
                   ],
                   marker_color='#E67E22')
        ])
        fig.update_layout(barmode='group', height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Répartition des Charges")
        
        charges_data = pd.DataFrame({
            'Type': ['Frais Mission', 'Coût Auditeurs', 'Charges Diverses'],
            'Montant': [frais_mission_total, cout_auditeur_total, charges_diverses_total]
        })
        
        fig = px.pie(charges_data, values='Montant', names='Type',
                    color_discrete_sequence=['#E74C3C', '#9B59B6', '#95A5A6'],
                    hole=0.4)
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    # Evolution mensuelle combinée
    st.subheader("Evolution Mensuelle: CA et Marges")
    
    # Agrégation mensuelle
    certif_monthly = st.session_state.facturation_certif.copy()
    certif_monthly['Mois'] = pd.to_datetime(certif_monthly['Date']).dt.to_period('M')
    certif_agg = certif_monthly.groupby('Mois').agg({
        'Montant_Facturation': 'sum',
        'Frais_Mission': 'sum',
        'Cout_Auditeur': 'sum'
    }).reset_index()
    certif_agg['Marge'] = certif_agg['Montant_Facturation'] - certif_agg['Frais_Mission'] - certif_agg['Cout_Auditeur']
    certif_agg['Mois'] = certif_agg['Mois'].astype(str)
    
    autres_monthly = st.session_state.facturation_autres.copy()
    autres_monthly['Mois'] = pd.to_datetime(autres_monthly['Date']).dt.to_period('M')
    autres_agg = autres_monthly.groupby('Mois').agg({
        'Montant_Facturation': 'sum',
        'Frais_Mission': 'sum',
        'Cout_Auditeur': 'sum'
    }).reset_index()
    autres_agg['Marge'] = autres_agg['Montant_Facturation'] - autres_agg['Frais_Mission'] - autres_agg['Cout_Auditeur']
    autres_agg['Mois'] = autres_agg['Mois'].astype(str)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=certif_agg['Mois'], y=certif_agg['Montant_Facturation'],
                        name='CA Certification', marker_color='#3498DB'))
    fig.add_trace(go.Bar(x=autres_agg['Mois'], y=autres_agg['Montant_Facturation'],
                        name='CA Autres', marker_color='#E67E22'))
    fig.add_trace(go.Scatter(x=certif_agg['Mois'], y=certif_agg['Marge'],
                            name='Marge Certification', mode='lines+markers',
                            line=dict(color='#27AE60', width=3)))
    
    fig.update_layout(
        xaxis_title="Mois",
        yaxis_title="Montant (€)",
        hovermode='x unified',
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

# =========================
# PAGE: FACTURATION CERTIFICATION
# =========================
elif page == "🔷 Facturation Certification":
    st.header("Facturation Certification")
    
    tab1, tab2, tab3 = st.tabs(["📊 Vue d'ensemble", "➕ Ajouter", "✏️ Modifier/Supprimer"])
    
    with tab1:
        # Calcul des marges
        df_with_marge = calculer_marge(st.session_state.facturation_certif, 'certification')
        
        # KPIs
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("CA Total", f"{df_with_marge['Montant_Facturation'].sum():,.0f} €")
        with col2:
            st.metric("Frais Mission", f"{df_with_marge['Frais_Mission'].sum():,.0f} €")
        with col3:
            st.metric("Coût Auditeurs", f"{df_with_marge['Cout_Auditeur'].sum():,.0f} €")
        with col4:
            marge_brute = df_with_marge['Marge_Brute'].sum()
            st.metric("Marge Brute", f"{marge_brute:,.0f} €")
        
        # Filtres
        col1, col2, col3 = st.columns(3)
        with col1:
            clients = ['Tous'] + list(df_with_marge['Client'].unique())
            client_filter = st.selectbox("Client", clients, key="certif_client")
        with col2:
            refs = ['Tous'] + list(df_with_marge['Référentiel'].unique())
            ref_filter = st.selectbox("Référentiel", refs, key="certif_ref")
        with col3:
            statuts = ['Tous', 'Facturé', 'Prévu']
            statut_filter = st.selectbox("Statut", statuts, key="certif_statut")
        
        # Application des filtres
        filtered_data = df_with_marge.copy()
        if client_filter != 'Tous':
            filtered_data = filtered_data[filtered_data['Client'] == client_filter]
        if ref_filter != 'Tous':
            filtered_data = filtered_data[filtered_data['Référentiel'] == ref_filter]
        if statut_filter != 'Tous':
            filtered_data = filtered_data[filtered_data['Statut'] == statut_filter]
        
        # Affichage du tableau avec formatage
        display_df = filtered_data.copy()
        display_df['Date'] = display_df['Date'].dt.strftime('%d/%m/%Y')
        display_df['Montant_Facturation'] = display_df['Montant_Facturation'].apply(lambda x: f"{x:,.0f} €")
        display_df['Frais_Mission'] = display_df['Frais_Mission'].apply(lambda x: f"{x:,.0f} €")
        display_df['Cout_Auditeur'] = display_df['Cout_Auditeur'].apply(lambda x: f"{x:,.0f} €")
        display_df['Marge_Brute'] = display_df['Marge_Brute'].apply(lambda x: f"{x:,.0f} €")
        display_df['Taux_Marge'] = display_df['Taux_Marge'].apply(lambda x: f"{x:.1f}%")
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # Graphique de marge par client
        st.subheader("Analyse de Marge par Client")
        marge_client = filtered_data.groupby('Client').agg({
            'Montant_Facturation': 'sum',
            'Marge_Brute': 'sum'
        }).reset_index()
        marge_client['Taux_Marge'] = (marge_client['Marge_Brute'] / marge_client['Montant_Facturation'] * 100).round(1)
        
        fig = px.bar(marge_client, x='Client', y=['Montant_Facturation', 'Marge_Brute'],
                    barmode='group',
                    labels={'value': 'Montant (€)', 'variable': 'Type'},
                    color_discrete_map={'Montant_Facturation': '#3498DB', 'Marge_Brute': '#27AE60'})
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Ajouter une nouvelle facturation certification")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            new_date = st.date_input("Date", datetime.now(), key="certif_new_date")
            new_client = st.text_input("Client", key="certif_new_client")
            new_ref = st.selectbox("Référentiel", 
                ["IFS FOOD", "BRC FOOD", "IFS LOGISTICS", "IFS BROKER", "IFS PROGRESS"],
                key="certif_new_ref")
        
        with col2:
            new_duree = st.number_input("Durée (jours)", min_value=0.5, max_value=5.0, step=0.5, value=1.0, key="certif_new_duree")
            new_montant = st.number_input("Montant Facturation (€)", min_value=0.0, step=50.0, key="certif_new_montant")
            new_frais = st.number_input("Frais Mission (€)", min_value=0.0, step=10.0, key="certif_new_frais")
        
        with col3:
            new_cout_audit = st.number_input("Coût Auditeur (€)", min_value=0.0, step=50.0, key="certif_new_cout")
            new_statut = st.selectbox("Statut", ["Facturé", "Prévu", "Devis"], key="certif_new_statut")
        
        # Calcul automatique de la marge
        marge_calc = new_montant - new_frais - new_cout_audit
        taux_marge_calc = (marge_calc / new_montant * 100) if new_montant > 0 else 0
        
        st.info(f"💡 Marge prévisionnelle: **{marge_calc:,.0f} €** ({taux_marge_calc:.1f}%)")
        
        if st.button("➕ Ajouter la facturation certification", key="add_certif"):
            new_row = pd.DataFrame({
                'Date': [pd.to_datetime(new_date)],
                'Client': [new_client],
                'Référentiel': [new_ref],
                'Durée': [new_duree],
                'Montant_Facturation': [new_montant],
                'Frais_Mission': [new_frais],
                'Cout_Auditeur': [new_cout_audit],
                'Statut': [new_statut]
            })
            st.session_state.facturation_certif = pd.concat(
                [st.session_state.facturation_certif, new_row], ignore_index=True)
            st.success("✅ Facturation ajoutée avec succès!")
            st.rerun()
    
    with tab3:
        st.subheader("Modifier ou supprimer une facturation")
        
        if len(st.session_state.facturation_certif) > 0:
            df_display = st.session_state.facturation_certif.copy()
            df_display['Date_str'] = df_display['Date'].dt.strftime('%d/%m/%Y')
            df_display['Label'] = df_display['Date_str'] + " - " + df_display['Client'] + " - " + df_display['Référentiel']
            
            selected_row = st.selectbox("Sélectionner une ligne", df_display['Label'].tolist(), key="certif_select")
            
            if selected_row:
                idx = df_display[df_display['Label'] == selected_row].index[0]
                row_data = st.session_state.facturation_certif.loc[idx]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Données actuelles:**")
                    st.write(f"Client: {row_data['Client']}")
                    st.write(f"Montant: {row_data['Montant_Facturation']:,.0f} €")
                    st.write(f"Frais Mission: {row_data['Frais_Mission']:,.0f} €")
                    st.write(f"Coût Auditeur: {row_data['Cout_Auditeur']:,.0f} €")
                
                with col2:
                    if st.button("🗑️ Supprimer cette ligne", key="del_certif"):
                        st.session_state.facturation_certif = st.session_state.facturation_certif.drop(idx).reset_index(drop=True)
                        st.success("✅ Ligne supprimée!")
                        st.rerun()

# =========================
# PAGE: FACTURATION AUTRES
# =========================
elif page == "🔶 Facturation Autres":
    st.header("Facturation Autres Prestations")
    
    tab1, tab2, tab3 = st.tabs(["📊 Vue d'ensemble", "➕ Ajouter", "✏️ Modifier/Supprimer"])
    
    with tab1:
        # Calcul des marges
        df_with_marge = calculer_marge(st.session_state.facturation_autres, 'autres')
        
        # KPIs
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("CA Total", f"{df_with_marge['Montant_Facturation'].sum():,.0f} €")
        with col2:
            st.metric("Frais Mission", f"{df_with_marge['Frais_Mission'].sum():,.0f} €")
        with col3:
            st.metric("Coût Auditeurs", f"{df_with_marge['Cout_Auditeur'].sum():,.0f} €")
        with col4:
            marge_brute = df_with_marge['Marge_Brute'].sum()
            st.metric("Marge Brute", f"{marge_brute:,.0f} €")
        
        # Filtres
        col1, col2 = st.columns(2)
        with col1:
            types = ['Tous'] + list(df_with_marge['Type'].unique())
            type_filter = st.selectbox("Type", types, key="autres_type")
        with col2:
            statuts = ['Tous', 'Facturé', 'Prévu']
            statut_filter = st.selectbox("Statut", statuts, key="autres_statut")
        
        # Application des filtres
        filtered_data = df_with_marge.copy()
        if type_filter != 'Tous':
            filtered_data = filtered_data[filtered_data['Type'] == type_filter]
        if statut_filter != 'Tous':
            filtered_data = filtered_data[filtered_data['Statut'] == statut_filter]
        
        # Affichage
        display_df = filtered_data.copy()
        display_df['Date'] = display_df['Date'].dt.strftime('%d/%m/%Y')
        display_df['Montant_Facturation'] = display_df['Montant_Facturation'].apply(lambda x: f"{x:,.0f} €")
        display_df['Frais_Mission'] = display_df['Frais_Mission'].apply(lambda x: f"{x:,.0f} €")
        display_df['Cout_Auditeur'] = display_df['Cout_Auditeur'].apply(lambda x: f"{x:,.0f} €")
        display_df['Marge_Brute'] = display_df['Marge_Brute'].apply(lambda x: f"{x:,.0f} €")
        display_df['Taux_Marge'] = display_df['Taux_Marge'].apply(lambda x: f"{x:.1f}%")
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # Graphique par type
        st.subheader("Répartition par Type de Prestation")
        type_agg = filtered_data.groupby('Type').agg({
            'Montant_Facturation': 'sum',
            'Marge_Brute': 'sum'
        }).reset_index()
        
        fig = px.bar(type_agg, x='Type', y=['Montant_Facturation', 'Marge_Brute'],
                    barmode='group',
                    color_discrete_map={'Montant_Facturation': '#E67E22', 'Marge_Brute': '#27AE60'})
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Ajouter une nouvelle facturation autre")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            new_date = st.date_input("Date", datetime.now(), key="autres_new_date")
            new_type = st.selectbox("Type", 
                ["Formation", "Conseil", "Prêt auditeur", "Traduction", "Autre"],
                key="autres_new_type")
            new_client = st.text_input("Client", key="autres_new_client")
        
        with col2:
            new_description = st.text_area("Description", key="autres_new_desc")
            new_montant = st.number_input("Montant Facturation (€)", min_value=0.0, step=50.0, key="autres_new_montant")
        
        with col3:
            new_frais = st.number_input("Frais Mission (€)", min_value=0.0, step=10.0, key="autres_new_frais")
            new_cout_audit = st.number_input("Coût Auditeur/Prestataire (€)", min_value=0.0, step=50.0, key="autres_new_cout")
            new_statut = st.selectbox("Statut", ["Facturé", "Prévu", "Devis"], key="autres_new_statut")
        
        # Calcul automatique de la marge
        marge_calc = new_montant - new_frais - new_cout_audit
        taux_marge_calc = (marge_calc / new_montant * 100) if new_montant > 0 else 0
        
        st.info(f"💡 Marge prévisionnelle: **{marge_calc:,.0f} €** ({taux_marge_calc:.1f}%)")
        
        if st.button("➕ Ajouter la facturation autre", key="add_autres"):
            new_row = pd.DataFrame({
                'Date': [pd.to_datetime(new_date)],
                'Type': [new_type],
                'Client': [new_client],
                'Description': [new_description],
                'Montant_Facturation': [new_montant],
                'Frais_Mission': [new_frais],
                'Cout_Auditeur': [new_cout_audit],
                'Statut': [new_statut]
            })
            st.session_state.facturation_autres = pd.concat(
                [st.session_state.facturation_autres, new_row], ignore_index=True)
            st.success("✅ Facturation ajoutée avec succès!")
            st.rerun()
    
    with tab3:
        st.subheader("Modifier ou supprimer une facturation")
        
        if len(st.session_state.facturation_autres) > 0:
            df_display = st.session_state.facturation_autres.copy()
            df_display['Date_str'] = df_display['Date'].dt.strftime('%d/%m/%Y')
            df_display['Label'] = df_display['Date_str'] + " - " + df_display['Type'] + " - " + df_display['Client']
            
            selected_row = st.selectbox("Sélectionner une ligne", df_display['Label'].tolist(), key="autres_select")
            
            if selected_row:
                idx = df_display[df_display['Label'] == selected_row].index[0]
                row_data = st.session_state.facturation_autres.loc[idx]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Données actuelles:**")
                    st.write(f"Type: {row_data['Type']}")
                    st.write(f"Client: {row_data['Client']}")
                    st.write(f"Montant: {row_data['Montant_Facturation']:,.0f} €")
                
                with col2:
                    if st.button("🗑️ Supprimer cette ligne", key="del_autres"):
                        st.session_state.facturation_autres = st.session_state.facturation_autres.drop(idx).reset_index(drop=True)
                        st.success("✅ Ligne supprimée!")
                        st.rerun()

# =========================
# PAGE: CHARGES & COÛTS
# =========================
elif page == "💸 Charges & Coûts":
    st.header("Charges & Coûts")
    
    tab1, tab2 = st.tabs(["📊 Vue d'ensemble", "➕ Ajouter une charge"])
    
    with tab1:
        # Calcul des totaux
        frais_mission_total = (st.session_state.facturation_certif['Frais_Mission'].sum() + 
                              st.session_state.facturation_autres['Frais_Mission'].sum())
        cout_auditeur_total = (st.session_state.facturation_certif['Cout_Auditeur'].sum() + 
                              st.session_state.facturation_autres['Cout_Auditeur'].sum())
        charges_diverses_total = st.session_state.charges_diverses['Montant'].sum()
        total_charges = frais_mission_total + cout_auditeur_total + charges_diverses_total
        
        # KPIs
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("🚗 Frais Mission", f"{frais_mission_total:,.0f} €")
        with col2:
            st.metric("👤 Coût Auditeurs", f"{cout_auditeur_total:,.0f} €")
        with col3:
            st.metric("📋 Charges Diverses", f"{charges_diverses_total:,.0f} €")
        with col4:
            st.metric("💰 Total Charges", f"{total_charges:,.0f} €")
        
        st.divider()
        
        # Graphiques
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Répartition des Charges")
            charges_repartition = pd.DataFrame({
                'Type': ['Frais Mission', 'Coût Auditeurs', 'Charges Diverses'],
                'Montant': [frais_mission_total, cout_auditeur_total, charges_diverses_total]
            })
            fig = px.pie(charges_repartition, values='Montant', names='Type',
                        color_discrete_sequence=['#E74C3C', '#9B59B6', '#95A5A6'],
                        hole=0.4)
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Charges Diverses par Catégorie")
            charges_cat = st.session_state.charges_diverses.groupby('Catégorie')['Montant'].sum().reset_index()
            fig = px.bar(charges_cat, x='Catégorie', y='Montant',
                        color='Montant', color_continuous_scale='Reds')
            fig.update_layout(height=350, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        # Détail des frais de mission
        st.subheader("📊 Détail des Frais de Mission")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Certification**")
            frais_certif = st.session_state.facturation_certif[['Date', 'Client', 'Frais_Mission']].copy()
            frais_certif['Date'] = frais_certif['Date'].dt.strftime('%d/%m/%Y')
            frais_certif['Frais_Mission'] = frais_certif['Frais_Mission'].apply(lambda x: f"{x:,.0f} €")
            st.dataframe(frais_certif, use_container_width=True, hide_index=True, height=250)
        
        with col2:
            st.write("**Autres Prestations**")
            frais_autres = st.session_state.facturation_autres[['Date', 'Client', 'Frais_Mission']].copy()
            frais_autres['Date'] = frais_autres['Date'].dt.strftime('%d/%m/%Y')
            frais_autres['Frais_Mission'] = frais_autres['Frais_Mission'].apply(lambda x: f"{x:,.0f} €")
            st.dataframe(frais_autres, use_container_width=True, hide_index=True, height=250)
        
        # Détail des coûts auditeurs
        st.subheader("👥 Détail des Coûts Auditeurs")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Certification**")
            cout_certif = st.session_state.facturation_certif[['Date', 'Client', 'Cout_Auditeur']].copy()
            cout_certif['Date'] = cout_certif['Date'].dt.strftime('%d/%m/%Y')
            cout_certif['Cout_Auditeur'] = cout_certif['Cout_Auditeur'].apply(lambda x: f"{x:,.0f} €")
            st.dataframe(cout_certif, use_container_width=True, hide_index=True, height=250)
        
        with col2:
            st.write("**Autres Prestations**")
            cout_autres = st.session_state.facturation_autres[['Date', 'Client', 'Cout_Auditeur']].copy()
            cout_autres['Date'] = cout_autres['Date'].dt.strftime('%d/%m/%Y')
            cout_autres['Cout_Auditeur'] = cout_autres['Cout_Auditeur'].apply(lambda x: f"{x:,.0f} €")
            st.dataframe(cout_autres, use_container_width=True, hide_index=True, height=250)
        
        # Charges diverses détaillées
        st.subheader("📋 Charges Diverses Détaillées")
        charges_display = st.session_state.charges_diverses.copy()
        charges_display['Date'] = charges_display['Date'].dt.strftime('%d/%m/%Y')
        charges_display['Montant'] = charges_display['Montant'].apply(lambda x: f"{x:,.0f} €")
        st.dataframe(charges_display, use_container_width=True, hide_index=True)
    
    with tab2:
        st.subheader("Ajouter une charge diverse")
        
        col1, col2 = st.columns(2)
        with col1:
            new_date = st.date_input("Date", datetime.now(), key="charge_new_date")
            new_categorie = st.selectbox("Catégorie", 
                ["Frais généraux", "Marketing", "Informatique", "Assurance", "Formation", "Autre"],
                key="charge_new_cat")
            new_description = st.text_input("Description", key="charge_new_desc")
        
        with col2:
            new_montant = st.number_input("Montant (€)", min_value=0.0, step=10.0, key="charge_new_montant")
            new_statut = st.selectbox("Statut", ["Payé", "À payer", "Prévu"], key="charge_new_statut")
        
        if st.button("➕ Ajouter la charge", key="add_charge"):
            new_row = pd.DataFrame({
                'Date': [pd.to_datetime(new_date)],
                'Catégorie': [new_categorie],
                'Description': [new_description],
                'Montant': [new_montant],
                'Statut': [new_statut]
            })
            st.session_state.charges_diverses = pd.concat(
                [st.session_state.charges_diverses, new_row], ignore_index=True)
            st.success("✅ Charge ajoutée avec succès!")
            st.rerun()

# =========================
# PAGE: FORECAST
# =========================
elif page == "📈 Forecast":
    st.header("Prévisions Financières avec Ajustements")
    
    # Paramètres du forecast
    col1, col2, col3 = st.columns(3)
    
    with col1:
        nb_mois = st.slider("Nombre de mois à prévoir", 1, 12, 6)
    with col2:
        croissance_ca_certif = st.slider("Croissance CA Certif (%/mois)", -10.0, 20.0, 3.0, 0.5)
        croissance_ca_autres = st.slider("Croissance CA Autres (%/mois)", -10.0, 20.0, 2.0, 0.5)
    with col3:
        croissance_charges = st.slider("Croissance Charges (%/mois)", -10.0, 20.0, 1.5, 0.5)
    
    st.divider()
    
    # Calcul des moyennes actuelles
    ca_certif_moy = st.session_state.facturation_certif.groupby(
        pd.Grouper(key='Date', freq='M'))['Montant_Facturation'].sum().mean()
    frais_certif_moy = st.session_state.facturation_certif.groupby(
        pd.Grouper(key='Date', freq='M'))['Frais_Mission'].sum().mean()
    cout_certif_moy = st.session_state.facturation_certif.groupby(
        pd.Grouper(key='Date', freq='M'))['Cout_Auditeur'].sum().mean()
    
    ca_autres_moy = st.session_state.facturation_autres.groupby(
        pd.Grouper(key='Date', freq='M'))['Montant_Facturation'].sum().mean()
    frais_autres_moy = st.session_state.facturation_autres.groupby(
        pd.Grouper(key='Date', freq='M'))['Frais_Mission'].sum().mean()
    cout_autres_moy = st.session_state.facturation_autres.groupby(
        pd.Grouper(key='Date', freq='M'))['Cout_Auditeur'].sum().mean()
    
    charges_diverses_moy = st.session_state.charges_diverses.groupby(
        pd.Grouper(key='Date', freq='M'))['Montant'].sum().mean()
    
    # Section d'ajustement des prévisions
    st.subheader("🎯 Ajuster les prévisions mensuelles")
    st.write("Modifiez les valeurs vides ou ajustez les prévisions pour chaque mois")
    
    # Génération des dates forecast
    derniere_date = max(st.session_state.facturation_certif['Date'].max(),
                       st.session_state.facturation_autres['Date'].max())
    dates_forecast = pd.date_range(
        start=derniere_date + timedelta(days=30), 
        periods=nb_mois, 
        freq='M'
    )
    
    # Création du dataframe de forecast éditable
    if 'forecast_data' not in st.session_state or len(st.session_state.forecast_data) != nb_mois:
        forecast_initial = []
        for i, date in enumerate(dates_forecast):
            ca_certif_prev = ca_certif_moy * (1 + croissance_ca_certif/100) ** (i+1)
            ca_autres_prev = ca_autres_moy * (1 + croissance_ca_autres/100) ** (i+1)
            frais_prev = (frais_certif_moy + frais_autres_moy) * (1 + croissance_charges/100) ** (i+1)
            cout_prev = (cout_certif_moy + cout_autres_moy) * (1 + croissance_charges/100) ** (i+1)
            charges_prev = charges_diverses_moy * (1 + croissance_charges/100) ** (i+1)
            
            forecast_initial.append({
                'Mois': date.strftime('%B %Y'),
                'CA_Certification': round(ca_certif_prev, 0),
                'CA_Autres': round(ca_autres_prev, 0),
                'Frais_Mission': round(frais_prev, 0),
                'Cout_Auditeurs': round(cout_prev, 0),
                'Charges_Diverses': round(charges_prev, 0)
            })
        
        st.session_state.forecast_data = pd.DataFrame(forecast_initial)
    
    # Editeur de données
    st.write("**💡 Astuce**: Double-cliquez sur une cellule pour modifier les valeurs")
    
    edited_forecast = st.data_editor(
        st.session_state.forecast_data,
        use_container_width=True,
        hide_index=True,
        num_rows="fixed",
        column_config={
            "Mois": st.column_config.TextColumn("Mois", disabled=True),
            "CA_Certification": st.column_config.NumberColumn(
                "CA Certification (€)",
                min_value=0,
                format="%.0f €"
            ),
            "CA_Autres": st.column_config.NumberColumn(
                "CA Autres (€)",
                min_value=0,
                format="%.0f €"
            ),
            "Frais_Mission": st.column_config.NumberColumn(
                "Frais Mission (€)",
                min_value=0,
                format="%.0f €"
            ),
            "Cout_Auditeurs": st.column_config.NumberColumn(
                "Coût Auditeurs (€)",
                min_value=0,
                format="%.0f €"
            ),
            "Charges_Diverses": st.column_config.NumberColumn(
                "Charges Diverses (€)",
                min_value=0,
                format="%.0f €"
            )
        }
    )
    
    # Mise à jour du forecast
    st.session_state.forecast_data = edited_forecast
    
    # Calculs des résultats
    edited_forecast['CA_Total'] = edited_forecast['CA_Certification'] + edited_forecast['CA_Autres']
    edited_forecast['Charges_Totales'] = (edited_forecast['Frais_Mission'] + 
                                         edited_forecast['Cout_Auditeurs'] + 
                                         edited_forecast['Charges_Diverses'])
    edited_forecast['Resultat'] = edited_forecast['CA_Total'] - edited_forecast['Charges_Totales']
    edited_forecast['Marge_Pct'] = (edited_forecast['Resultat'] / edited_forecast['CA_Total'] * 100).round(1)
    
    st.divider()
    
    # Graphique de forecast
    st.subheader("📊 Visualisation des Prévisions")
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=edited_forecast['Mois'],
        y=edited_forecast['CA_Certification'],
        name='CA Certification',
        marker_color='#3498DB'
    ))
    
    fig.add_trace(go.Bar(
        x=edited_forecast['Mois'],
        y=edited_forecast['CA_Autres'],
        name='CA Autres',
        marker_color='#E67E22'
    ))
    
    fig.add_trace(go.Scatter(
        x=edited_forecast['Mois'],
        y=edited_forecast['Charges_Totales'],
        name='Charges Totales',
        mode='lines+markers',
        line=dict(color='#E74C3C', width=3),
        marker=dict(size=10)
    ))
    
    fig.add_trace(go.Scatter(
        x=edited_forecast['Mois'],
        y=edited_forecast['Resultat'],
        name='Résultat',
        mode='lines+markers',
        line=dict(color='#27AE60', width=3, dash='dash'),
        marker=dict(size=10)
    ))
    
    fig.update_layout(
        xaxis_title="Mois",
        yaxis_title="Montant (€)",
        hovermode='x unified',
        height=500,
        barmode='stack'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # KPIs du forecast
    st.subheader("📈 Résumé des Prévisions")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_ca = edited_forecast['CA_Total'].sum()
        st.metric("CA Total Prévu", f"{total_ca:,.0f} €")
    
    with col2:
        total_charges = edited_forecast['Charges_Totales'].sum()
        st.metric("Charges Totales Prévues", f"{total_charges:,.0f} €")
    
    with col3:
        total_resultat = edited_forecast['Resultat'].sum()
        st.metric("Résultat Prévu", f"{total_resultat:,.0f} €",
                 delta_color="normal" if total_resultat > 0 else "inverse")
    
    with col4:
        marge_moy = (total_resultat / total_ca * 100) if total_ca > 0 else 0
        st.metric("Marge Moyenne", f"{marge_moy:.1f}%")
    
    # Tableau détaillé des résultats
    st.subheader("📋 Détail des Prévisions avec Résultats")
    
    result_display = edited_forecast.copy()
    for col in ['CA_Certification', 'CA_Autres', 'CA_Total', 'Frais_Mission', 
                'Cout_Auditeurs', 'Charges_Diverses', 'Charges_Totales', 'Resultat']:
        result_display[col] = result_display[col].apply(lambda x: f"{x:,.0f} €")
    result_display['Marge_Pct'] = result_display['Marge_Pct'].apply(lambda x: f"{x:.1f}%")
    
    st.dataframe(result_display, use_container_width=True, hide_index=True)
    
    # Bouton pour réinitialiser le forecast
    if st.button("🔄 Réinitialiser les prévisions avec les nouveaux paramètres"):
        del st.session_state.forecast_data
        st.rerun()

# =========================
# PAGE: IMPORT/EXPORT
# =========================
elif page == "📤 Import/Export":
    st.header("Import/Export de Données")
    
    tab1, tab2 = st.tabs(["📥 Import", "📤 Export"])
    
    with tab1:
        st.subheader("Importer des données depuis Excel")
        
        st.info("""
        💡 **Import automatique intelligent**
        
        L'application détecte automatiquement les colonnes de vos feuilles Excel :
        - **Facturation-Certif** : Import automatique des facturations certification
        - **Facturation-Autres** : Import automatique des autres prestations
        - **FRAIS DIVERS** : Import automatique des charges diverses
        
        Téléchargez simplement votre fichier !
        """)
        
        uploaded_file = st.file_uploader(
            "Choisir un fichier Excel", 
            type=['xlsx', 'xls', 'xlsm']
        )
        
        if uploaded_file:
            try:
                # Lecture du fichier
                excel_file = pd.ExcelFile(uploaded_file)
                st.success(f"✅ Fichier chargé: {uploaded_file.name}")
                st.write("**Feuilles disponibles:**", ", ".join(excel_file.sheet_names))
                
                # Fonction pour détecter et mapper les colonnes automatiquement
                def detect_column(df_columns, possible_names):
                    """Détecte une colonne en cherchant des noms possibles"""
                    df_columns_lower = [str(col).lower().strip() for col in df_columns]
                    for name in possible_names:
                        name_lower = name.lower().strip()
                        for i, col in enumerate(df_columns_lower):
                            if name_lower in col or col in name_lower:
                                return df_columns[i]
                    return None
                
                # Fonction pour nettoyer et convertir les données
                def clean_data(df, start_row=2):
                    """Nettoie les données en supprimant les lignes vides"""
                    if start_row > 0:
                        df = df.iloc[start_row:]
                    df = df.dropna(how='all')
                    return df.reset_index(drop=True)
                
                # ========================================
                # IMPORT AUTOMATIQUE FACTURATION CERTIFICATION
                # ========================================
                if 'Facturation-Certif' in excel_file.sheet_names:
                    with st.expander("🔷 Facturation Certification - Import Automatique", expanded=True):
                        try:
                            df_certif_raw = pd.read_excel(excel_file, sheet_name='Facturation-Certif')
                            
                            st.write(f"📊 Aperçu des données brutes ({len(df_certif_raw)} lignes):")
                            st.dataframe(df_certif_raw.head(5), use_container_width=True)
                            
                            # Paramètres d'import
                            col1, col2 = st.columns(2)
                            with col1:
                                start_row_certif = st.number_input(
                                    "Ligne de départ (0 = première ligne)", 
                                    min_value=0, 
                                    max_value=max(0, len(df_certif_raw)-1), 
                                    value=2,
                                    key="auto_certif_start"
                                )
                            with col2:
                                replace_certif = st.checkbox(
                                    "Remplacer les données existantes", 
                                    value=True,
                                    key="auto_certif_replace"
                                )
                            
                            # Détection automatique des colonnes
                            df_certif = clean_data(df_certif_raw, start_row_certif)
                            columns = df_certif.columns.tolist()
                            
                            date_col = detect_column(columns, ['date', 'DATE', 'Date audit', 'Date d\'audit'])
                            client_col = detect_column(columns, ['client', 'CLIENT', 'nom', 'société', 'entreprise'])
                            ref_col = detect_column(columns, ['référentiel', 'referentiel', 'programme', 'norme', 'standard'])
                            duree_col = detect_column(columns, ['durée', 'duree', 'jours', 'jour', 'temps'])
                            montant_col = detect_column(columns, ['montant', 'CA', 'chiffre', 'facturation', 'prix', 'tarif'])
                            frais_col = detect_column(columns, ['frais', 'mission', 'déplacement', 'deplacement', 'km'])
                            cout_col = detect_column(columns, ['coût', 'cout', 'auditeur', 'honoraire', 'vacation'])
                            statut_col = detect_column(columns, ['statut', 'état', 'etat', 'status'])
                            
                            # Afficher les colonnes détectées
                            st.write("**🔍 Colonnes détectées automatiquement:**")
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.write(f"📅 Date: `{date_col}`")
                                st.write(f"👤 Client: `{client_col}`")
                            with col2:
                                st.write(f"📋 Référentiel: `{ref_col}`")
                                st.write(f"⏱️ Durée: `{duree_col}`")
                            with col3:
                                st.write(f"💰 Montant: `{montant_col}`")
                                st.write(f"🚗 Frais: `{frais_col}`")
                            with col4:
                                st.write(f"👨‍💼 Coût Aud.: `{cout_col}`")
                                st.write(f"✅ Statut: `{statut_col}`")
                            
                            if st.button("✨ Importer automatiquement Certification", key="auto_import_certif", type="primary"):
                                if date_col and client_col and montant_col:
                                    try:
                                        new_data = pd.DataFrame()
                                        new_data['Date'] = pd.to_datetime(df_certif[date_col], errors='coerce')
                                        new_data['Client'] = df_certif[client_col].astype(str)
                                        new_data['Référentiel'] = df_certif[ref_col].astype(str) if ref_col else 'N/A'
                                        new_data['Durée'] = pd.to_numeric(df_certif[duree_col], errors='coerce') if duree_col else 1.0
                                        new_data['Montant_Facturation'] = pd.to_numeric(df_certif[montant_col], errors='coerce')
                                        new_data['Frais_Mission'] = pd.to_numeric(df_certif[frais_col], errors='coerce') if frais_col else 0
                                        new_data['Cout_Auditeur'] = pd.to_numeric(df_certif[cout_col], errors='coerce') if cout_col else 0
                                        new_data['Statut'] = df_certif[statut_col].astype(str) if statut_col else 'Facturé'
                                        
                                        # Nettoyer
                                        new_data = new_data.dropna(subset=['Date'])
                                        new_data = new_data[new_data['Client'].str.strip() != '']
                                        new_data = new_data[new_data['Montant_Facturation'].notna()]
                                        new_data = new_data[new_data['Montant_Facturation'] > 0]
                                        new_data = new_data.fillna(0)
                                        
                                        # Remplacer ou ajouter
                                        if replace_certif:
                                            st.session_state.facturation_certif = new_data.reset_index(drop=True)
                                        else:
                                            st.session_state.facturation_certif = pd.concat(
                                                [st.session_state.facturation_certif, new_data], 
                                                ignore_index=True
                                            )
                                        
                                        st.success(f"✅ {len(new_data)} lignes de Certification importées avec succès!")
                                        st.balloons()
                                        st.rerun()
                                        
                                    except Exception as e:
                                        st.error(f"❌ Erreur lors de l'import: {str(e)}")
                                        st.write("Détails:", e)
                                else:
                                    st.error("❌ Impossible de détecter les colonnes essentielles (Date, Client, Montant)")
                                    
                        except Exception as e:
                            st.error(f"❌ Erreur lors de la lecture de la feuille Certification: {str(e)}")
                
                # ========================================
                # IMPORT AUTOMATIQUE FACTURATION AUTRES
                # ========================================
                if 'Facturation-Autres' in excel_file.sheet_names:
                    with st.expander("🔶 Facturation Autres - Import Automatique", expanded=True):
                        try:
                            df_autres_raw = pd.read_excel(excel_file, sheet_name='Facturation-Autres')
                            
                            st.write(f"📊 Aperçu des données brutes ({len(df_autres_raw)} lignes):")
                            st.dataframe(df_autres_raw.head(5), use_container_width=True)
                            
                            # Paramètres d'import
                            col1, col2 = st.columns(2)
                            with col1:
                                start_row_autres = st.number_input(
                                    "Ligne de départ (0 = première ligne)", 
                                    min_value=0, 
                                    max_value=max(0, len(df_autres_raw)-1), 
                                    value=2,
                                    key="auto_autres_start"
                                )
                            with col2:
                                replace_autres = st.checkbox(
                                    "Remplacer les données existantes", 
                                    value=True,
                                    key="auto_autres_replace"
                                )
                            
                            # Détection automatique
                            df_autres = clean_data(df_autres_raw, start_row_autres)
                            columns = df_autres.columns.tolist()
                            
                            date_col = detect_column(columns, ['date', 'DATE'])
                            type_col = detect_column(columns, ['type', 'prestation', 'catégorie', 'categorie'])
                            client_col = detect_column(columns, ['client', 'CLIENT', 'nom', 'société'])
                            desc_col = detect_column(columns, ['description', 'libellé', 'libelle', 'objet', 'commentaire'])
                            montant_col = detect_column(columns, ['montant', 'CA', 'chiffre', 'facturation', 'prix'])
                            frais_col = detect_column(columns, ['frais', 'mission', 'déplacement'])
                            cout_col = detect_column(columns, ['coût', 'cout', 'auditeur', 'prestataire', 'honoraire'])
                            statut_col = detect_column(columns, ['statut', 'état', 'status'])
                            
                            # Afficher les colonnes détectées
                            st.write("**🔍 Colonnes détectées automatiquement:**")
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.write(f"📅 Date: `{date_col}`")
                                st.write(f"📦 Type: `{type_col}`")
                            with col2:
                                st.write(f"👤 Client: `{client_col}`")
                                st.write(f"📝 Description: `{desc_col}`")
                            with col3:
                                st.write(f"💰 Montant: `{montant_col}`")
                                st.write(f"🚗 Frais: `{frais_col}`")
                            with col4:
                                st.write(f"👨‍💼 Coût: `{cout_col}`")
                                st.write(f"✅ Statut: `{statut_col}`")
                            
                            if st.button("✨ Importer automatiquement Autres", key="auto_import_autres", type="primary"):
                                if date_col and client_col and montant_col:
                                    try:
                                        new_data = pd.DataFrame()
                                        new_data['Date'] = pd.to_datetime(df_autres[date_col], errors='coerce')
                                        new_data['Type'] = df_autres[type_col].astype(str) if type_col else 'Autre'
                                        new_data['Client'] = df_autres[client_col].astype(str)
                                        new_data['Description'] = df_autres[desc_col].astype(str) if desc_col else ''
                                        new_data['Montant_Facturation'] = pd.to_numeric(df_autres[montant_col], errors='coerce')
                                        new_data['Frais_Mission'] = pd.to_numeric(df_autres[frais_col], errors='coerce') if frais_col else 0
                                        new_data['Cout_Auditeur'] = pd.to_numeric(df_autres[cout_col], errors='coerce') if cout_col else 0
                                        new_data['Statut'] = df_autres[statut_col].astype(str) if statut_col else 'Facturé'
                                        
                                        # Nettoyer
                                        new_data = new_data.dropna(subset=['Date'])
                                        new_data = new_data[new_data['Client'].str.strip() != '']
                                        new_data = new_data[new_data['Montant_Facturation'].notna()]
                                        new_data = new_data[new_data['Montant_Facturation'] > 0]
                                        new_data = new_data.fillna(0)
                                        
                                        # Remplacer ou ajouter
                                        if replace_autres:
                                            st.session_state.facturation_autres = new_data.reset_index(drop=True)
                                        else:
                                            st.session_state.facturation_autres = pd.concat(
                                                [st.session_state.facturation_autres, new_data], 
                                                ignore_index=True
                                            )
                                        
                                        st.success(f"✅ {len(new_data)} lignes de Facturation Autres importées avec succès!")
                                        st.balloons()
                                        st.rerun()
                                        
                                    except Exception as e:
                                        st.error(f"❌ Erreur lors de l'import: {str(e)}")
                                        st.write("Détails:", e)
                                else:
                                    st.error("❌ Impossible de détecter les colonnes essentielles (Date, Client, Montant)")
                                    
                        except Exception as e:
                            st.error(f"❌ Erreur lors de la lecture de la feuille Autres: {str(e)}")
                
                # ========================================
                # IMPORT AUTOMATIQUE CHARGES DIVERSES
                # ========================================
                if 'FRAIS DIVERS' in excel_file.sheet_names:
                    with st.expander("💸 Charges Diverses - Import Automatique"):
                        try:
                            df_charges_raw = pd.read_excel(excel_file, sheet_name='FRAIS DIVERS')
                            
                            st.write(f"📊 Aperçu des données brutes ({len(df_charges_raw)} lignes):")
                            st.dataframe(df_charges_raw.head(5), use_container_width=True)
                            
                            # Paramètres d'import
                            col1, col2 = st.columns(2)
                            with col1:
                                start_row_charges = st.number_input(
                                    "Ligne de départ (0 = première ligne)", 
                                    min_value=0, 
                                    max_value=max(0, len(df_charges_raw)-1), 
                                    value=1,
                                    key="auto_charges_start"
                                )
                            with col2:
                                replace_charges = st.checkbox(
                                    "Remplacer les données existantes", 
                                    value=True,
                                    key="auto_charges_replace"
                                )
                            
                            # Détection automatique
                            df_charges = clean_data(df_charges_raw, start_row_charges)
                            columns = df_charges.columns.tolist()
                            
                            date_col = detect_column(columns, ['date', 'DATE'])
                            cat_col = detect_column(columns, ['catégorie', 'categorie', 'type', 'nature'])
                            desc_col = detect_column(columns, ['description', 'libellé', 'libelle', 'objet'])
                            montant_col = detect_column(columns, ['montant', 'coût', 'cout', 'prix', 'charge'])
                            statut_col = detect_column(columns, ['statut', 'état', 'status', 'payé', 'paye'])
                            
                            # Afficher les colonnes détectées
                            st.write("**🔍 Colonnes détectées automatiquement:**")
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.write(f"📅 Date: `{date_col}`")
                                st.write(f"📦 Catégorie: `{cat_col}`")
                            with col2:
                                st.write(f"📝 Description: `{desc_col}`")
                                st.write(f"💰 Montant: `{montant_col}`")
                            with col3:
                                st.write(f"✅ Statut: `{statut_col}`")
                            
                            if st.button("✨ Importer automatiquement Charges", key="auto_import_charges", type="primary"):
                                if date_col and montant_col:
                                    try:
                                        new_data = pd.DataFrame()
                                        new_data['Date'] = pd.to_datetime(df_charges[date_col], errors='coerce')
                                        new_data['Catégorie'] = df_charges[cat_col].astype(str) if cat_col else 'Autre'
                                        new_data['Description'] = df_charges[desc_col].astype(str) if desc_col else ''
                                        new_data['Montant'] = pd.to_numeric(df_charges[montant_col], errors='coerce')
                                        new_data['Statut'] = df_charges[statut_col].astype(str) if statut_col else 'Payé'
                                        
                                        # Nettoyer
                                        new_data = new_data.dropna(subset=['Date', 'Montant'])
                                        new_data = new_data[new_data['Montant'] > 0]
                                        new_data = new_data.fillna('')
                                        
                                        # Remplacer ou ajouter
                                        if replace_charges:
                                            st.session_state.charges_diverses = new_data.reset_index(drop=True)
                                        else:
                                            st.session_state.charges_diverses = pd.concat(
                                                [st.session_state.charges_diverses, new_data], 
                                                ignore_index=True
                                            )
                                        
                                        st.success(f"✅ {len(new_data)} lignes de Charges importées avec succès!")
                                        st.balloons()
                                        st.rerun()
                                        
                                    except Exception as e:
                                        st.error(f"❌ Erreur lors de l'import: {str(e)}")
                                        st.write("Détails:", e)
                                else:
                                    st.error("❌ Impossible de détecter les colonnes essentielles (Date, Montant)")
                                    
                        except Exception as e:
                            st.error(f"❌ Erreur lors de la lecture de la feuille Charges: {str(e)}")
                
                # Message si aucune feuille reconnue
                if not any(sheet in excel_file.sheet_names for sheet in ['Facturation-Certif', 'Facturation-Autres', 'FRAIS DIVERS']):
                    st.warning("⚠️ Aucune feuille standard détectée. Assurez-vous que votre fichier contient les feuilles: 'Facturation-Certif', 'Facturation-Autres' ou 'FRAIS DIVERS'")
                    
            except Exception as e:
                st.error(f"❌ Erreur lors de la lecture du fichier: {str(e)}")
                st.write("Détails de l'erreur:", e)
            try:
                # Lecture du fichier
                excel_file = pd.ExcelFile(uploaded_file)
                st.success(f"✅ Fichier chargé: {uploaded_file.name}")
                
                st.write("**Feuilles disponibles:**", excel_file.sheet_names)
                
                # Section Import Facturation Certification
                with st.expander("📋 Importer Facturation Certification", expanded=True):
                    st.write("**Sélectionner la feuille contenant les facturations certification**")
                    
                    certif_sheet = st.selectbox(
                        "Feuille Certification", 
                        excel_file.sheet_names,
                        key="certif_sheet"
                    )
                    
                    if certif_sheet:
                        df_certif = pd.read_excel(excel_file, sheet_name=certif_sheet)
                        st.write(f"Aperçu ({len(df_certif)} lignes):")
                        st.dataframe(df_certif.head(10), use_container_width=True)
                        
                        st.write("**Mapper les colonnes:**")
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            date_col = st.selectbox("Colonne Date", [''] + list(df_certif.columns), key="certif_date")
                            client_col = st.selectbox("Colonne Client", [''] + list(df_certif.columns), key="certif_client")
                            ref_col = st.selectbox("Colonne Référentiel", [''] + list(df_certif.columns), key="certif_ref")
                        
                        with col2:
                            duree_col = st.selectbox("Colonne Durée", [''] + list(df_certif.columns), key="certif_duree")
                            montant_col = st.selectbox("Colonne Montant Facturation", [''] + list(df_certif.columns), key="certif_montant")
                            frais_col = st.selectbox("Colonne Frais Mission", [''] + list(df_certif.columns), key="certif_frais")
                        
                        with col3:
                            cout_col = st.selectbox("Colonne Coût Auditeur", [''] + list(df_certif.columns), key="certif_cout")
                            statut_col = st.selectbox("Colonne Statut (optionnel)", [''] + list(df_certif.columns), key="certif_statut")
                        
                        # Ligne de départ
                        start_row = st.number_input("Ligne de départ (0 = première ligne)", 
                                                   min_value=0, 
                                                   max_value=len(df_certif)-1, 
                                                   value=2,
                                                   key="certif_start")
                        
                        if st.button("✅ Importer les données Certification", key="import_certif"):
                            if all([date_col, client_col, montant_col]):
                                try:
                                    # Créer le nouveau dataframe
                                    new_data = pd.DataFrame()
                                    new_data['Date'] = pd.to_datetime(df_certif[date_col].iloc[start_row:], errors='coerce')
                                    new_data['Client'] = df_certif[client_col].iloc[start_row:]
                                    new_data['Référentiel'] = df_certif[ref_col].iloc[start_row:] if ref_col else ''
                                    new_data['Durée'] = pd.to_numeric(df_certif[duree_col].iloc[start_row:], errors='coerce') if duree_col else 1.0
                                    new_data['Montant_Facturation'] = pd.to_numeric(df_certif[montant_col].iloc[start_row:], errors='coerce')
                                    new_data['Frais_Mission'] = pd.to_numeric(df_certif[frais_col].iloc[start_row:], errors='coerce') if frais_col else 0
                                    new_data['Cout_Auditeur'] = pd.to_numeric(df_certif[cout_col].iloc[start_row:], errors='coerce') if cout_col else 0
                                    new_data['Statut'] = df_certif[statut_col].iloc[start_row:] if statut_col else 'Facturé'
                                    
                                    # Nettoyer les lignes vides
                                    new_data = new_data.dropna(subset=['Date', 'Client', 'Montant_Facturation'])
                                    new_data = new_data[new_data['Montant_Facturation'] > 0]
                                    new_data = new_data.fillna(0)
                                    
                                    # Remplacer ou ajouter
                                    replace_option = st.radio("Options d'import:", 
                                                             ["Remplacer les données existantes", "Ajouter aux données existantes"],
                                                             key="certif_replace")
                                    
                                    if replace_option == "Remplacer les données existantes":
                                        st.session_state.facturation_certif = new_data.reset_index(drop=True)
                                    else:
                                        st.session_state.facturation_certif = pd.concat(
                                            [st.session_state.facturation_certif, new_data], 
                                            ignore_index=True
                                        )
                                    
                                    st.success(f"✅ {len(new_data)} lignes importées avec succès!")
                                    st.balloons()
                                    st.rerun()
                                    
                                except Exception as e:
                                    st.error(f"❌ Erreur lors de l'import: {str(e)}")
                            else:
                                st.warning("⚠️ Veuillez sélectionner au minimum: Date, Client et Montant")
                
                # Section Import Facturation Autres
                with st.expander("📋 Importer Facturation Autres"):
                    st.write("**Sélectionner la feuille contenant les autres facturations**")
                    
                    autres_sheet = st.selectbox(
                        "Feuille Autres", 
                        excel_file.sheet_names,
                        key="autres_sheet"
                    )
                    
                    if autres_sheet:
                        df_autres = pd.read_excel(excel_file, sheet_name=autres_sheet)
                        st.write(f"Aperçu ({len(df_autres)} lignes):")
                        st.dataframe(df_autres.head(10), use_container_width=True)
                        
                        st.write("**Mapper les colonnes:**")
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            date_col_a = st.selectbox("Colonne Date", [''] + list(df_autres.columns), key="autres_date")
                            type_col = st.selectbox("Colonne Type", [''] + list(df_autres.columns), key="autres_type")
                            client_col_a = st.selectbox("Colonne Client", [''] + list(df_autres.columns), key="autres_client")
                        
                        with col2:
                            desc_col = st.selectbox("Colonne Description", [''] + list(df_autres.columns), key="autres_desc")
                            montant_col_a = st.selectbox("Colonne Montant", [''] + list(df_autres.columns), key="autres_montant")
                            frais_col_a = st.selectbox("Colonne Frais Mission", [''] + list(df_autres.columns), key="autres_frais")
                        
                        with col3:
                            cout_col_a = st.selectbox("Colonne Coût Auditeur", [''] + list(df_autres.columns), key="autres_cout")
                            statut_col_a = st.selectbox("Colonne Statut (optionnel)", [''] + list(df_autres.columns), key="autres_statut")
                        
                        start_row_a = st.number_input("Ligne de départ", 
                                                     min_value=0, 
                                                     max_value=len(df_autres)-1, 
                                                     value=2,
                                                     key="autres_start")
                        
                        if st.button("✅ Importer les données Autres", key="import_autres"):
                            if all([date_col_a, client_col_a, montant_col_a]):
                                try:
                                    new_data = pd.DataFrame()
                                    new_data['Date'] = pd.to_datetime(df_autres[date_col_a].iloc[start_row_a:], errors='coerce')
                                    new_data['Type'] = df_autres[type_col].iloc[start_row_a:] if type_col else 'Autre'
                                    new_data['Client'] = df_autres[client_col_a].iloc[start_row_a:]
                                    new_data['Description'] = df_autres[desc_col].iloc[start_row_a:] if desc_col else ''
                                    new_data['Montant_Facturation'] = pd.to_numeric(df_autres[montant_col_a].iloc[start_row_a:], errors='coerce')
                                    new_data['Frais_Mission'] = pd.to_numeric(df_autres[frais_col_a].iloc[start_row_a:], errors='coerce') if frais_col_a else 0
                                    new_data['Cout_Auditeur'] = pd.to_numeric(df_autres[cout_col_a].iloc[start_row_a:], errors='coerce') if cout_col_a else 0
                                    new_data['Statut'] = df_autres[statut_col_a].iloc[start_row_a:] if statut_col_a else 'Facturé'
                                    
                                    new_data = new_data.dropna(subset=['Date', 'Client', 'Montant_Facturation'])
                                    new_data = new_data[new_data['Montant_Facturation'] > 0]
                                    new_data = new_data.fillna(0)
                                    
                                    replace_option = st.radio("Options d'import:", 
                                                             ["Remplacer les données existantes", "Ajouter aux données existantes"],
                                                             key="autres_replace")
                                    
                                    if replace_option == "Remplacer les données existantes":
                                        st.session_state.facturation_autres = new_data.reset_index(drop=True)
                                    else:
                                        st.session_state.facturation_autres = pd.concat(
                                            [st.session_state.facturation_autres, new_data], 
                                            ignore_index=True
                                        )
                                    
                                    st.success(f"✅ {len(new_data)} lignes importées avec succès!")
                                    st.balloons()
                                    st.rerun()
                                    
                                except Exception as e:
                                    st.error(f"❌ Erreur lors de l'import: {str(e)}")
                            else:
                                st.warning("⚠️ Veuillez sélectionner au minimum: Date, Client et Montant")
                
                # Section Import Charges
                with st.expander("📋 Importer Charges Diverses"):
                    st.write("**Sélectionner la feuille contenant les charges diverses**")
                    
                    charges_sheet = st.selectbox(
                        "Feuille Charges", 
                        excel_file.sheet_names,
                        key="charges_sheet"
                    )
                    
                    if charges_sheet:
                        df_charges = pd.read_excel(excel_file, sheet_name=charges_sheet)
                        st.write(f"Aperçu ({len(df_charges)} lignes):")
                        st.dataframe(df_charges.head(10), use_container_width=True)
                        
                        st.write("**Mapper les colonnes:**")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            date_col_c = st.selectbox("Colonne Date", [''] + list(df_charges.columns), key="charges_date")
                            cat_col = st.selectbox("Colonne Catégorie", [''] + list(df_charges.columns), key="charges_cat")
                            desc_col_c = st.selectbox("Colonne Description", [''] + list(df_charges.columns), key="charges_desc")
                        
                        with col2:
                            montant_col_c = st.selectbox("Colonne Montant", [''] + list(df_charges.columns), key="charges_montant")
                            statut_col_c = st.selectbox("Colonne Statut (optionnel)", [''] + list(df_charges.columns), key="charges_statut")
                        
                        start_row_c = st.number_input("Ligne de départ", 
                                                     min_value=0, 
                                                     max_value=len(df_charges)-1, 
                                                     value=1,
                                                     key="charges_start")
                        
                        if st.button("✅ Importer les Charges", key="import_charges"):
                            if all([date_col_c, montant_col_c]):
                                try:
                                    new_data = pd.DataFrame()
                                    new_data['Date'] = pd.to_datetime(df_charges[date_col_c].iloc[start_row_c:], errors='coerce')
                                    new_data['Catégorie'] = df_charges[cat_col].iloc[start_row_c:] if cat_col else 'Autre'
                                    new_data['Description'] = df_charges[desc_col_c].iloc[start_row_c:] if desc_col_c else ''
                                    new_data['Montant'] = pd.to_numeric(df_charges[montant_col_c].iloc[start_row_c:], errors='coerce')
                                    new_data['Statut'] = df_charges[statut_col_c].iloc[start_row_c:] if statut_col_c else 'Payé'
                                    
                                    new_data = new_data.dropna(subset=['Date', 'Montant'])
                                    new_data = new_data[new_data['Montant'] > 0]
                                    new_data = new_data.fillna('')
                                    
                                    replace_option = st.radio("Options d'import:", 
                                                             ["Remplacer les données existantes", "Ajouter aux données existantes"],
                                                             key="charges_replace")
                                    
                                    if replace_option == "Remplacer les données existantes":
                                        st.session_state.charges_diverses = new_data.reset_index(drop=True)
                                    else:
                                        st.session_state.charges_diverses = pd.concat(
                                            [st.session_state.charges_diverses, new_data], 
                                            ignore_index=True
                                        )
                                    
                                    st.success(f"✅ {len(new_data)} lignes importées avec succès!")
                                    st.balloons()
                                    st.rerun()
                                    
                                except Exception as e:
                                    st.error(f"❌ Erreur lors de l'import: {str(e)}")
                            else:
                                st.warning("⚠️ Veuillez sélectionner au minimum: Date et Montant")
                    
            except Exception as e:
                st.error(f"❌ Erreur lors de la lecture du fichier: {str(e)}")
                st.write("Détails de l'erreur:", e)
    
    with tab2:
        st.subheader("Exporter les données")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("**📋 Facturation Certification**")
            csv_certif = st.session_state.facturation_certif.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Télécharger (CSV)",
                data=csv_certif,
                file_name=f'facturation_certif_{datetime.now().strftime("%Y%m%d")}.csv',
                mime='text/csv'
            )
        
        with col2:
            st.write("**📋 Facturation Autres**")
            csv_autres = st.session_state.facturation_autres.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Télécharger (CSV)",
                data=csv_autres,
                file_name=f'facturation_autres_{datetime.now().strftime("%Y%m%d")}.csv',
                mime='text/csv'
            )
        
        with col3:
            st.write("**📋 Charges Diverses**")
            csv_charges = st.session_state.charges_diverses.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Télécharger (CSV)",
                data=csv_charges,
                file_name=f'charges_diverses_{datetime.now().strftime("%Y%m%d")}.csv',
                mime='text/csv'
            )
        
        st.divider()
        
        # Export du forecast
        if 'forecast_data' in st.session_state:
            st.write("**📈 Export du Forecast**")
            csv_forecast = st.session_state.forecast_data.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Télécharger Forecast (CSV)",
                data=csv_forecast,
                file_name=f'forecast_{datetime.now().strftime("%Y%m%d")}.csv',
                mime='text/csv',
                type="primary"
            )

# Footer
st.divider()
st.markdown("""
    <div style='text-align: center; color: #888; padding: 20px;'>
    📊 Outil de Suivi Financier & Forecast | Développé avec Streamlit
    </div>
""", unsafe_allow_html=True)
