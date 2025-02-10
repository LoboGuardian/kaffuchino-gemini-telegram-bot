# gemini/models.py
import google.generativeai as genai

try:
    model_list = genai.list_models() # Llama a la función para listar modelos
    import pprint
    for model in genai.list_models():
        pprint.pprint(model)

except Exception as e:
    print(f"Error al listar modelos: {e}")