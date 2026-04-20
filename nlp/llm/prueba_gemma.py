import pandas as pd
import requests
import json
import time
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]
SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUTS_DIR = SCRIPT_DIR / 'outputs'
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

# ==========================================
# 1. CARGA DE DATOS Y CONSTRUCCIÓN DE REGLAS
# ==========================================
print("Cargando datasets...")
# Rutas a tus archivos en la máquina virtual
ruta_corpus = ROOT_DIR / 'data' / 'corpus' / 'master_corpus_mixto_1000_clean_enriched.csv'
ruta_pbs = ROOT_DIR / 'corpus_PB' / 'data' / 'pb_reference.csv'

try:
    df_corpus = pd.read_csv(ruta_corpus)
    df_pbs = pd.read_csv(ruta_pbs)
except FileNotFoundError as e:
    print(f"Error fatal: No se encontró el archivo. {e}")
    exit()

# Inyectamos tu inteligencia institucional (CSV de reglas) en el prompt
pb_rules = ""
for index, row in df_pbs.iterrows():
    pb_rules += f"- PB Code: {row['pb_code']} ({row['pb_name']})\n"
    pb_rules += f"  * Core Definition: {row['short_definition']}\n"
    pb_rules += f"  * UPV Context: Look for terms like: {row['applied_keywords_upv']}\n"
    pb_rules += f"  * ACTIVATION LOGIC: {row['activation_logic']}\n"
    pb_rules += f"  * EXCLUSION RULE (CRITICAL): {row['exclusion_notes']}\n\n"

# ==========================================
# 2. CONFIGURACIÓN DEL LLM LOCAL (OLLAMA)
# ==========================================
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma4:26b"

def classify_abstract_strict(abstract_text):
    # NUEVO PROMPT: Similitud estricta + Evaluación de Confianza (Confidence Score)
    prompt = f"""You are a strict and precise scientific evaluator analyzing research abstracts from the Universitat Politècnica de València (UPV) against the Planetary Boundaries (PBs) framework.

Your task is to find the PB with the HIGHEST conceptual similarity to the abstract. You must strictly apply the activation rules and evaluate the exclusion rules. Do not force a match if the scientific connection is weak.

### PLANETARY BOUNDARIES RULES:
{pb_rules}

### ABSTRACT TO EVALUATE:
"{abstract_text}"

### INSTRUCTIONS:
Step 1: Concept Extraction. Identify the core scientific concepts, phenomena, or metrics in the abstract.
Step 2: Similarity Matching. Compare these concepts against the Core Definition and Activation Logic of each PB. Select the PB(s) with the strongest scientific overlap.
Step 3: Exclusion Check. Apply the EXCLUSION RULE. If the rule is explicitly violated, the PB MUST be discarded.
Step 4: Output the final decision in JSON format EXACTLY as follows. You must include a "confidence" score (High, Medium, or Low) evaluating how strong the match is.

{{
    "reasoning_process": "Analyze the similarity and evaluate the exclusion rules to justify your decision.",
    "assigned_pbs": [
        {{
            "pb_code": "PB1",
            "reason": "Justify why this is the highest similarity match.",
            "confidence": "High / Medium / Low"
        }}
    ]
}}
If no PB meets the criteria after applying the strict rules, return {{"reasoning_process": "Explain why similarities were too weak or excluded...", "assigned_pbs": []}}.
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.0, # Determinismo puro: el modelo será estricto y analítico
            "top_p": 0.9
        }
    }

    start_time = time.time()
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        result_json = response.json()
        
        llm_response_text = result_json.get("response", "{}")
        eval_time = time.time() - start_time
        return llm_response_text, eval_time
    except Exception as e:
        return json.dumps({"error": str(e)}), time.time() - start_time

# ==========================================
# EXTRAE EL JSON (AHORA INCLUYE CONFIDENCE)
# ==========================================
def parse_llm_output(raw_text):
    try:
        # Buscamos la primera llave '{' y la última llave '}'
        start_idx = raw_text.find('{')
        end_idx = raw_text.rfind('}')
        
        if start_idx != -1 and end_idx != -1:
            # Recortamos estrictamente el bloque JSON
            json_str = raw_text[start_idx:end_idx+1]
            data = json.loads(json_str)
        else:
            raise ValueError("No se encontró estructura JSON en la respuesta.")
        
        reasoning = data.get("reasoning_process", "")
        assigned_pbs = data.get("assigned_pbs", [])
        
        if not assigned_pbs or len(assigned_pbs) == 0:
            return reasoning, "None", "N/A" # Retorna "N/A" en confianza si no hay PB
        else:
            pb_codes_str = ", ".join([item.get("pb_code", "") for item in assigned_pbs])
            # Extraemos la confianza (si por algún motivo el modelo olvida ponerlo, dirá "Unknown")
            confidence_str = ", ".join([item.get("confidence", "Unknown") for item in assigned_pbs])
            
            return reasoning, pb_codes_str, confidence_str
    except Exception as e:
        return f"Error procesando JSON: {e}", "Error_Formato", "Error"

# ==========================================
# 3. BUCLE DE EVALUACIÓN
# ==========================================
sample_size = 5  # Abstracts a procesar (para pruebas rápidas, luego sube a 50 o 1000)
df_sample = df_corpus.head(sample_size).copy()

resultados_raw = []
resultados_reasoning = []
resultados_codes = []
resultados_confidence = [] # NUEVA LISTA para guardar el score
tiempos_inferencia = []

print(f"\nIniciando evaluación ESTRICTA con el modelo: {MODEL_NAME}")
print("-" * 70)

for index, row in df_sample.iterrows():
    print(f"Procesando Abstract {index + 1}/{sample_size} (Doc ID: {row['doc_id']})...", end=" ", flush=True)
    
    llm_out, t_elapsed = classify_abstract_strict(row['clean_abstract'])
    
    # Ahora la función devuelve 3 valores
    reasoning, codes, confidence = parse_llm_output(llm_out)
    
    resultados_raw.append(llm_out)
    resultados_reasoning.append(reasoning)
    resultados_codes.append(codes)
    resultados_confidence.append(confidence)
    tiempos_inferencia.append(t_elapsed)
    
    # Imprimimos también el nivel de confianza en tiempo real
    print(f"[{t_elapsed:.2f}s] -> PBs: {codes} | Confianza: {confidence}")

# ==========================================
# 4. GUARDAR RESULTADOS PARA ANÁLISIS
# ==========================================
df_sample['llm_raw_output'] = resultados_raw
df_sample['llm_reasoning'] = resultados_reasoning
df_sample['llm_predicted_pbs'] = resultados_codes 
df_sample['llm_confidence'] = resultados_confidence # NUEVA COLUMNA en tu CSV
df_sample['inference_time_sec'] = tiempos_inferencia

# Reordenamos columnas para la vista en Excel, poniendo la confianza junto al PB
cols_to_front = ['doc_id', 'llm_predicted_pbs', 'llm_confidence', 'llm_reasoning', 'clean_abstract']
remaining_cols = [c for c in df_sample.columns if c not in cols_to_front]
df_sample = df_sample[cols_to_front + remaining_cols]

output_filename = OUTPUTS_DIR / f'eval_{MODEL_NAME.replace(":", "_")}_strict_confidence.csv'
df_sample.to_csv(output_filename, index=False)

print("\n" + "=" * 70)
print(f"✅ Completado. Tiempo medio por abstract: {sum(tiempos_inferencia)/len(tiempos_inferencia):.2f} segundos.")
print(f"📄 Resultados guardados listos para revisar en: {output_filename}")