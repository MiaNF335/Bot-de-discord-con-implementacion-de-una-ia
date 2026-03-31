import os 
os.environ["TF_USE_LEGACY_KERAS"] = "1" 
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 
import tf_keras as keras
from tf_keras.models import load_model 
from PIL import Image, ImageOps
import numpy as np

# Cargamos el modelo una sola vez al iniciar para que el bot sea rápido
model = load_model("keras_model.h5", compile=False)
class_names = open("labels.txt", "r").readlines()



# ... (tus otros imports y carga de modelo arriba)

colorimetry_info = {
    "winter": {
        "advice": "Opta por colores fríos, intensos y claros como el azul eléctrico, el fucsia, el blanco puro y el negro. Evita los tonos cálidos y apagados. Los contrastes fuertes te favorecen.",
        "celebrities": ["Anne Hathaway", "Salma Hayek", "Megan Fox", "Penélope Cruz"]
    },
    "autumn": {
        "advice": "Te lucen los colores cálidos, profundos y suaves de la naturaleza, como el verde oliva, el naranja óxido, el marrón chocolate, el dorado y el beige.",
        "celebrities": ["Julia Roberts", "Drew Barrymore", "Jessica Alba", "Jennifer Lopez"]
    },
    "summer": {
        "advice": "Los colores fríos, suaves y empolvados son tus aliados. Piensa en azules cielo, rosas empolvados, lavandas, grises perla y beige rosado.",
        "celebrities": ["Reese Witherspoon", "Kate Moss", "Scarlett Johansson", "Naomi Watts"]
    },
    "spring": {
        "advice": "Brilla con colores cálidos, claros y brillantes, como el melocotón, el verde manzana, el coral, el turquesa y el amarillo dorado.",
        "celebrities": ["Blake Lively", "Taylor Swift", "Emma Stone", "Amy Adams"]
    }
}

def analizar_colorimetria(ruta_imagen):
    """
    Recibe la ruta de una imagen, la procesa y devuelve el resultado, 
    la confianza y la información extra.
    """
    # --- 1. PREPARACIÓN DE LA VARIABLE DATA (Lo que faltaba) ---
    # Creamos el array con la forma exacta que espera el modelo
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # --- 2. PROCESAMIENTO DE LA IMAGEN ---
    image = Image.open(ruta_imagen).convert("RGB")
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    # Convertir a array y normalizar
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    
    # Insertamos la imagen en nuestro array 'data'
    data[0] = normalized_image_array

    # --- 3. PREDICCIÓN ---
    prediction = model.predict(data)
    index = np.argmax(prediction)
    
    # Limpiamos el nombre (ej: "0 Winter" -> "winter")
    class_name_raw = class_names[index].strip()
    cleaned_class_name = class_name_raw[2:].strip().lower()
    
    confidence_score = np.round(prediction[0][index] * 100)

    # --- 4. INFORMACIÓN EXTRA ---
    if cleaned_class_name in colorimetry_info:
        info = colorimetry_info[cleaned_class_name]
        famosos = ", ".join(info["celebrities"])
        extra_msg = f"\n\n**Consejos:** {info['advice']}\n\n**Famosos con tu colorimetría:** {famosos}"
    else:
        extra_msg = f"\n\nNo tengo consejos específicos para '{cleaned_class_name}' aún."

    return cleaned_class_name.capitalize(), confidence_score, extra_msg