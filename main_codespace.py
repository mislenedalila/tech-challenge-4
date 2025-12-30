"""
Video Analysis Application - Versão para Codespace
Salva o vídeo processado ao invés de mostrar em janela
"""

import cv2
import sys
import os
from pathlib import Path

sys.path.append(str(Path(__file__).parent / 'app'))

try:
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
        print("✓ Módulos inicializados com sucesso!")
    
    def process_video_codespace(self, video_source, output_path="output_video.mp4"):
        """
        Processa vídeo e salva o resultado (para Codespace - sem GUI)
        
        Args:
            video_source: Caminho para arquivo de vídeo
            output_path: Caminho para salvar o vídeo processado
        """
        cap = cv2.VideoCapture(video_source)
        
        if not cap.isOpened():
            print(f"❌ Erro ao abrir vídeo: {video_source}")
            print("\nVerifique:")
            print(f"  1. O arquivo existe: {os.path.exists(video_source)}")
            print(f"  2. O caminho está correto")
            print(f"  3. O formato é suportado (MP4, AVI, MOV, etc.)")
            return
        
        # Pega informações do vídeo
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duracao = total_frames / fps if fps > 0 else 0
        
        print("\n" + "="*60)
        print("PROCESSANDO VÍDEO")
        print("="*60)
        print(f"📹 Entrada:     {video_source}")
        print(f"💾 Saída:       {output_path}")
        print(f"📐 Resolução:   {width}x{height}")
        print(f"🎞️  FPS:         {fps}")
        print(f"🎬 Frames:      {total_frames}")
        print(f"⏱️  Duração:     {int(duracao//60)}m {int(duracao%60)}s")
        print("="*60)
        
        # Configura o writer para salvar o vídeo
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        if not out.isOpened():
            print("❌ Erro ao criar arquivo de saída!")
            cap.release()
            return
        
        frame_count = 0
        print("\n🔄 Processando frames...")
        print("-" * 60)
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame_count += 1
                
                # Processa o frame com cada módulo
                frame = self.face_recognition.process_frame(frame)
                frame = self.emotion_detection.process_frame(frame)
                frame = self.activity_recognition.process_frame(frame)
                
                # Adiciona informações ao frame
                info_text = f"Frame: {frame_count}/{total_frames}"
                cv2.putText(frame, info_text, (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                # Adiciona barra de progresso visual
                progress_width = int((frame_count / total_frames) * (width - 20))
                cv2.rectangle(frame, (10, height - 20), (10 + progress_width, height - 10), 
                             (0, 255, 0), -1)
                
                # Salva o frame processado
                out.write(frame)
                
                # Mostra progresso no terminal
                if frame_count % 30 == 0 or frame_count == total_frames:
                    progresso = (frame_count / total_frames) * 100
                    tempo_decorrido = frame_count / fps
                    tempo_restante = (total_frames - frame_count) / fps
                    
                    print(f"[{progresso:5.1f}%] Frame {frame_count:4d}/{total_frames:4d} | "
                          f"Tempo: {int(tempo_decorrido)}s | "
                          f"Restante: ~{int(tempo_restante)}s", end='\r')
        
        except KeyboardInterrupt:
            print("\n\n⚠️  Processamento interrompido pelo usuário")
        except Exception as e:
            print(f"\n\n❌ Erro durante processamento: {e}")
            import traceback
            traceback.print_exc()
        finally:
            cap.release()
            out.release()
        
        print("\n" + "-" * 60)
        print("\n" + "="*60)
        print("✅ PROCESSAMENTO CONCLUÍDO!")
        print("="*60)
        print(f"✓ Frames processados: {frame_count}/{total_frames}")
        print(f"✓ Vídeo salvo em:     {output_path}")
        print(f"✓ Tamanho do arquivo: {os.path.getsize(output_path) / (1024*1024):.2f} MB")
        print("="*60)
        print("\n📥 Para baixar o vídeo processado:")
        print(f"  1. No Explorer, navegue até: {output_path}")
        print(f"  2. Clique com botão direito no arquivo")
        print(f"  3. Selecione 'Download'")
        print("\n🎬 Ou visualize o vídeo no Codespace usando:")
        print(f"  Clique no arquivo para abrir preview")
        print()


def main():
    """Função principal"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Video Analysis - Versão Codespace (salva vídeo processado)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python main_codespace.py --video data/input/video/teste.mp4
  python main_codespace.py --video input.mp4 --output resultado.mp4
        """
    )
    parser.add_argument('--video', type=str, required=True,
                       help='Caminho para arquivo de vídeo de entrada')
    parser.add_argument('--output', type=str, default='data/output/processed_video.mp4',
                       help='Caminho para salvar vídeo processado (padrão: data/output/processed_video.mp4)')
    
    args = parser.parse_args()
    
    # Verifica se o vídeo de entrada existe
    if not os.path.exists(args.video):
        print(f"❌ Erro: Vídeo não encontrado: {args.video}")
        print("\nVerifique:")
        print("  1. O caminho está correto")
        print("  2. O arquivo foi carregado no Codespace")
        print("  3. Use: ls -la para listar arquivos")
        sys.exit(1)
    
    # Cria pasta de output se não existir
    output_dir = os.path.dirname(args.output)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        print(f"✓ Pasta de output criada/verificada: {output_dir}")
    
    try:
        # Inicializa o analisador
        analyzer = VideoAnalyzer()
        
        # Processa o vídeo
        analyzer.process_video_codespace(args.video, args.output)
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrompido pelo usuário")
    except Exception as e:
        print(f"\n\n❌ Erro durante execução: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()