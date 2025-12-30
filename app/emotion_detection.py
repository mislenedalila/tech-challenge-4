"""
Módulo de Detecção de Emoções
Emotion Detection Module usando MediaPipe e análise facial
"""

import cv2
import mediapipe as mp
import numpy as np


class EmotionDetectionModule:
    """Módulo para detecção de emoções através de expressões faciais"""
    
    def __init__(self):
        """Inicializa o detector de malha facial do MediaPipe"""
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Mapeamento simples de emoções baseado em landmarks
        self.emotions = ['Neutro', 'Feliz', 'Triste', 'Surpreso']
        
    def analyze_emotion(self, landmarks, image_shape):
        """
        Analisa emoção baseado nos landmarks faciais
        
        Args:
            landmarks: Pontos faciais detectados
            image_shape: Dimensões da imagem
            
        Returns:
            String com a emoção detectada
        """
        # Algoritmo simplificado de análise de emoção
        # Em produção, use um modelo treinado (CNN, etc.)
        
        # Pontos de referência para análise
        # 61, 291 = cantos da boca
        # 13 = ponta do nariz
        # 33, 263 = olhos
        
        h, w = image_shape[:2]
        
        # Extrai pontos específicos
        mouth_left = landmarks.landmark[61]
        mouth_right = landmarks.landmark[291]
        nose_tip = landmarks.landmark[13]
        
        # Análise simples: altura da boca vs nariz
        mouth_y = (mouth_left.y + mouth_right.y) / 2
        mouth_height = abs(mouth_y - nose_tip.y)
        
        # Classificação básica
        if mouth_height < 0.02:
            return 'Neutro'
        elif mouth_height < 0.04:
            return 'Feliz'
        elif mouth_height < 0.06:
            return 'Surpreso'
        else:
            return 'Triste'
    
    def process_frame(self, frame):
        """
        Processa um frame para detectar emoções
        
        Args:
            frame: Frame de vídeo (numpy array)
            
        Returns:
            Frame processado com anotações
        """
        # Converte BGR para RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Processa o frame
        results = self.face_mesh.process(rgb_frame)
        
        # Desenha as detecções
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Desenha a malha facial (opcional, pode deixar comentado para performance)
                # self.mp_drawing.draw_landmarks(
                #     image=frame,
                #     landmark_list=face_landmarks,
                #     connections=self.mp_face_mesh.FACEMESH_TESSELATION,
                #     landmark_drawing_spec=None,
                #     connection_drawing_spec=self.mp_drawing_styles
                #     .get_default_face_mesh_tesselation_style()
                # )
                
                # Analisa emoção
                emotion = self.analyze_emotion(face_landmarks, frame.shape)
                
                # Adiciona texto com emoção
                h, w, _ = frame.shape
                text = f"Emocao: {emotion}"
                cv2.putText(frame, text, (10, h - 50),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 2)
        
        return frame
    
    def __del__(self):
        """Limpa recursos"""
        self.face_mesh.close()
