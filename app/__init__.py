"""
Pacote de módulos para análise de vídeo
"""

from .face_recognition import FaceRecognitionModule
from .emotion_detection import EmotionDetectionModule
from .activity_recognition import ActivityRecognitionModule

__all__ = [
    'FaceRecognitionModule',
    'EmotionDetectionModule',
    'ActivityRecognitionModule'
]
