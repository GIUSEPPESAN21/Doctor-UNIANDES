# -*- coding: utf-8 -*-
"""
Módulo de Componentes de Interfaz de Usuario (UI) - v6.0 FIXED
Diseño Premium SIN comentarios HTML que rompan el render.
"""
import streamlit as st
import pandas as pd

# ==============================================================================
# CSS PREMIUM
# ==============================================================================
def load_custom_css():
    """Inyecta CSS premium."""
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
        
        :root {
            --primary: #0066FF;
            --primary-dark: #0052CC;
            --primary-light: #E6F0FF;
            --success: #00C853;
            --warning: #FF9800;
            --danger: #F44336;
            --bg-primary: #F8FAFC;
            --bg-secondary: #FFFFFF;
            --text-primary: #0F172A;
            --text-secondary: #64748B;
            --border: #E2E8F0;
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.07);
            --shadow-lg: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
            --radius-md: 12px;
            --radius-lg: 16px;
        }

        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', sans-serif;
            color: var(--text-primary);
            -webkit-font-smoothing: antialiased;
        }
        
        .stApp {
            background: linear-gradient(135deg, #F8FAFC 0%, #EEF2FF 50%, #F0F9FF 100%) !important;
        }

        h1 {
            font-size: 2.25rem !important;
            font-weight: 800 !important;
            background: linear-gradient(135deg, #0066FF, #00C2FF);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        h2, h3 { font-weight: 700; }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(15px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .main > div { animation: fadeIn 0.4s ease-out; }

        .card-container, .medical-card {
            background: white;
            border-radius: var(--radius-lg);
            padding: 1.5rem;
            border: 1px solid var(--border);
            box-shadow: var(--shadow-md);
        }

        .badge {
            display: inline-flex;
            padding: 4px 12px;
            border-radius: 999px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        
        .badge-blue { background: #E6F0FF; color: #0066FF; }
        .badge-green { background: #E8F5E9; color: #00C853; }
        .badge-red { background: #FFEBEE; color: #F44336; }

        div[data-testid="stButton"] > button {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-weight: 600;
            border-radius: var(--radius-md);
            transition: all 0.2s ease;
        }
        
        div[data-testid="stButton"] > button[kind="primary"] {
            background: linear-gradient(135deg, #0066FF, #0052CC);
            color: white;
            box-shadow: 0 4px 14px rgba(0, 102, 255, 0.35);
        }
        
        div[data-testid="stButton"] > button[kind="primary"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 102, 255, 0.45);
        }

        div[data-testid="stTextInput"] input,
        div[data-testid="stNumberInput"] input,
        div[data-testid="stTextArea"] textarea {
            border-radius: var(--radius-md) !important;
            border: 2px solid var(--border) !important;
            padding: 0.75rem 1rem !important;
        }
        
        div[data-testid="stTextInput"] input:focus,
        div[data-testid="stNumberInput"] input:focus {
            border-color: var(--primary) !important;
            box-shadow: 0 0 0 3px rgba(0, 102, 255, 0.15) !important;
        }

        button[data-baseweb="tab"][aria-selected="true"] {
            background: white;
            color: var(--primary);
            border-bottom: 3px solid var(--primary);
        }
        </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# COMPONENTES
# ==============================================================================

def render_hero_header_with_logout(physician_email, on_logout):
    """Header Hero CON botón de logout integrado."""
    name = physician_email.split('@')[0].title() if physician_email else "Doctor"
    
    col1, col2 = st.columns([5, 1])
    with col1:
        st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #0066FF 0%, #00C2FF 100%);
                padding: 1.5rem 2rem;
                border-radius: 16px;
                color: white;
                box-shadow: 0 10px 40px rgba(0, 102, 255, 0.25);
            ">
                <p style="margin: 0; font-size: 0.85rem; opacity: 0.9;">👋 Bienvenido de nuevo</p>
                <h2 style="margin: 0.25rem 0 0 0; font-size: 1.5rem; font-weight: 800; color: white;">Dr. {name}</h2>
                <p style="margin: 0.25rem 0 0 0; font-size: 0.85rem; opacity: 0.85;">Panel de Control | SaludIA</p>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.write("")
        st.write("")
        if st.button("🚪 Salir", type="secondary", use_container_width=True):
            on_logout()

def render_hero_header(physician_email):
    """Header Hero simple (sin logout)."""
    name = physician_email.split('@')[0].title() if physician_email else "Doctor"
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #0066FF 0%, #00C2FF 100%);
            padding: 1.5rem 2rem;
            border-radius: 16px;
            color: white;
            margin-bottom: 1.5rem;
            box-shadow: 0 10px 40px rgba(0, 102, 255, 0.25);
        ">
            <p style="margin: 0; font-size: 0.85rem; opacity: 0.9;">👋 Bienvenido de nuevo</p>
            <h2 style="margin: 0.25rem 0 0 0; font-size: 1.5rem; font-weight: 800; color: white;">Dr. {name}</h2>
            <p style="margin: 0.25rem 0 0 0; font-size: 0.85rem; opacity: 0.85;">Panel de Control | SaludIA</p>
        </div>
    """, unsafe_allow_html=True)

def card_metric(label, value, delta=None, color_hex="#0066FF"):
    """Tarjeta KPI."""
    delta_html = f"<div style='font-size:0.8rem; color:#00C853; margin-top:6px;'>▲ {delta}</div>" if delta else ""
    st.markdown(f"""
        <div style="
            background: white;
            padding: 1.25rem;
            border-radius: 14px;
            border: 1px solid #E2E8F0;
            border-left: 4px solid {color_hex};
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        ">
            <div style="font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.05em; color: #64748B; font-weight: 600;">{label}</div>
            <div style="font-size: 1.75rem; font-weight: 800; color: #0F172A; margin-top: 4px;">{value}</div>
            {delta_html}
        </div>
    """, unsafe_allow_html=True)

def render_patient_card_item(patient, on_click):
    """Tarjeta de paciente."""
    with st.container():
        col1, col2, col3 = st.columns([3, 1.5, 1])
        with col1:
            st.markdown(f"**{patient['nombre']}**")
            st.caption(f"ID: {patient['cedula']}")
        with col2:
            st.markdown(f"<span style='background:#E6F0FF; color:#0066FF; padding:4px 10px; border-radius:999px; font-size:0.75rem; font-weight:600;'>{patient.get('edad', '?')} años</span>", unsafe_allow_html=True)
        with col3:
            if st.button("Ver →", key=f"p_{patient['id']}", type="secondary"):
                on_click(patient['id'])
        st.markdown("<hr style='margin:8px 0; border:0; border-top:1px solid #E2E8F0;'>", unsafe_allow_html=True)

def render_consultation_timeline_item(consultation, on_ai_click):
    """Timeline item - CORREGIDO sin comentarios HTML."""
    ts = consultation.get('timestamp')
    try:
        if ts is None or str(ts) == 'NaT':
            date_str = "Sin fecha"
        elif hasattr(ts, 'strftime'):
            date_str = ts.strftime('%d %b %Y • %H:%M')
        else:
            date_str = str(ts)[:16]
    except:
        date_str = "Fecha desconocida"
    
    # Badges
    badges = ""
    try:
        bp = int(consultation.get('presion_sistolica', 0) or 0)
        if bp >= 140:
            badges = "<span style='background:#FFEBEE; color:#F44336; padding:3px 10px; border-radius:999px; font-size:0.7rem; font-weight:600;'>⚠️ HTA</span>"
        elif 0 < bp < 90:
            badges = "<span style='background:#FFF3E0; color:#FF9800; padding:3px 10px; border-radius:999px; font-size:0.7rem; font-weight:600;'>⚡ Hipotensión</span>"
    except: pass
    
    # Motivo
    motivo = str(consultation.get('motivo_consulta', 'Sin motivo'))[:80]
    if len(str(consultation.get('motivo_consulta', ''))) > 80:
        motivo += "..."
    
    # Vitales
    pa_s = consultation.get('presion_sistolica', 'N/A')
    pa_d = consultation.get('presion_diastolica', 'N/A')
    fc = consultation.get('frec_cardiaca', 'N/A')
    glu = consultation.get('glucemia', 'N/A')
    imc = consultation.get('imc', 'N/A')

    # Render con Streamlit columns para evitar HTML crudo
    with st.container():
        st.markdown(f"""
        <div style="
            display: flex;
            gap: 15px;
            margin-bottom: 1rem;
        ">
            <div style="
                width: 12px;
                display: flex;
                flex-direction: column;
                align-items: center;
            ">
                <div style="width:12px; height:12px; background:#0066FF; border:3px solid white; border-radius:50%; box-shadow:0 0 0 3px #E6F0FF;"></div>
                <div style="width:2px; flex:1; background:linear-gradient(180deg, #0066FF, #E6F0FF);"></div>
            </div>
            <div style="flex:1;">
                <div style="font-family:'JetBrains Mono', monospace; font-size:0.8rem; color:#64748B; font-weight:600; margin-bottom:6px;">{date_str}</div>
                <div style="
                    background: white;
                    border: 1px solid #E2E8F0;
                    border-radius: 12px;
                    padding: 1rem;
                    box-shadow: 0 2px 6px rgba(0,0,0,0.04);
                ">
                    <div style="display:flex; justify-content:space-between; align-items:start; margin-bottom:10px;">
                        <div style="font-weight:700; color:#0F172A;">{motivo}</div>
                        <div>{badges}</div>
                    </div>
                    <div style="
                        display: grid;
                        grid-template-columns: repeat(4, 1fr);
                        gap: 8px;
                        background: #F8FAFC;
                        padding: 10px;
                        border-radius: 8px;
                        text-align: center;
                        font-size: 0.85rem;
                    ">
                        <div><span style="color:#94A3B8; font-size:0.65rem;">PA</span><br><b>{pa_s}/{pa_d}</b></div>
                        <div><span style="color:#94A3B8; font-size:0.65rem;">FC</span><br><b>{fc}</b></div>
                        <div><span style="color:#94A3B8; font-size:0.65rem;">GLU</span><br><b>{glu}</b></div>
                        <div><span style="color:#94A3B8; font-size:0.65rem;">IMC</span><br><b>{imc}</b></div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # AI Analysis
    ai = consultation.get('ai_analysis')
    if ai and ai != "N/A":
        with st.expander("🤖 Ver Análisis de IA"):
            st.markdown(ai)
    else:
        c1, _ = st.columns([1, 4])
        if c1.button("⚡ Analizar", key=f"ai_{consultation.get('id', 'x')}", type="secondary"):
            on_ai_click(consultation['id'])

def render_about_section():
    """Sección Acerca de - Interactiva con métricas."""
    st.markdown("""
        <div style="text-align:center; padding:2rem 0;">
            <h2 style="color:#0066FF; margin-bottom:0.5rem;">🩺 SaludIA</h2>
            <p style="color:#64748B; font-size:1rem;">Sistema de Soporte a la Decisión Clínica</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Métricas en lugar de texto
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("""
            <div style="text-align:center; background:white; padding:1rem; border-radius:12px; border:1px solid #E2E8F0;">
                <div style="font-size:2rem;">🧠</div>
                <div style="font-weight:700; color:#0F172A;">IA Gemini</div>
                <div style="font-size:0.8rem; color:#64748B;">Análisis clínico</div>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
            <div style="text-align:center; background:white; padding:1rem; border-radius:12px; border:1px solid #E2E8F0;">
                <div style="font-size:2rem;">📊</div>
                <div style="font-weight:700; color:#0F172A;">Visualización</div>
                <div style="font-size:0.8rem; color:#64748B;">Tendencias vitales</div>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
            <div style="text-align:center; background:white; padding:1rem; border-radius:12px; border:1px solid #E2E8F0;">
                <div style="font-size:2rem;">📄</div>
                <div style="font-weight:700; color:#0F172A;">PDF</div>
                <div style="font-size:0.8rem; color:#64748B;">Reportes y recetas</div>
            </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown("""
            <div style="text-align:center; background:white; padding:1rem; border-radius:12px; border:1px solid #E2E8F0;">
                <div style="font-size:2rem;">🔒</div>
                <div style="font-weight:700; color:#0F172A;">Seguro</div>
                <div style="font-size:0.8rem; color:#64748B;">Datos en Firebase</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Créditos compactos
    st.markdown("""
        <div style="text-align:center; color:#94A3B8; font-size:0.85rem;">
            <p>Desarrollado por <b>Joseph Javier Sánchez Acuña</b> | CEO de SAVA</p>
            <p>Universidad de los Andes | 2024</p>
        </div>
    """, unsafe_allow_html=True)

# Aliases
render_kpi_card = card_metric
render_patient_list_item = render_patient_card_item
