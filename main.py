"""
Video Analysis Application
Aplicação de análise de vídeo com reconhecimento facial, detecção de emoções
e reconhecimento de atividades humanas.
"""

import cv2
import sys
import os
from pathlib import Path

# Adiciona o diretório app ao path para imports
sys.path.append(str(Path(__file__).parent / 'app'))

try:
    # Importa os módulos da aplicação
    from app.face_recognition import FaceRecognitionModule
    from app.emotion_detection import EmotionDetectionModule
    from app.activity_recognition import ActivityRecognitionModule
except ImportError as e:
    print(f"Erro ao importar módulos: {e}")
    print("\nCertifique-se de que a estrutura do projeto está correta:")
    print("  app/")
    print("    face_recognition.py")
    print("    emotion_detection.py")
    print("    activity_recognition.py")
    sys.exit(1)


class VideoAnalyzer:
    """Classe principal para análise de vídeo"""
    
    def __init__(self):
        """Inicializa os módulos de análise"""
        print("Inicializando módulos de análise...")
        self.face_recognition = FaceRecognitionModule()
        self.emotion_detection = EmotionDetectionModule()
        self.activity_recognition = ActivityRecognitionModule()
        print("Módulos inicializados com sucesso!")
    
    def process_video(self, video_source=0):
        """
        Processa vídeo em tempo real ou de arquivo
        
        Args:
            video_source: 0 para webcam ou caminho para arquivo de vídeo
        """
        cap = cv2.VideoCapture(video_source)
        
        if not cap.isOpened():
            print(f"Erro ao abrir vídeo: {video_source}")
            return
        
        print(f"Processando vídeo de: {video_source}")
        print("Pressione 'q' para sair")
        
        frame_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Fim do vídeo ou erro na captura")
                break
            
            frame_count += 1
            
            # Processa o frame com cada módulo
            frame = self.face_recognition.process_frame(frame)
            frame = self.emotion_detection.process_frame(frame)
            frame = self.activity_recognition.process_frame(frame)
            
            # Adiciona contador de frames
            cv2.putText(frame, f"Frame: {frame_count}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Exibe o frame processado
            cv2.imshow('Video Analysis', frame)
            
            # Verifica se o usuário pressionou 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Encerrando...")
                break
        
        cap.release()
        cv2.destroyAllWindows()
        print(f"Total de frames processados: {frame_count}")
    
    def process_image(self, image_path):
        """
        Processa uma imagem única
        
        Args:
            image_path: Caminho para a imagem
        """
        if not os.path.exists(image_path):
            print(f"Imagem não encontrada: {image_path}")
            return
        
        image = cv2.imread(image_path)
        if image is None:
            print(f"Erro ao carregar imagem: {image_path}")
            return
        
        print(f"Processando imagem: {image_path}")
        
        # Processa a imagem com cada módulo
        image = self.face_recognition.process_frame(image)
        image = self.emotion_detection.process_frame(image)
        image = self.activity_recognition.process_frame(image)
        
        # Exibe o resultado
        cv2.imshow('Image Analysis', image)
        print("Pressione qualquer tecla para fechar")
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def print_usage():
    """Imprime instruções de uso"""
    print("\n" + "="*60)
    print("VIDEO ANALYSIS APPLICATION")
    print("="*60)
    print("\nModos de uso:")
    print("\n1. Análise em tempo real (webcam):")
    print("   python main.py")
    print("   python main.py --webcam")
    print("\n2. Análise de arquivo de vídeo:")
    print("   python main.py --video caminho/para/video.mp4")
    print("\n3. Análise de imagem:")
    print("   python main.py --image caminho/para/imagem.jpg")
    print("\n4. Especificar câmera:")
    print("   python main.py --camera 1")
    print("\nOpções:")
    print("  --help, -h       Mostra esta mensagem")
    print("  --webcam         Usa webcam (padrão)")
    print("  --video PATH     Processa arquivo de vídeo")
    print("  --image PATH     Processa imagem")
    print("  --camera ID      ID da câmera (padrão: 0)")
    print("\nPressione 'q' durante a execução para sair")
    print("="*60 + "\n")


def main():
    """Função principal"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Aplicação de análise de vídeo com IA',
        add_help=False
    )
    parser.add_argument('--help', '-h', action='store_true',
                       help='Mostra ajuda')
    parser.add_argument('--webcam', action='store_true',
                       help='Usa webcam')
    parser.add_argument('--video', type=str,
                       help='Caminho para arquivo de vídeo')
    parser.add_argument('--image', type=str,
                       help='Caminho para imagem')
    parser.add_argument('--camera', type=int, default=0,
                       help='ID da câmera (padrão: 0)')
    
    args = parser.parse_args()
    
    # Mostra ajuda se solicitado
    if args.help:
        print_usage()
        return
    
    try:
        # Inicializa o analisador
        analyzer = VideoAnalyzer()
        
        # Determina o modo de operação
        if args.image:
            analyzer.process_image(args.image)
        elif args.video:
            analyzer.process_video(args.video)
        else:
            # Modo padrão: webcam
            camera_id = args.camera
            analyzer.process_video(camera_id)
    
    except KeyboardInterrupt:
        print("\n\nInterrompido pelo usuário")
    except Exception as e:
        print(f"\n\nErro durante execução: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()