"""
Módulo de Reconhecimento de Atividades
Activity Recognition Module usando MediaPipe Pose
"""

import cv2
import mediapipe as mp
import numpy as np


class ActivityRecognitionModule:
    """Módulo para reconhecimento de atividades humanas através de pose"""
    
    def __init__(self):
        """Inicializa o detector de pose do MediaPipe"""
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Atividades possíveis
        self.activities = {
            'standing': 'Em pé',
            'sitting': 'Sentado',
            'waving': 'Acenando',
            'raising_hand': 'Levantando a mão',
            'unknown': 'Desconhecido'
        }
        
    def analyze_activity(self, landmarks, image_shape):
        """
        Analisa a atividade baseado nos landmarks de pose
        
        Args:
            landmarks: Pontos de pose detectados
            image_shape: Dimensões da imagem
            
        Returns:
            String com a atividade detectada
        """
        # Pontos de referência importantes
        # 0 = nariz
        # 11, 12 = ombros
        # 13, 14 = cotovelos
        # 15, 16 = pulsos
        # 23, 24 = quadris
        # 25, 26 = joelhos
        # 27, 28 = tornozelos
        
        h, w = image_shape[:2]
        
        # Extrai pontos específicos
        nose = landmarks.landmark[self.mp_pose.PoseLandmark.NOSE]
        left_shoulder = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_SHOULDER]
        left_hip = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_HIP]
        right_hip = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_HIP]
        left_wrist = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_WRIST]
        right_wrist = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_WRIST]
        
        # Calcula alturas relativas
        shoulder_y = (left_shoulder.y + right_shoulder.y) / 2
        hip_y = (left_hip.y + right_hip.y) / 2
        
        # Verifica se a mão está levantada
        if left_wrist.y < shoulder_y - 0.1 or right_wrist.y < shoulder_y - 0.1:
            # Verifica se está acenando (mão acima da cabeça)
            if left_wrist.y < nose.y or right_wrist.y < nose.y:
                return 'waving'
            else:
                return 'raising_hand'
        
        # Verifica se está sentado ou em pé baseado na distância ombro-quadril
        torso_length = abs(shoulder_y - hip_y)
        
        if torso_length < 0.2:  # Valor arbitrário
            return 'sitting'
        elif torso_length > 0.25:
            return 'standing'
        
        return 'unknown'
    
    def process_frame(self, frame):
        """
        Processa um frame para detectar atividades
        
        Args:
            frame: Frame de vídeo (numpy array)
            
        Returns:
            Frame processado com anotações
        """
        # Converte BGR para RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Processa o frame
        results = self.pose.process(rgb_frame)
        
        # Desenha as detecções
        if results.pose_landmarks:
            # Desenha os landmarks de pose
            self.mp_drawing.draw_landmarks(
                frame,
                results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style()
            )
            
            # Analisa atividade
            activity_key = self.analyze_activity(results.pose_landmarks, frame.shape)
            activity = self.activities.get(activity_key, 'Desconhecido')
            
            # Adiciona texto com atividade
            h, w, _ = frame.shape
            text = f"Atividade: {activity}"
            cv2.putText(frame, text, (10, h - 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        
        return frame
    
    def __del__(self):
        """Limpa recursos"""
        self.pose.close()
