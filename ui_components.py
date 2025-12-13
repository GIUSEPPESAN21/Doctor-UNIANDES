# -*- coding: utf-8 -*-
"""
Módulo de Componentes de Interfaz de Usuario (UI)
Descripción: Centraliza el diseño visual, estilos CSS avanzados y componentes
reutilizables para limpiar el código de la aplicación principal.
"""
import streamlit as st

# --- CONFIGURACIÓN DE ESTILOS (CSS) ---
def load_custom_css():
    """Inyecta CSS avanzado para una apariencia premium y moderna."""
    st.markdown("""
        <style>
        /* --- FUENTES --- */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* --- VARIABLES GLOBALES --- */
        :root {
            /* Colores Principales (Tema Clínico Moderno) */
            --primary: #2563EB;        /* Azul Real */
            --primary-dark: #1E40AF;
            --secondary: #10B981;      /* Verde Esmeralda (Éxito/Vitalidad) */
            --accent: #F59E0B;         /* Ámbar (Alertas) */
            --danger: #EF4444;         /* Rojo (Peligro) */
            --background: #F3F4F6;     /* Gris muy claro para fondo */
            --surface: #FFFFFF;        /* Blanco puro para tarjetas */
            --text-main: #1F2937;
            --text-light: #6B7280;
            
            /* Efectos */
            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            --radius-md: 0.5rem;
            --radius-lg: 0.75rem;
        }

        /* --- AJUSTES GENERALES --- */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        /* --- CONTENEDORES Y TARJETAS --- */
        .stContainer, [data-testid="stVerticalBlock"] > div > div {
           /* background-color: var(--surface);  <-- Streamlit maneja esto dinamico, cuidado */
        }
        
        /* Clase personalizada para tarjetas tipo "Glass" o limpias */
        .card-container {
            background-color: var(--surface);
            border-radius: var(--radius-lg);
            padding: 1.5rem;
            box-shadow: var(--shadow-md);
            border: 1px solid rgba(229, 231, 235, 0.5);
            margin-bottom: 1rem;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .card-container:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-lg);
        }

        /* --- METRICAS --- */
        [data-testid="stMetricValue"] {
            font-size: 1.8rem !important;
            font-weight: 700 !important;
            color: var(--primary);
        }
        [data-testid="stMetricLabel"] {
            font-size: 0.9rem !important;
            color: var(--text-light);
            font-weight: 500;
        }

        /* --- BOTONES --- */
        .stButton > button {
            border-radius: var(--radius-md);
            font-weight: 600;
            border: none;
            padding: 0.5rem 1rem;
            transition: all 0.2s;
        }
        .stButton > button:hover {
            opacity: 0.9;
            transform: scale(1.02);
        }
        /* Botón Primario */
        div[data-testid="stButton"] > button[kind="primary"] {
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
            box-shadow: 0 4px 6px rgba(37, 99, 235, 0.2);
            color: white;
        }
        /* Botón Secundario/Outline */
        div[data-testid="stButton"] > button[kind="secondary"] {
            background: transparent;
            border: 2px solid var(--primary);
            color: var(--primary);
        }
        div[data-testid="stButton"] > button[kind="secondary"]:hover {
            background: var(--primary);
            color: white;
        }

        /* --- INPUTS --- */
        .stTextInput input, .stNumberInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
            border-radius: var(--radius-md);
            border: 1px solid #E5E7EB;
            padding: 0.5rem;
        }
        .stTextInput input:focus, .stNumberInput input:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2);
        }

        /* --- TÍTULOS --- */
        h1, h2, h3 {
            color: var(--text-main); 
            letter-spacing: -0.025em;
        }
        h1 { font-weight: 800; }
        .highlight { color: var(--primary); }

        /* --- HEADER PERSONALIZADO --- */
        .header-style {
            background: linear-gradient(90deg, #1E3A8A 0%, #2563EB 100%);
            padding: 1rem 2rem;
            border-radius: var(--radius-lg);
            color: white;
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 2rem;
            box-shadow: var(--shadow-md);
        }
        </style>
    """, unsafe_allow_html=True)

# --- COMPONENTES VISUALES ---

def render_hero_header(physician_email):
    """Renderiza un encabezado moderno tipo 'Hero'."""
    st.markdown(f"""
        <div class="header-style">
            <div>
                <h2 style="color: white; margin: 0; font-size: 1.5rem;">Doctor at Home</h2>
                <p style="margin: 0; opacity: 0.9; font-size: 0.9rem;">Portal Clínico Inteligente</p>
            </div>
            <div style="text-align: right;">
                <span style="font-size: 0.9rem; background: rgba(255,255,255,0.2); padding: 5px 10px; border-radius: 20px;">
                    👨‍⚕️ {physician_email}
                </span>
            </div>
        </div>
    """, unsafe_allow_html=True)

def card_metric(label, value, delta=None, color="blue"):
    """Renderiza una métrica en una tarjeta estilizada."""
    st.markdown(f"""
        <div style="background: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); border-left: 5px solid {color};">
            <p style="margin: 0; color: #6B7280; font-size: 0.85rem; font-weight: 600; text-transform: uppercase;">{label}</p>
            <h3 style="margin: 5px 0 0 0; color: #1F2937; font-size: 1.5rem;">{value}</h3>
            {f'<p style="margin: 0; color: {color}; font-size: 0.8rem;">{delta}</p>' if delta else ''}
        </div>
    """, unsafe_allow_html=True)

def render_patient_card_item(patient, on_click_callback):
    """Renderiza un item de paciente en la lista con estilo de tarjeta."""
    # Usamos contenedores nativos de Streamlit con un estilo CSS aplicado via clase
    with st.container():
        st.markdown("""<div class="card-container">""", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([3, 2, 2])
        with c1:
            st.markdown(f"**{patient['nombre']}**")
            st.caption(f"ID: {patient['cedula']}")
        with c2:
            st.markdown(f"🗓️ **Edad:** {patient.get('edad', 'N/A')} años")
            st.markdown(f"📞 {patient.get('telefono', 'N/A')}")
        with c3:
            # El callback maneja la lógica de selección
            if st.button("Ver Expediente", key=f"btn_{patient['id']}", use_container_width=True, type="primary"):
                on_click_callback(patient['id'])
        st.markdown("</div>", unsafe_allow_html=True)
