# -*- coding: utf-8 -*-
"""
Módulo de Utilidades de Gemini AI - v2.0 (Deep Diagnostic Logic)
Descripción: Lógica avanzada para diagnóstico diferencial, análisis de documentos
y predicción de riesgo clínico.
"""
import streamlit as st
import google.generativeai as genai
import logging
import time
from pypdf import PdfReader
from io import BytesIO

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiUtils:
    def __init__(self):
        self.api_key = st.secrets.get('gemini_api_key')
        if not self.api_key:
            # Fallback seguro por si no hay secrets (evita crash inmediato)
            return 
        
        genai.configure(api_key=self.api_key)
        self.model = self._get_available_model()

    def _get_available_model(self):
        # Priorizar modelos capaces de razonamiento complejo y multimodal
        model_list = [
            "gemini-1.5-pro", # Mejor para documentos/contexto largo
            "gemini-1.5-flash",
            "gemini-pro"
        ]
        
        for model_name in model_list:
            try:
                model = genai.GenerativeModel(model_name)
                # Test de conexión rápido
                # model.generate_content("Ping") 
                # (Comentado para no gastar cuota/tiempo en init, confiamos en la instanciación)
                return model
            except Exception:
                continue
        return None

    def extract_text_from_pdf(self, uploaded_file):
        """Extrae texto de un archivo PDF en memoria."""
        try:
            reader = PdfReader(uploaded_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            return f"[Error leyendo PDF: {e}]"

    def analyze_clinical_document(self, text_content):
        """Analiza texto de laboratorios/imágenes para encontrar anomalías."""
        if not self.model: return "IA no configurada."
        
        prompt = f"""
        **ACTÚA COMO UN PATÓLOGO CLIÍNICO SENIOR.**
        Analiza el siguiente texto extraído de un reporte de laboratorio/imagenología:
        
        "{text_content[:8000]}" ... (truncado si es muy largo)
        
        **TAREA:**
        1. Identifica TODOS los valores fuera de rango o hallazgos anormales.
        2. Para cada anomalía, explica brevemente su posible significado clínico en un contexto general.
        3. Si todo parece normal, indícalo claramente.
        
        Salida en formato Markdown conciso.
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error analizando documento: {e}"

    @st.cache_data(show_spinner=False, ttl=600)
    def generate_ai_holistic_review(_self, patient_info, latest_consultation, history_summary):
        """
        Genera un diagnóstico diferencial probabilístico de alto nivel.
        """
        if not _self.model:
            return "⚠️ Error: Modelo de IA no conectado. Verifique API Key."

        # Construcción de contexto clínico rico
        prompt = f"""
        **ROL:** Eres un ESPECIALISTA EN MEDICINA INTERNA de clase mundial (tipo Dr. House pero empático).
        Tu trabajo no es solo resumir, sino **PREDECIR y DIAGNOSTICAR**.
        
        **PACIENTE:**
        - Nombre: {patient_info.get('nombre', 'N/A')} | Edad: {patient_info.get('edad', '?')} años.
        
        **CONSULTA ACTUAL:**
        - Motivo: "{latest_consultation.get('motivo_consulta', 'N/A')}"
        - Vitales: PA {latest_consultation.get('presion_sistolica')}/{latest_consultation.get('presion_diastolica')}, FC {latest_consultation.get('frec_cardiaca')}, Glu {latest_consultation.get('glucemia')}, IMC {latest_consultation.get('imc')}.
        - Síntomas: {latest_consultation.get('sintomas_cardio')} / {latest_consultation.get('sintomas_resp')}.
        
        **HISTORIAL PREVIO (Resumen):**
        {history_summary}
        
        **INSTRUCCIONES DE RESPUESTA ("The Clinical Insight"):**
        Usa formato Markdown profesional.
        
        1.  **🔍 HIPÓTESIS DIAGNÓSTICA PRINCIPAL (Probabilidad Alta):**
            *   Da un diagnóstico claro. Justifica con los signos/síntomas presentes.
            *   *Ejemplo: "Insuficiencia Cardíaca Descompensada (NYHA II) debido a..."*
            
        2.  **⚖️ DIAGNÓSTICOS DIFERENCIALES (Barajar opciones):**
            *   Lista 2-3 alternativas plausibles y por qué se deben descartar o considerar.
            
        3.  **🔮 PREDICCIÓN DE RIESGO (Machine Learning Style Logic):**
            *   Estima el riesgo de complicaciones a 30 días (Bajo/Medio/Alto).
            *   Menciona qué "Red Flag" activó esta alerta (ej. Hipertensión sostenida + Disnea).
            
        4.  **💊 CONDUCTA MÉDICA RECOMENDADA:**
            *   **Laboratorios a pedir:** (Sé específico).
            *   **Tratamiento Inicial:** (Principio activo y mecanismo, NO dosis específicas por seguridad).
            *   **Recomendaciones para el Paciente:** (Estilo de vida).

        Sé directo, técnico pero claro.
        """
        
        try:
            response = _self.model.generate_content(
                prompt,
                generation_config={"temperature": 0.2} # Temperatura baja para precisión médica
            )
            return response.text
        except Exception as e:
            return f"Error en razonamiento clínico: {e}"
