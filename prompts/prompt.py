import pandas as pd

# 1. Cargar los datos (asegúrate de que los nombres de archivo son correctos)
try:
    df_corpus = pd.read_csv('data/corpus/master_corpus_mixto_1000_clean_enriched.csv')
    df_pbs = pd.read_csv('/home/sortmon/UPV_EARTH_PROYECTOIII/corpus_PB/data/pb_reference.csv')
except FileNotFoundError as e:
    print(f"Error al cargar archivos: {e}")
    exit()

# 2. Extraer un abstract de prueba (cogemos el primero, índice 0)
# Puedes cambiar el 0 por otro número para ver diferentes abstracts
abstract_de_prueba = df_corpus['clean_abstract'].iloc[0]

# 3. Construir las reglas dinámicas desde el CSV de los PBs
pb_rules = ""
for index, row in df_pbs.iterrows():
    pb_rules += f"- PB Code: {row['pb_code']} ({row['pb_name']})\n"
    pb_rules += f"  * Core Definition: {row['short_definition']}\n"
    pb_rules += f"  * UPV Context: Look for terms like: {row['applied_keywords_upv']}\n"
    pb_rules += f"  * ACTIVATION LOGIC: {row['activation_logic']}\n"
    pb_rules += f"  * EXCLUSION RULE (CRITICAL): {row['exclusion_notes']}\n\n"

# 4. Construir el Prompt Final (El "Prompt Rompedor" hidratado)
prompt_final = f"""You are an expert scientific evaluator auditing research abstracts from the Universitat Politècnica de València (UPV) for their impact on Planetary Boundaries (PBs).

Your task is to analyze the abstract and strictly apply the activation and exclusion rules provided below. 
Do NOT assign a PB just because the text sounds "green" or "sustainable" (Misled by Positivity bias). You need explicit evidence.

### PLANETARY BOUNDARIES RULES:
{pb_rules}
### ABSTRACT TO EVALUATE:
"{abstract_de_prueba}"

### INSTRUCTIONS:
Step 1: Think step-by-step. Analyze if the abstract contains explicit metrics, outcomes, or core keywords related to any PB.
Step 2: Check the "EXCLUSION RULE" for that PB. Does the abstract violate the exclusion rule? If yes, discard the PB.
Step 3: Output the final decision in JSON format EXACTLY as follows:

{{
    "reasoning_process": "Your step-by-step analysis applying the activation and exclusion rules. Mention why a PB was included or discarded.",
    "assigned_pbs": [
        {{
            "pb_code": "PB1",
            "reason": "Direct quote from the text that proves the activation logic."
        }}
    ]
}}
If no PB is relevant, return {{"reasoning_process": "Explain why none apply...", "assigned_pbs": []}}.
"""

# 5. Imprimir el resultado por pantalla
print("="*80)
print("🔍 ASÍ ES EXACTAMENTE EL PROMPT QUE RECIBE EL MODELO:")
print("="*80)
print(prompt_final)
print("="*80)
print(f"Longitud total del prompt: {len(prompt_final)} caracteres (aprox {len(prompt_final)//4} tokens).")