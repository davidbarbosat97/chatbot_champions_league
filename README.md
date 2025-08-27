# 🏆 Chatbot Champions League 24/25

Este proyecto forma parte de mi **Trabajo de Fin de Máster** y consiste en una aplicación interactiva orientada a la **Dirección Deportiva** de un club profesional.  
La herramienta combina **IA Generativa**, **visualización de datos** y una interfaz sencilla para **analizar y comparar jugadores de la UEFA Champions League 2024/2025**.

---

## 🚀 Funcionalidades

- **Chatbot especializado**: responde preguntas sobre las estadísticas de jugadores cargadas en un `.csv` utilizando `LangChain` y modelos de OpenAI (GPT-4o-mini).
- **Radar Chart comparativo**: permite comparar el rendimiento de dos futbolistas en métricas ofensivas, defensivas, creativas y físicas.
- **Interfaz en Streamlit**: pensada para usuarios sin conocimientos de programación.
- **Accesible a clubes sin equipo de datos**: con una API de extracción de datos y ligeros ajustes, la herramienta puede ser usada por cualquier dirección deportiva.

---

---

## 🔑 Configuración

Para poder utilizar el chatbot necesitas:

1. **Cuenta de OpenAI con saldo activo**  
   El modelo `gpt-4o-mini` no está disponible en la versión gratuita, por lo que es necesario tener una **cuenta de pago en OpenAI** y haber cargado saldo en dólares.  
   Puedes crear tu cuenta y gestionar el billing aquí: [https://platform.openai.com](https://platform.openai.com).

2. **Archivo `.env` con tu clave de API**  
   En la raíz del proyecto crea un archivo llamado `.env` con el siguiente contenido:

   ```env
   OPENAI_API_KEY=tu_api_key_aqui

---


## 📊 Datos

⚠️ **Importante**: este repositorio incluye únicamente el código (`main.py`) y las dependencias (`requirements.txt`).  
Los **datasets de estadísticas y alineaciones** no se comparten aquí porque fueron facilitados por **Sport Data Campus** como apoyo académico.  

Para ejecutar el proyecto necesitarás:
- Un archivo `.csv` con estadísticas de jugadores (493 métricas).
- Un archivo `UEFA_Champions_League_lineups.csv` con edad, posición y equipo.

Coloca estos ficheros en la carpeta raíz del proyecto antes de lanzar la aplicación.

---

## 🛠️ Tecnologías utilizadas

- **Python 3.11+**
- Streamlit – interfaz interactiva
- pandas – manipulación de datos
- NumPy – cálculos numéricos
- Plotly – radar charts
- LangChain – orquestación del chatbot
- OpenAI – modelo GPT-4o-mini
- python-dotenv – gestión de credenciales

---

## 📦 Instalación

Clona este repositorio y crea un entorno virtual:

```bash
git clone https://github.com/tuusuario/chatbot-champions-league.git
cd chatbot-champions-league

python -m venv venv
source venv/bin/activate   # En Linux/Mac
venv\Scripts\activate      # En Windows
