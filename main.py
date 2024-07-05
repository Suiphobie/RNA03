# ANOUSSONE SIMUONG M2 DATA MARKETING


import pandas as pd
import streamlit as st
import plotly.express as px
st.set_page_config(page_title='Devoir RNA Dashboard', layout='wide')

#caching for better perf
@st.cache_data
def load_data():
    return pd.read_csv('asso.csv')

df = load_data()

st.subheader('RNA 03')

#input for the filter
with st.sidebar:
    codepostal_options = df['adrs_codepostal'].unique().tolist()
    codepostal_filter = st.sidebar.multiselect(
        'Sélectionnez un ou plusieurs codes postaux',
        options=codepostal_options
    )

    categorie_options = [''] + df['libelle_parent'].unique().tolist()
    categorie_filter = st.sidebar.selectbox(
        'Sélectionnez une catégorie',
        options=categorie_options,
        index=0
    )

    annee_creat_options = [''] + df['annee_creat'].unique().tolist()
    annee_creat_filter = st.sidebar.selectbox(
        'Sélectionnez une année de création',
        options=annee_creat_options,
        index=0
    )
    st.markdown("""Réalisé par Anoussone SIMUONG | M2 Data Marketing""")

#logic for the filter
#probs have a better way to do this, idk
filtered_df_col1 = df.copy()

if codepostal_filter:
    filtered_df_col1 = filtered_df_col1[filtered_df_col1['adrs_codepostal'].isin(codepostal_filter)]

if categorie_filter:
    filtered_df_col1 = filtered_df_col1[filtered_df_col1['libelle_parent'] == categorie_filter]

if annee_creat_filter:
    filtered_df_col1 = filtered_df_col1[filtered_df_col1['annee_creat'] == annee_creat_filter]

filtered_df_col2 = df.copy()

if codepostal_filter:
    filtered_df_col2 = filtered_df_col2[filtered_df_col2['adrs_codepostal'].isin(codepostal_filter)]

filtered_df_col3 = df.copy()

if categorie_filter:
    filtered_df_col3 = filtered_df_col3[filtered_df_col3['libelle_parent'] == categorie_filter]

if annee_creat_filter:
    filtered_df_col3 = filtered_df_col3[filtered_df_col3['annee_creat'] == annee_creat_filter]

# making central graph a bit larger than the rest
col1, col2, col3 = st.columns([0.1,0.7,0.2])
# logic for the number
with col1:
    st.markdown('**Associations**')
    st.write(f'{filtered_df_col1["nom"].nunique()}')
    st.markdown('**Membres**')
    st.write(f'{filtered_df_col1["membres"].sum()}')
    st.markdown('**Bénéfices**')
    st.markdown(f'{filtered_df_col1["benefices"].sum()} **euro**')

# logic for the bar chart
asso_by_year = filtered_df_col2.groupby('annee_creat').size().reset_index(name='count')

with col2:
    st.markdown('**Nombre d\'associations par année de création**')
    st.bar_chart(asso_by_year.set_index('annee_creat')['count'])

# logic for the donut chart
filtered_df_col3['position'] = filtered_df_col3['position'].map({'A': 'Active', 'D': 'Dissoute', 'S': 'Supprimée'})
position_counts = filtered_df_col3['position'].value_counts().reset_index()
position_counts.columns = ['position', 'count']

fig = px.pie(position_counts, names='position', values='count', hole=0.5,
             title='Répartition des positions')

with col3:
    st.plotly_chart(fig)

# last bar chart
filtered_df_bar_chart = df.copy()

if annee_creat_filter:
    filtered_df_bar_chart = filtered_df_bar_chart[filtered_df_bar_chart['annee_creat'] == annee_creat_filter]

category_counts = filtered_df_bar_chart['libelle_parent'].value_counts().reset_index()
category_counts.columns = ['libelle_parent', 'count']

fig_bar = px.bar(category_counts, x='count', y='libelle_parent', orientation='h',
                 title='Répartition des associations par catégorie',
                 labels={'libelle_parent': 'Catégories', 'count': 'Nombre'})

st.plotly_chart(fig_bar)
