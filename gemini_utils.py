# -*- coding: utf-8 -*-
"""
Módulo de Utilidades de Gemini AI - v4.0 (Latest Models Dec 2024)
Lista actualizada de modelos disponibles en la API de Google Generative AI.
"""
import streamlit as st
import google.generativeai as genai
import logging
import time
from pypdf import PdfReader
from google.api_core import exceptions

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiUtils:
    def __init__(self):
        self.api_key = st.secrets.get('gemini_api_key')
        if not self.api_key:
            logger.error("API Key no encontrada.")
            return 
        
        genai.configure(api_key=self.api_key)
        
        # MODELOS ACTUALIZADOS DICIEMBRE 2024
        # Basado en: https://ai.google.dev/gemini-api/docs/models/gemini
        self.models_priority = [
            "gemini-flash-latest",      # Alias oficial de Google: siempre apunta al Flash vigente
            "gemini-flash-lite-latest", # Alias oficial: Flash-Lite vigente (fallback)
        ]
        self.model = None
        self._init_best_model()

    def _init_best_model(self):
        """Intenta inicializar el mejor modelo disponible."""
        for model_name in self.models_priority:
            try:
                self.model = genai.GenerativeModel(model_name)
                # Quick test
                self.model.generate_content("test", generation_config={'max_output_tokens': 5})
                logger.info(f"✅ Modelo activo: {model_name}")
                self.active_model_name = model_name
                return
            except Exception as e:
                logger.warning(f"❌ {model_name}: {str(e)[:60]}")
                continue
        
        logger.error("No se pudo conectar a ningún modelo de IA.")
        self.model = None

    def _generate_with_fallback(self, prompt, config=None):
        """Genera contenido con fallback automático entre modelos."""
        if not self.model:
            return "⚠️ Servicio de IA no disponible. Verifique su API Key."

        for model_name in self.models_priority:
            try:
                active = genai.GenerativeModel(model_name)
                response = active.generate_content(prompt, generation_config=config)
                return response.text
            except exceptions.ResourceExhausted:
                logger.warning(f"429 en {model_name}, probando siguiente...")
                time.sleep(0.5)
                continue
            except Exception as e:
                logger.warning(f"Error en {model_name}: {str(e)[:50]}")
                continue
        
        return "⚠️ Todos los modelos están saturados. Intente en 1 minuto."

    def extract_text_from_pdf(self, uploaded_file):
        try:
            reader = PdfReader(uploaded_file)
            return "\n".join([p.extract_text() or "" for p in reader.pages])
        except Exception as e:
            return f"[Error leyendo PDF: {e}]"

    def analyze_clinical_document(self, text_content):
        prompt = f"""Analiza este reporte médico y lista SOLO los hallazgos anormales:

{text_content[:8000]}

Formato: - ⚠️ [Hallazgo]: [Interpretación breve]
Si todo es normal: "✅ Sin hallazgos patológicos"
"""
        return self._generate_with_fallback(prompt)

    @st.cache_data(show_spinner=False, ttl=600)
    def generate_ai_holistic_review(_self, patient_info, latest_consultation, history_summary):
        prompt = f"""**CASO CLÍNICO:**
Paciente: {patient_info.get('nombre', 'N/A')} ({patient_info.get('edad', '?')} años)
Consulta: {latest_consultation.get('motivo_consulta', 'Sin datos')}
Signos: PA {latest_consultation.get('presion_sistolica')}/{latest_consultation.get('presion_diastolica')}, Glu {latest_consultation.get('glucemia')}

**HISTORIAL:** {history_summary}

**RESPONDE COMO MÉDICO INTERNISTA:**
1. **Diagnóstico Probable:** (Justificación breve)
2. **Riesgo:** (Bajo/Medio/Alto)
3. **Plan:** 3 acciones concretas
"""
        config = genai.types.GenerationConfig(temperature=0.3, max_output_tokens=1024)
        return _self._generate_with_fallback(prompt, config)
