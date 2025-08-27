import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from dotenv import load_dotenv
from langchain_experimental.agents import create_csv_agent
from langchain.llms import OpenAI


def plot_radar_chart(df: pd.DataFrame, lineup_df: pd.DataFrame, player_col: str):
    """
    Dibuja un radar chart comparando dos jugadores e informa equipo, posición y edad.
    - df: DataFrame agregado por jugador.
    - lineup_df: DataFrame con datos extra (imagen, equipo, posiciones, edad).
    - player_col: nombre de la columna de jugador.
    """
    # Columnas numéricas para métricas
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    st.subheader("Radar Chart: Comparación de futbolistas 📊")

    # Filtros de equipo independientes para ambos jugadores
    teams = sorted(lineup_df['team_name'].dropna().unique().tolist())
    teams.insert(0, "Todos")
    team1 = st.selectbox("Equipo Jugador 1 (opcional)", teams, key="team1")
    team2 = st.selectbox("Equipo Jugador 2 (opcional)", teams, key="team2")

    

    # Generar listas de jugadores filtradas
    if team1 != "Todos":
        players1 = lineup_df[lineup_df['team_name'] == team1][player_col].unique().tolist()
    else:
        players1 = df[player_col].tolist()
    if team2 != "Todos":
        players2 = lineup_df[lineup_df['team_name'] == team2][player_col].unique().tolist()
    else:
        players2 = df[player_col].tolist()

    col1, col2 = st.columns(2)
    with col1:
        player1 = st.selectbox("Jugador 1", players1, key="player1")
    with col2:
        player2 = st.selectbox("Jugador 2", players2, index=1 if len(players2) > 1 else 0, key="player2")

    if player1 and player2:
        # Información de equipo, posición y edad
        info_col1, info_col2 = st.columns(2)
        for idx, player in enumerate([player1, player2]):
            rows = lineup_df[lineup_df[player_col] == player]
            if not rows.empty:
                team = rows['team_name'].iloc[0]
                detailed = rows.get('player_detailed_field_position', pd.Series([None])).iloc[0]
                primary = rows.get('player_field_position', pd.Series([None])).iloc[0]
                if detailed and str(detailed).upper() not in ['0', 'UNKNOWN', 'NAN']:
                    pos = str(detailed).capitalize().replace("_", " ")
                else:
                    pos = str(primary).capitalize() if primary else 'Desconocida'
                raw_age = rows['player_age'].iloc[0] if 'player_age' in rows.columns else None
                age = int(raw_age) if pd.notna(raw_age) else None
                age_text = f"{age} años" if age is not None else "Edad no disponible"
                info_text = f"**Equipo:** {team}  \n**Posición:** {pos}  \n**Edad:** {age_text}"
            else:
                info_text = "No hay datos de equipo/posición."
            (info_col1 if idx == 0 else info_col2).markdown(info_text)

        # Mostrar imágenes de los jugadores
        img_col1, img_col2 = st.columns(2)
        for idx, player in enumerate([player1, player2]):
            rows = lineup_df[lineup_df[player_col] == player]
            url = rows['player_image_url'].iloc[0] if ('player_image_url' in rows.columns and not rows.empty) else None
            target_col = img_col1 if idx == 0 else img_col2
            if url:
                target_col.image(url, caption=player, use_container_width=True)
            else:
                target_col.write(f"No hay imagen para {player}")

        # Selección de métricas
        metrics = st.multiselect(
            "Selecciona métricas para el radar",
            numeric_cols[3:],
            default=numeric_cols[3:6]
        )

        # Normalizar y preparar datos para radar
        radar_df = df[df[player_col].isin([player1, player2])].copy()
        global_max = df[metrics].max()
        for m in metrics:
            radar_df[m] = radar_df[m] / global_max[m] * 100

        # Convertir a formato largo y renombrar etiquetas
        df_long = pd.melt(
            radar_df,
            id_vars=player_col,
            value_vars=metrics,
            var_name="metric",
            value_name="value"
        )
        df_long["label"] = (
            df_long["metric"]
            .str.replace("_", " ")
            .str.title()
            .str.replace("Kilometer Per Hour", "Km/h")
        )

        # Dibujar radar
        fig = px.line_polar(
            df_long,
            r="value",
            theta="label",
            color=player_col,
            line_close=True,
            title=f"Comparación normalizada: {player1} vs {player2}"
        )
        fig.update_traces(fill="toself")
        fig.update_layout(
            polar=dict(
                radialaxis=dict(range=[0, 100], showgrid=False, showticklabels=False, ticks=''),
                angularaxis=dict(tickfont=dict(size=11), rotation=90, direction="clockwise")
            ),
            margin=dict(l=140, r=140, t=100, b=140)
        )
        st.plotly_chart(fig, use_container_width=True)


def main():
    
    # Carga de variables de entorn
    load_dotenv()

    # Cargamos permanentemente el CSV de lineups. Contine imágenes, datos de los jugadores, etc.
    try:
        lineup_df = pd.read_csv('./data/UEFA_Champions_League_lineups.csv')
    except FileNotFoundError:
        st.error("No se encontró el archivo 'UEFA_Champions_League_lineups.csv'.")
        return

    # Logo en esquina superior izquierda y título al lado
    col_logo, col_title = st.columns([3, 10])
    col_logo.image(
        'img/uefa-champions-league-1-logo-png-transparent.png',
        width=200,
        use_container_width=False
    )

    st.title("Analiza a los futbolistas de la Champions League 🌟⚽️ 24/25")
    st.header("Pregunta a tu CSV 🧑🏻‍💻 y compara jugadores")

    # Subida de CSV principal
    user_csv = st.file_uploader("Upload your CSV file", type="csv")
    if user_csv is None:
        return

    # Leer stats numericas y crear DataFrame con los datos agregados (Ej: Nº de goles, 
    # asistencias, etc... sumando todos los partidos
    df = pd.read_csv(user_csv)
    player_col = "player_name"
    if player_col not in df.columns:
        st.error(f"La columna '{player_col}' no se encontró en el CSV principal.")
        return

    # Columnas numericas para agregación
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    # agg_df contiene los datos de un jugador sumando todos los partidos
    agg_df = df.groupby(player_col, as_index=False)[numeric_cols].sum()


    # Radar Chart
    plot_radar_chart(agg_df, lineup_df, player_col)

    # Botón / guía para mostrar columnas disponibles
    with st.expander("**Guía: Columnas disponibles para análisis 📕**"):
        st.write(df.columns)

    # Chat Section
    st.subheader("Chat sobre tu CSV 📊")
    user_question = st.text_input("¿Qué quieres saber de tu CSV?")
    if user_question:
        user_csv.seek(0)
        llm = OpenAI(temperature=0, model="gpt-4o-mini")
        agent = create_csv_agent(
            llm,
            user_csv,
            verbose=True,
            allow_dangerous_code=True,
        )
        response = agent.run(user_question)
        st.write(response)

if __name__ == "__main__":
    main()
