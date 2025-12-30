"""
Módulo de Reconhecimento Facial
Face Recognition Module usando MediaPipe
"""

import cv2
import mediapipe as mp
import numpy as np


class FaceRecognitionModule:
    """Módulo para detecção e reconhecimento facial"""
    
    def __init__(self):
        """Inicializa o detector de faces do MediaPipe"""
        self.mp_face_detection = mp.solutions.face_detection
        self.mp_drawing = mp.solutions.drawing_utils
        self.face_detection = self.mp_face_detection.FaceDetection(
            model_selection=1,
            min_detection_confidence=0.5
        )
        
    def process_frame(self, frame):
        """
        Processa um frame para detectar faces
        
        Args:
            frame: Frame de vídeo (numpy array)
            
        Returns:
            Frame processado com anotações
        """
        # Converte BGR para RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Processa o frame
        results = self.face_detection.process(rgb_frame)
        
        # Desenha as detecções
        if results.detections:
            for detection in results.detections:
                # Desenha caixa delimitadora
                self.mp_drawing.draw_detection(frame, detection)
                
                # Extrai confiança da detecção
                confidence = detection.score[0]
                
                # Pega a localização da face
                bbox = detection.location_data.relative_bounding_box
                h, w, _ = frame.shape
                x = int(bbox.xmin * w)
                y = int(bbox.ymin * h)
                
                # Adiciona texto com confiança
                text = f"Face: {confidence:.2f}"
                cv2.putText(frame, text, (x, y - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        return frame
    
    def __del__(self):
        """Limpa recursos"""
        self.face_detection.close()
