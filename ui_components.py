# -*- coding: utf-8 -*-
"""
Módulo de Componentes UI - v7.0 POLISHED
Todas las correcciones de UI/UX aplicadas.
"""
import streamlit as st
import pandas as pd

# ==============================================================================
# CSS PREMIUM - CORREGIDO
# ==============================================================================
def load_custom_css():
    """CSS pulido con todas las correcciones."""
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
        
        :root {
            /* Paleta Médica SOBRIA - más clínica y calmada */
            --primary: #0A6DC2;           /* Azul más sobrio/profesional */
            --primary-dark: #085A9E;
            --primary-light: #E8F4FC;
            --primary-gradient: linear-gradient(135deg, #0A6DC2 0%, #0891B2 100%); /* Azul a Cian */
            
            --success: #059669;
            --warning: #D97706;
            --danger: #DC2626;
            
            --bg-primary: #F8FAFC;
            --bg-card: #FFFFFF;
            --text-primary: #1E293B;
            --text-secondary: #64748B;
            --text-muted: #94A3B8;
            --border: #E2E8F0;
            --border-focus: #0A6DC2;
            
            --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.04);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.06);
            --shadow-lg: 0 10px 25px -5px rgba(0, 0, 0, 0.08);
            
            --radius-sm: 8px;
            --radius-md: 12px;
            --radius-lg: 16px;
        }

        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            color: var(--text-primary);
            -webkit-font-smoothing: antialiased;
        }
        
        .stApp {
            background: linear-gradient(180deg, #F0F9FF 0%, #F8FAFC 100%) !important;
        }

        h1 {
            font-size: 2rem !important;
            font-weight: 800 !important;
            background: var(--primary-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        h2, h3 { font-weight: 700; color: var(--text-primary); }

        /* === TABS - Línea AZUL en vez de roja === */
        button[data-baseweb="tab"] {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-weight: 600;
            font-size: 0.875rem;
            color: var(--text-secondary);
            border-bottom: 3px solid transparent;
            transition: all 0.2s ease;
        }
        
        button[data-baseweb="tab"][aria-selected="true"] {
            color: var(--primary) !important;
            border-bottom: 3px solid var(--primary) !important;
            background: transparent !important;
        }
        
        button[data-baseweb="tab"]:hover {
            color: var(--primary);
        }
        
        /* Eliminar cualquier línea roja residual */
        div[data-baseweb="tab-highlight"] {
            background-color: var(--primary) !important;
        }
        
        div[data-baseweb="tab-border"] {
            background-color: var(--border) !important;
        }

        /* === INPUTS - Fondo BLANCO con borde suave === */
        div[data-testid="stTextInput"] input,
        div[data-testid="stNumberInput"] input,
        div[data-testid="stTextArea"] textarea,
        div[data-testid="stSelectbox"] > div > div {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            background: #FFFFFF !important;
            border: 1.5px solid var(--border) !important;
            border-radius: var(--radius-md) !important;
            padding: 0.75rem 1rem !important;
            font-size: 0.9375rem !important;
            color: var(--text-primary) !important;
            transition: all 0.2s ease !important;
        }
        
        div[data-testid="stTextInput"] input:focus,
        div[data-testid="stNumberInput"] input:focus,
        div[data-testid="stTextArea"] textarea:focus {
            border-color: var(--primary) !important;
            box-shadow: 0 0 0 3px rgba(10, 109, 194, 0.12) !important;
            outline: none !important;
        }
        
        div[data-testid="stTextInput"] input::placeholder,
        div[data-testid="stTextArea"] textarea::placeholder {
            color: var(--text-muted) !important;
        }

        /* === BOTONES === */
        div[data-testid="stButton"] > button {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-weight: 600;
            border-radius: var(--radius-md);
            transition: all 0.2s ease;
            font-size: 0.875rem;
        }
        
        div[data-testid="stButton"] > button[kind="primary"] {
            background: var(--primary-gradient);
            color: white;
            border: none;
            box-shadow: 0 4px 12px rgba(10, 109, 194, 0.25);
        }
        
        div[data-testid="stButton"] > button[kind="primary"]:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 16px rgba(10, 109, 194, 0.35);
        }
        
        /* Ghost Button - Para "Ver" */
        div[data-testid="stButton"] > button[kind="secondary"] {
            background: transparent !important;
            color: var(--primary) !important;
            border: none !important;
            padding: 0.5rem 1rem !important;
        }
        
        div[data-testid="stButton"] > button[kind="secondary"]:hover {
            background: var(--primary-light) !important;
        }

        /* === CARDS === */
        .card-container, .medical-card {
            background: var(--bg-card);
            border-radius: var(--radius-lg);
            padding: 1.5rem;
            border: 1px solid var(--border);
            box-shadow: var(--shadow-sm);
        }

        /* === BADGES === */
        .badge {
            display: inline-flex;
            align-items: center;
            padding: 4px 10px;
            border-radius: 999px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        
        .badge-blue { background: var(--primary-light); color: var(--primary); }
        .badge-green { background: #ECFDF5; color: #059669; }

        /* === Mejora general del espaciado === */
        section[data-testid="stSidebar"] { display: none; }
        
        /* Hacer que los dividers sean más sutiles */
        hr {
            border: none;
            height: 1px;
            background: var(--border);
            margin: 1.25rem 0;
        }
        </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# COMPONENTES
# ==============================================================================

def render_hero_header_with_logout(physician_email, on_logout):
    """Header Hero con logout INTEGRADO dentro de la barra azul."""
    # Limpiar nombre: quitar punto, capitalizar
    if physician_email:
        name_part = physician_email.split('@')[0]
        name_clean = name_part.replace('.', ' ').replace('_', ' ').title()
    else:
        name_clean = "Doctor"
    
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #0A6DC2 0%, #0891B2 100%);
            padding: 1.5rem 2rem;
            border-radius: 16px;
            color: white;
            margin-bottom: 1.5rem;
            box-shadow: 0 8px 30px rgba(10, 109, 194, 0.2);
            display: flex;
            justify-content: space-between;
            align-items: center;
        ">
            <div>
                <p style="margin: 0; font-size: 0.85rem; opacity: 0.9; font-weight: 500;">👋 Bienvenido de nuevo</p>
                <h2 style="margin: 0.25rem 0 0 0; font-size: 1.5rem; font-weight: 800; color: white;">Dr. {name_clean}</h2>
                <p style="margin: 0.25rem 0 0 0; font-size: 0.85rem; opacity: 0.85;">Panel de Control | SaludIA</p>
            </div>
            <div id="logout-placeholder"></div>
        </div>
    """, unsafe_allow_html=True)
    
    # Botón de logout usando Streamlit (se renderiza después del HTML)
    cols = st.columns([6, 1])
    with cols[1]:
        if st.button("🚪 Salir", key="logout_integrated", type="secondary"):
            on_logout()

def render_hero_header(physician_email):
    """Header simple sin logout."""
    if physician_email:
        name_part = physician_email.split('@')[0]
        name_clean = name_part.replace('.', ' ').replace('_', ' ').title()
    else:
        name_clean = "Doctor"
        
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #0A6DC2 0%, #0891B2 100%);
            padding: 1.5rem 2rem;
            border-radius: 16px;
            color: white;
            margin-bottom: 1.5rem;
            box-shadow: 0 8px 30px rgba(10, 109, 194, 0.2);
        ">
            <p style="margin: 0; font-size: 0.85rem; opacity: 0.9;">👋 Bienvenido de nuevo</p>
            <h2 style="margin: 0.25rem 0 0 0; font-size: 1.5rem; font-weight: 800; color: white;">Dr. {name_clean}</h2>
            <p style="margin: 0.25rem 0 0 0; font-size: 0.85rem; opacity: 0.85;">Panel de Control | SaludIA</p>
        </div>
    """, unsafe_allow_html=True)

def card_metric(label, value, delta=None, color_hex="#0A6DC2"):
    """Tarjeta KPI."""
    delta_html = f"<div style='font-size:0.8rem; color:#059669; margin-top:6px;'>▲ {delta}</div>" if delta else ""
    st.markdown(f"""
        <div style="
            background: white;
            padding: 1.25rem;
            border-radius: 14px;
            border: 1px solid #E2E8F0;
            border-left: 4px solid {color_hex};
            box-shadow: 0 2px 6px rgba(0,0,0,0.03);
        ">
            <div style="font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.05em; color: #64748B; font-weight: 600;">{label}</div>
            <div style="font-size: 1.75rem; font-weight: 800; color: #1E293B; margin-top: 4px;">{value}</div>
            {delta_html}
        </div>
    """, unsafe_allow_html=True)

def render_patient_card_item(patient, on_click):
    """Tarjeta de paciente LIMPIA - sin markdown visible."""
    # Limpiar nombre de asteriscos y markdown
    nombre = str(patient.get('nombre', 'Sin nombre'))
    nombre_limpio = nombre.replace('**', '').replace('*', '').strip()
    
    edad = patient.get('edad', '?')
    cedula = patient.get('cedula', 'N/A')
    
    with st.container():
        col1, col2, col3 = st.columns([3.5, 1.2, 0.8])
        with col1:
            st.markdown(f"""
                <div style="padding: 8px 0;">
                    <div style="font-weight: 700; font-size: 0.95rem; color: #1E293B;">{nombre_limpio}</div>
                    <div style="font-size: 0.8rem; color: #94A3B8; margin-top: 2px;">ID: {cedula}</div>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div style="display: flex; align-items: center; height: 100%; padding: 8px 0;">
                    <span style="background: #E8F4FC; color: #0A6DC2; padding: 4px 12px; border-radius: 999px; font-size: 0.75rem; font-weight: 600;">{edad} años</span>
                </div>
            """, unsafe_allow_html=True)
        with col3:
            if st.button("→", key=f"p_{patient['id']}", type="secondary", help="Ver historial"):
                on_click(patient['id'])
        
        st.markdown("<hr style='margin: 4px 0; border: 0; border-top: 1px solid #F1F5F9;'>", unsafe_allow_html=True)

def render_consultation_timeline_item(consultation, on_ai_click):
    """Timeline item limpio."""
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
            badges = "<span style='background:#FEE2E2; color:#DC2626; padding:3px 10px; border-radius:999px; font-size:0.7rem; font-weight:600;'>⚠️ HTA</span>"
        elif 0 < bp < 90:
            badges = "<span style='background:#FEF3C7; color:#D97706; padding:3px 10px; border-radius:999px; font-size:0.7rem; font-weight:600;'>⚡ Hipotensión</span>"
    except: pass
    
    # Limpiar motivo de asteriscos
    motivo_raw = str(consultation.get('motivo_consulta', 'Sin motivo'))
    motivo = motivo_raw.replace('**', '').replace('*', '')[:80]
    if len(motivo_raw) > 80:
        motivo += "..."
    
    pa_s = consultation.get('presion_sistolica', 'N/A')
    pa_d = consultation.get('presion_diastolica', 'N/A')
    fc = consultation.get('frec_cardiaca', 'N/A')
    glu = consultation.get('glucemia', 'N/A')
    imc = consultation.get('imc', 'N/A')

    st.markdown(f"""
    <div style="display: flex; gap: 15px; margin-bottom: 1.25rem;">
        <div style="width: 12px; display: flex; flex-direction: column; align-items: center;">
            <div style="width:12px; height:12px; background:#0A6DC2; border:3px solid white; border-radius:50%; box-shadow:0 0 0 3px #E8F4FC;"></div>
            <div style="width:2px; flex:1; background:linear-gradient(180deg, #0A6DC2, #E8F4FC);"></div>
        </div>
        <div style="flex:1;">
            <div style="font-size:0.8rem; color:#64748B; font-weight:600; margin-bottom:6px; font-family: monospace;">{date_str}</div>
            <div style="background: white; border: 1px solid #E2E8F0; border-radius: 12px; padding: 1rem; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
                <div style="display:flex; justify-content:space-between; align-items:start; margin-bottom:10px;">
                    <div style="font-weight:600; color:#1E293B; font-size:0.95rem;">{motivo}</div>
                    <div>{badges}</div>
                </div>
                <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; background: #F8FAFC; padding: 10px; border-radius: 8px; text-align: center; font-size: 0.85rem;">
                    <div><span style="color:#94A3B8; font-size:0.65rem; text-transform:uppercase;">PA</span><br><b style="color:#1E293B;">{pa_s}/{pa_d}</b></div>
                    <div><span style="color:#94A3B8; font-size:0.65rem; text-transform:uppercase;">FC</span><br><b style="color:#1E293B;">{fc}</b></div>
                    <div><span style="color:#94A3B8; font-size:0.65rem; text-transform:uppercase;">GLU</span><br><b style="color:#1E293B;">{glu}</b></div>
                    <div><span style="color:#94A3B8; font-size:0.65rem; text-transform:uppercase;">IMC</span><br><b style="color:#1E293B;">{imc}</b></div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    ai = consultation.get('ai_analysis')
    if ai and ai != "N/A":
        with st.expander("🤖 Ver Análisis de IA"):
            st.markdown(ai)
    else:
        c1, _ = st.columns([1, 4])
        if c1.button("⚡ Analizar", key=f"ai_{consultation.get('id', 'x')}", type="secondary"):
            on_ai_click(consultation['id'])

def render_about_section():
    """Sección Acerca de - Interactiva."""
    st.markdown("""
        <div style="text-align:center; padding:1.5rem 0;">
            <h2 style="color:#0A6DC2; margin-bottom:0.5rem;">🩺 SaludIA</h2>
            <p style="color:#64748B; font-size:1rem;">Sistema de Soporte a la Decisión Clínica</p>
        </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    features = [
        ("🧠", "IA Gemini", "Análisis clínico"),
        ("📊", "Visualización", "Tendencias vitales"),
        ("📄", "PDF", "Reportes y recetas"),
        ("🔒", "Seguro", "Datos en Firebase"),
    ]
    for col, (icon, title, desc) in zip([c1, c2, c3, c4], features):
        with col:
            st.markdown(f"""
                <div style="text-align:center; background:white; padding:1rem; border-radius:12px; border:1px solid #E2E8F0;">
                    <div style="font-size:1.75rem;">{icon}</div>
                    <div style="font-weight:700; color:#1E293B; margin-top:0.5rem;">{title}</div>
                    <div style="font-size:0.8rem; color:#64748B;">{desc}</div>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
        <div style="text-align:center; color:#94A3B8; font-size:0.85rem;">
            <p>Desarrollado por <b>Joseph Javier Sánchez Acuña</b> | CEO de SAVA</p>
            <p>Universidad de los Andes | 2024</p>
        </div>
    """, unsafe_allow_html=True)

# Aliases
render_kpi_card = card_metric
render_patient_list_item = render_patient_card_item
