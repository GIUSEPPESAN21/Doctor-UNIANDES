# -*- coding: utf-8 -*-
"""
Módulo de Componentes de Interfaz de Usuario (UI) - v5.0 PREMIUM
Diseño Ultra-Profesional con animaciones, glassmorphism y micro-interacciones.
"""
import streamlit as st
import pandas as pd

# ==============================================================================
# CSS PREMIUM - DISEÑO MÉDICO DE CLASE MUNDIAL
# ==============================================================================
def load_custom_css():
    """Inyecta CSS ultra-premium para una experiencia clínica de elite."""
    st.markdown("""
        <style>
        /* === IMPORTAR FUENTES PREMIUM === */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
        
        /* === VARIABLES CSS (Design Tokens) === */
        :root {
            /* Paleta Médica Premium */
            --primary: #0066FF;
            --primary-dark: #0052CC;
            --primary-light: #E6F0FF;
            --primary-glow: rgba(0, 102, 255, 0.15);
            
            --success: #00C853;
            --success-light: #E8F5E9;
            --warning: #FF9800;
            --warning-light: #FFF3E0;
            --danger: #F44336;
            --danger-light: #FFEBEE;
            
            /* Neutros */
            --bg-primary: #F8FAFC;
            --bg-secondary: #FFFFFF;
            --bg-tertiary: #F1F5F9;
            --text-primary: #0F172A;
            --text-secondary: #64748B;
            --text-muted: #94A3B8;
            --border: #E2E8F0;
            --border-focus: #0066FF;
            
            /* Efectos */
            --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.04);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.07), 0 2px 4px -1px rgba(0, 0, 0, 0.04);
            --shadow-lg: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.04);
            --shadow-glow: 0 0 20px var(--primary-glow);
            
            --radius-sm: 8px;
            --radius-md: 12px;
            --radius-lg: 16px;
            --radius-xl: 24px;
            
            --transition-fast: 150ms ease;
            --transition-base: 250ms ease;
            --transition-slow: 350ms ease;
        }

        /* === RESET Y BASE === */
        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            color: var(--text-primary);
            background: var(--bg-primary) !important;
            -webkit-font-smoothing: antialiased;
        }
        
        .stApp {
            background: linear-gradient(135deg, #F8FAFC 0%, #EEF2FF 50%, #F0F9FF 100%) !important;
        }

        /* === TIPOGRAFÍA === */
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-weight: 700;
            letter-spacing: -0.02em;
            color: var(--text-primary);
        }
        
        h1 {
            font-size: 2.25rem !important;
            font-weight: 800 !important;
            background: linear-gradient(135deg, #0066FF 0%, #00C2FF 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        h2 { font-size: 1.5rem !important; }
        h3 { font-size: 1.25rem !important; }
        
        p, span, label, div {
            font-size: 0.9375rem;
            line-height: 1.6;
        }

        /* === ANIMACIONES === */
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.02); }
        }
        
        @keyframes shimmer {
            0% { background-position: -200% 0; }
            100% { background-position: 200% 0; }
        }
        
        .main > div {
            animation: fadeInUp 0.5s ease-out forwards;
        }

        /* === TARJETAS PREMIUM (Cards) === */
        .card-container, .medical-card {
            background: var(--bg-secondary);
            border-radius: var(--radius-lg);
            padding: 1.5rem;
            border: 1px solid var(--border);
            box-shadow: var(--shadow-md);
            transition: all var(--transition-base);
            position: relative;
            overflow: hidden;
        }
        
        .card-container::before, .medical-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--primary), #00C2FF);
            opacity: 0;
            transition: opacity var(--transition-base);
        }
        
        .card-container:hover, .medical-card:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-lg);
            border-color: var(--primary-light);
        }
        
        .card-container:hover::before, .medical-card:hover::before {
            opacity: 1;
        }

        /* === BADGES PREMIUM === */
        .badge {
            display: inline-flex;
            align-items: center;
            gap: 4px;
            padding: 4px 12px;
            border-radius: 999px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.03em;
            transition: all var(--transition-fast);
        }
        
        .badge-blue {
            background: var(--primary-light);
            color: var(--primary);
        }
        
        .badge-green {
            background: var(--success-light);
            color: var(--success);
        }
        
        .badge-red {
            background: var(--danger-light);
            color: var(--danger);
        }
        
        .badge-warning {
            background: var(--warning-light);
            color: var(--warning);
        }

        /* === BOTONES PREMIUM === */
        div[data-testid="stButton"] > button {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-weight: 600;
            border-radius: var(--radius-md);
            padding: 0.625rem 1.25rem;
            font-size: 0.875rem;
            transition: all var(--transition-base);
            border: none;
            cursor: pointer;
        }
        
        div[data-testid="stButton"] > button[kind="primary"] {
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
            color: white;
            box-shadow: 0 4px 14px rgba(0, 102, 255, 0.35);
        }
        
        div[data-testid="stButton"] > button[kind="primary"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 102, 255, 0.45);
        }
        
        div[data-testid="stButton"] > button[kind="secondary"] {
            background: var(--bg-tertiary);
            color: var(--text-primary);
            border: 1px solid var(--border);
        }
        
        div[data-testid="stButton"] > button[kind="secondary"]:hover {
            background: var(--primary-light);
            border-color: var(--primary);
            color: var(--primary);
        }

        /* === INPUTS PREMIUM === */
        div[data-testid="stTextInput"] input,
        div[data-testid="stNumberInput"] input,
        div[data-testid="stTextArea"] textarea {
            font-family: 'Plus Jakarta Sans', sans-serif;
            border-radius: var(--radius-md) !important;
            border: 2px solid var(--border) !important;
            padding: 0.75rem 1rem !important;
            font-size: 0.9375rem !important;
            transition: all var(--transition-base) !important;
            background: var(--bg-secondary) !important;
        }
        
        div[data-testid="stTextInput"] input:focus,
        div[data-testid="stNumberInput"] input:focus,
        div[data-testid="stTextArea"] textarea:focus {
            border-color: var(--primary) !important;
            box-shadow: 0 0 0 3px var(--primary-glow) !important;
            outline: none !important;
        }

        /* === TABS PREMIUM === */
        button[data-baseweb="tab"] {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-weight: 600;
            font-size: 0.875rem;
            padding: 0.75rem 1.5rem;
            border-radius: var(--radius-md) var(--radius-md) 0 0;
            transition: all var(--transition-base);
        }
        
        button[data-baseweb="tab"][aria-selected="true"] {
            background: var(--bg-secondary);
            color: var(--primary);
            border-bottom: 3px solid var(--primary);
        }

        /* === EXPANDER PREMIUM === */
        div[data-testid="stExpander"] {
            border-radius: var(--radius-md);
            border: 1px solid var(--border);
            background: var(--bg-secondary);
            overflow: hidden;
        }
        
        div[data-testid="stExpander"] summary {
            font-weight: 600;
            padding: 1rem;
        }

        /* === DIVIDER === */
        hr {
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, var(--border), transparent);
            margin: 1.5rem 0;
        }

        /* === METRIC CARDS === */
        div[data-testid="metric-container"] {
            background: var(--bg-secondary);
            padding: 1rem;
            border-radius: var(--radius-md);
            border: 1px solid var(--border);
        }

        /* === SCROLLBAR CUSTOM === */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: var(--bg-tertiary);
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: var(--text-muted);
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: var(--text-secondary);
        }

        /* === TOAST/ALERTS === */
        div[data-testid="stAlert"] {
            border-radius: var(--radius-md);
            border-left: 4px solid;
        }

        /* === TIMELINE STYLES === */
        .timeline-container {
            position: relative;
            padding-left: 30px;
        }
        
        .timeline-line {
            position: absolute;
            left: 6px;
            top: 0;
            bottom: 0;
            width: 2px;
            background: linear-gradient(180deg, var(--primary), var(--primary-light));
        }
        
        .timeline-dot {
            position: absolute;
            left: 0;
            width: 14px;
            height: 14px;
            background: var(--primary);
            border: 3px solid var(--bg-secondary);
            border-radius: 50%;
            box-shadow: 0 0 0 3px var(--primary-light);
        }

        /* === GLASSMORPHISM EFFECT === */
        .glass-card {
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.3);
        }

        /* === LOADING SKELETON === */
        .skeleton {
            background: linear-gradient(90deg, var(--bg-tertiary) 25%, var(--bg-secondary) 50%, var(--bg-tertiary) 75%);
            background-size: 200% 100%;
            animation: shimmer 1.5s infinite;
            border-radius: var(--radius-sm);
        }
        </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# COMPONENTES VISUALES PREMIUM
# ==============================================================================

def render_hero_header(physician_email):
    """Encabezado Hero premium con gradiente animado."""
    name = physician_email.split('@')[0].title() if physician_email else "Doctor"
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #0066FF 0%, #00C2FF 50%, #0066FF 100%);
            background-size: 200% 200%;
            animation: gradient 8s ease infinite;
            padding: 2rem;
            border-radius: 20px;
            color: white;
            margin-bottom: 1.5rem;
            box-shadow: 0 10px 40px rgba(0, 102, 255, 0.3);
            position: relative;
            overflow: hidden;
        ">
            <div style="position: relative; z-index: 1;">
                <p style="margin: 0; font-size: 0.875rem; opacity: 0.9; font-weight: 500;">👋 Bienvenido de nuevo</p>
                <h2 style="margin: 0.5rem 0 0 0; font-size: 1.75rem; font-weight: 800; color: white;">Dr. {name}</h2>
                <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; opacity: 0.85;">Panel de Control Clínico | SaludIA</p>
            </div>
            <div style="position: absolute; right: 20px; top: 50%; transform: translateY(-50%); font-size: 4rem; opacity: 0.2;">🩺</div>
        </div>
        <style>
            @keyframes gradient {{
                0% {{ background-position: 0% 50%; }}
                50% {{ background-position: 100% 50%; }}
                100% {{ background-position: 0% 50%; }}
            }}
        </style>
    """, unsafe_allow_html=True)

def card_metric(label, value, delta=None, color_hex="#0066FF"):
    """Tarjeta de métrica KPI premium con animación."""
    delta_html = f"""
        <div style="
            display: inline-flex;
            align-items: center;
            gap: 4px;
            font-size: 0.8rem;
            color: #00C853;
            margin-top: 8px;
            font-weight: 600;
        ">
            <span>▲</span> {delta}
        </div>
    """ if delta else ""
    
    st.markdown(f"""
        <div style="
            background: white;
            padding: 1.25rem;
            border-radius: 16px;
            border: 1px solid #E2E8F0;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            border-left: 4px solid {color_hex};
            transition: all 0.25s ease;
            cursor: default;
        " onmouseover="this.style.transform='translateY(-3px)';this.style.boxShadow='0 10px 25px -5px rgba(0,0,0,0.1)';"
           onmouseout="this.style.transform='translateY(0)';this.style.boxShadow='0 4px 6px -1px rgba(0,0,0,0.05)';">
            <div style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; color: #64748B; font-weight: 600;">{label}</div>
            <div style="font-size: 2rem; font-weight: 800; color: #0F172A; line-height: 1.2; margin-top: 4px;">{value}</div>
            {delta_html}
        </div>
    """, unsafe_allow_html=True)

def render_patient_card_item(patient, on_click):
    """Tarjeta de paciente interactiva con hover effect."""
    with st.container():
        st.markdown(f"""
            <div style="
                background: white;
                padding: 1rem 1.25rem;
                border-radius: 12px;
                border: 1px solid #E2E8F0;
                margin-bottom: 0.75rem;
                transition: all 0.2s ease;
                cursor: pointer;
            " onmouseover="this.style.borderColor='#0066FF';this.style.boxShadow='0 4px 12px rgba(0,102,255,0.1)';"
               onmouseout="this.style.borderColor='#E2E8F0';this.style.boxShadow='none';">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-weight: 700; font-size: 1rem; color: #0F172A;">{patient['nombre']}</div>
                        <div style="font-size: 0.8rem; color: #64748B; margin-top: 2px;">ID: {patient['cedula']}</div>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="background: #E6F0FF; color: #0066FF; padding: 4px 10px; border-radius: 999px; font-size: 0.75rem; font-weight: 600;">{patient.get('edad', '?')} años</span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Botón invisible que cubre la tarjeta
        if st.button("Ver →", key=f"p_btn_{patient['id']}", type="secondary", use_container_width=True):
            on_click(patient['id'])

def render_consultation_timeline_item(consultation, on_ai_click):
    """Timeline item premium con diseño de línea de tiempo elegante."""
    # Parseo seguro de fecha
    ts = consultation.get('timestamp')
    try:
        if ts is None or (isinstance(ts, float) and pd.isna(ts)) or str(ts) == 'NaT':
            date_str = "Fecha no registrada"
        elif hasattr(ts, 'strftime'):
            date_str = ts.strftime('%d %b %Y • %H:%M')
        else:
            date_str = str(ts)[:16]
    except:
        date_str = "Fecha desconocida"
    
    # Badges de riesgo
    badges_html = ""
    try:
        bp_sist = int(consultation.get('presion_sistolica', 0) or 0)
        if bp_sist >= 140:
            badges_html += """<span style="background:#FFEBEE; color:#F44336; padding:3px 10px; border-radius:999px; font-size:0.7rem; font-weight:600;">⚠️ HIPERTENSIÓN</span>"""
        elif 0 < bp_sist < 90:
            badges_html += """<span style="background:#FFF3E0; color:#FF9800; padding:3px 10px; border-radius:999px; font-size:0.7rem; font-weight:600;">⚡ HIPOTENSIÓN</span>"""
    except: pass
    
    # Síntomas
    symptoms_parts = []
    for k in ['sintomas_cardio', 'sintomas_resp', 'sintomas_gi', 'sintomas_neuro']:
        val = consultation.get(k)
        if isinstance(val, list) and val:
            symptoms_parts.extend(val)
    symptoms_html = ", ".join(symptoms_parts[:4]) if symptoms_parts else ""
    
    # Motivo truncado
    motivo = str(consultation.get('motivo_consulta', 'Sin motivo'))[:100]
    if len(str(consultation.get('motivo_consulta', ''))) > 100:
        motivo += "..."

    st.markdown(f"""
        <div style="
            position: relative;
            padding-left: 35px;
            margin-bottom: 1.5rem;
        ">
            <!-- Línea vertical -->
            <div style="
                position: absolute;
                left: 5px;
                top: 20px;
                bottom: -20px;
                width: 2px;
                background: linear-gradient(180deg, #0066FF 0%, #E6F0FF 100%);
            "></div>
            
            <!-- Punto -->
            <div style="
                position: absolute;
                left: 0;
                top: 4px;
                width: 12px;
                height: 12px;
                background: #0066FF;
                border: 3px solid white;
                border-radius: 50%;
                box-shadow: 0 0 0 3px #E6F0FF;
            "></div>
            
            <!-- Contenido -->
            <div style="
                background: white;
                border: 1px solid #E2E8F0;
                border-radius: 12px;
                padding: 1.25rem;
                box-shadow: 0 2px 8px rgba(0,0,0,0.04);
                transition: all 0.2s ease;
            ">
                <!-- Header -->
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 12px;">
                    <div>
                        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; color: #64748B; font-weight: 600;">{date_str}</div>
                        <div style="font-size: 1rem; font-weight: 700; color: #0F172A; margin-top: 4px;">{motivo}</div>
                        {"<div style='font-size: 0.8rem; color: #94A3B8; margin-top: 4px;'>📋 " + symptoms_html + "</div>" if symptoms_html else ""}
                    </div>
                    <div>{badges_html}</div>
                </div>
                
                <!-- Vitales Grid -->
                <div style="
                    display: grid;
                    grid-template-columns: repeat(4, 1fr);
                    gap: 10px;
                    background: #F8FAFC;
                    padding: 12px;
                    border-radius: 10px;
                    text-align: center;
                ">
                    <div>
                        <div style="font-size: 0.65rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em;">Presión</div>
                        <div style="font-size: 0.95rem; font-weight: 700; color: #0F172A;">{consultation.get('presion_sistolica', 'N/A')}/{consultation.get('presion_diastolica', 'N/A')}</div>
                    </div>
                    <div>
                        <div style="font-size: 0.65rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em;">FC</div>
                        <div style="font-size: 0.95rem; font-weight: 700; color: #0F172A;">{consultation.get('frec_cardiaca', 'N/A')}</div>
                    </div>
                    <div>
                        <div style="font-size: 0.65rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em;">Glucemia</div>
                        <div style="font-size: 0.95rem; font-weight: 700; color: #0F172A;">{consultation.get('glucemia', 'N/A')}</div>
                    </div>
                    <div>
                        <div style="font-size: 0.65rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em;">IMC</div>
                        <div style="font-size: 0.95rem; font-weight: 700; color: #0F172A;">{consultation.get('imc', 'N/A')}</div>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # AI Analysis
    ai_report = consultation.get('ai_analysis')
    if ai_report and ai_report != "N/A":
        with st.expander("🤖 Ver Análisis de IA", expanded=False):
            st.markdown(ai_report)
    else:
        col1, _ = st.columns([1, 4])
        if col1.button("⚡ Analizar", key=f"ai_btn_{consultation.get('id', 'x')}", type="secondary"):
            on_ai_click(consultation['id'])

# Aliases para compatibilidad
render_kpi_card = card_metric
render_patient_list_item = render_patient_card_item
