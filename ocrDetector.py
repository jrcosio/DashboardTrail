import cv2
import easyocr
import re

class OCRDetector:
    def __init__(self):
        self.lector = easyocr.Reader(['en'])
    
    def suavizar_imagen(self, imagen):
        dorsal_suavizado = cv2.GaussianBlur(imagen, (5, 5), 0)
        dorsal_suavizado = cv2.cvtColor(dorsal_suavizado, cv2.COLOR_BGR2GRAY)
        dorsal_suavizado = cv2.threshold(dorsal_suavizado, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        return dorsal_suavizado
    
    def obtener_numero_dorsal(self, imagen, lector):
        result = lector.readtext(imagen)
        if result:
            return result[0][1]
        return None
    
    def detectar_dorsal(self, bbox_image):
        try:
            # Redimensionar imagen
            dorsal_small = cv2.resize(bbox_image, (0, 0), fx=0.5, fy=0.5)
            
            # Suavizar imagen
            dorsal_preparada = self.suavizar_imagen(dorsal_small)
            
            # Detectar texto
            numero_dorsal = self.obtener_numero_dorsal(dorsal_preparada, self.lector)
            
            if numero_dorsal:
                # Filtrar solo números
                solo_numeros = re.sub(r'[^0-9]', '', numero_dorsal)
                
                if solo_numeros:
                    # Formatear a 3 dígitos con ceros
                    numero_formateado = solo_numeros.zfill(3)
                    return numero_formateado, dorsal_preparada
            
            return None, dorsal_preparada
            
        except Exception as e:
            print(f"Error en detección OCR: {e}")
            return None, None
            
        except Exception as e:
            print(f"Error en detección OCR: {e}")
            return None