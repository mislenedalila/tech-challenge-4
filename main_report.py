"""
Video Analysis Application - Com Geração de Relatório
Aplicação de análise de vídeo com reconhecimento facial, detecção de emoções
e reconhecimento de atividades humanas.
"""

import cv2
import sys
import os
from pathlib import Path
from datetime import datetime
from collections import Counter
import json

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


class VideoAnalysisReport:
    """Classe para gerar relatórios de análise"""
    
    def __init__(self, video_path):
        self.video_path = video_path
        self.total_frames = 0
        self.frames_com_faces = 0
        self.emocoes_detectadas = []
        self.atividades_detectadas = []
        self.anomalias = []
        self.inicio_analise = datetime.now()
        self.fim_analise = None
        
    def registrar_frame(self, tem_face, emocao, atividade):
        """Registra informações de um frame"""
        self.total_frames += 1
        
        if tem_face:
            self.frames_com_faces += 1
            
        if emocao:
            self.emocoes_detectadas.append(emocao)
            
        if atividade:
            self.atividades_detectadas.append(atividade)
    
    def registrar_anomalia(self, tipo, descricao, frame_numero):
        """Registra uma anomalia detectada"""
        self.anomalias.append({
            'tipo': tipo,
            'descricao': descricao,
            'frame': frame_numero,
            'timestamp': datetime.now().strftime('%H:%M:%S')
        })
    
    def finalizar(self):
        """Finaliza a análise"""
        self.fim_analise = datetime.now()
    
    def gerar_relatorio_texto(self):
        """Gera relatório em formato texto"""
        duracao = (self.fim_analise - self.inicio_analise).total_seconds()
        
        # Contadores
        emocoes_counter = Counter(self.emocoes_detectadas)
        atividades_counter = Counter(self.atividades_detectadas)
        
        relatorio = []
        relatorio.append("=" * 80)
        relatorio.append("RELATÓRIO DE ANÁLISE DE VÍDEO")
        relatorio.append("=" * 80)
        relatorio.append("")
        
        # Informações Gerais
        relatorio.append("📋 INFORMAÇÕES GERAIS")
        relatorio.append("-" * 80)
        relatorio.append(f"Vídeo Analisado:     {os.path.basename(self.video_path)}")
        relatorio.append(f"Data/Hora Análise:   {self.inicio_analise.strftime('%d/%m/%Y %H:%M:%S')}")
        relatorio.append(f"Duração da Análise:  {duracao:.2f} segundos")
        relatorio.append("")
        
        # Estatísticas de Frames
        relatorio.append("🎬 ESTATÍSTICAS DE FRAMES")
        relatorio.append("-" * 80)
        relatorio.append(f"Total de Frames Analisados:     {self.total_frames}")
        relatorio.append(f"Frames com Faces Detectadas:   {self.frames_com_faces}")
        percentual_faces = (self.frames_com_faces / self.total_frames * 100) if self.total_frames > 0 else 0
        relatorio.append(f"Percentual de Detecção:         {percentual_faces:.2f}%")
        relatorio.append("")
        
        # Emoções Detectadas
        relatorio.append("😊 EMOÇÕES DETECTADAS")
        relatorio.append("-" * 80)
        if emocoes_counter:
            relatorio.append(f"Total de Registros:   {len(self.emocoes_detectadas)}")
            relatorio.append("")
            relatorio.append("Distribuição das Emoções:")
            for emocao, count in emocoes_counter.most_common():
                percentual = (count / len(self.emocoes_detectadas) * 100)
                barra = "█" * int(percentual / 2)
                relatorio.append(f"  {emocao:15s}: {count:5d} ({percentual:5.1f}%) {barra}")
            
            relatorio.append("")
            relatorio.append(f"Emoção Predominante:  {emocoes_counter.most_common(1)[0][0]}")
        else:
            relatorio.append("Nenhuma emoção detectada")
        relatorio.append("")
        
        # Atividades Detectadas
        relatorio.append("🏃 ATIVIDADES DETECTADAS")
        relatorio.append("-" * 80)
        if atividades_counter:
            relatorio.append(f"Total de Registros:   {len(self.atividades_detectadas)}")
            relatorio.append("")
            relatorio.append("Distribuição das Atividades:")
            for atividade, count in atividades_counter.most_common():
                percentual = (count / len(self.atividades_detectadas) * 100)
                barra = "█" * int(percentual / 2)
                relatorio.append(f"  {atividade:15s}: {count:5d} ({percentual:5.1f}%) {barra}")
            
            relatorio.append("")
            relatorio.append(f"Atividade Predominante:  {atividades_counter.most_common(1)[0][0]}")
        else:
            relatorio.append("Nenhuma atividade detectada")
        relatorio.append("")
        
        # Anomalias Detectadas
        relatorio.append("⚠️  ANOMALIAS DETECTADAS")
        relatorio.append("-" * 80)
        relatorio.append(f"Número de Anomalias:  {len(self.anomalias)}")
        
        if self.anomalias:
            relatorio.append("")
            relatorio.append("Detalhamento das Anomalias:")
            for i, anomalia in enumerate(self.anomalias, 1):
                relatorio.append(f"  {i}. [{anomalia['timestamp']}] Frame {anomalia['frame']}")
                relatorio.append(f"     Tipo: {anomalia['tipo']}")
                relatorio.append(f"     Descrição: {anomalia['descricao']}")
                relatorio.append("")
        else:
            relatorio.append("Nenhuma anomalia detectada no vídeo")
        
        relatorio.append("")
        relatorio.append("=" * 80)
        relatorio.append("FIM DO RELATÓRIO")
        relatorio.append("=" * 80)
        
        return "\n".join(relatorio)
    
    def gerar_relatorio_json(self):
        """Gera relatório em formato JSON"""
        duracao = (self.fim_analise - self.inicio_analise).total_seconds()
        
        # Contadores
        emocoes_counter = Counter(self.emocoes_detectadas)
        atividades_counter = Counter(self.atividades_detectadas)
        
        relatorio = {
            "informacoes_gerais": {
                "video": os.path.basename(self.video_path),
                "data_analise": self.inicio_analise.strftime('%d/%m/%Y %H:%M:%S'),
                "duracao_analise_segundos": round(duracao, 2)
            },
            "estatisticas_frames": {
                "total_frames_analisados": self.total_frames,
                "frames_com_faces": self.frames_com_faces,
                "percentual_deteccao": round((self.frames_com_faces / self.total_frames * 100) if self.total_frames > 0 else 0, 2)
            },
            "emocoes": {
                "total_registros": len(self.emocoes_detectadas),
                "distribuicao": dict(emocoes_counter),
                "emocao_predominante": emocoes_counter.most_common(1)[0][0] if emocoes_counter else None
            },
            "atividades": {
                "total_registros": len(self.atividades_detectadas),
                "distribuicao": dict(atividades_counter),
                "atividade_predominante": atividades_counter.most_common(1)[0][0] if atividades_counter else None
            },
            "anomalias": {
                "numero_anomalias": len(self.anomalias),
                "detalhes": self.anomalias
            }
        }
        
        return json.dumps(relatorio, indent=2, ensure_ascii=False)
    
    def salvar_relatorio(self, formato='txt', output_dir='data/output'):
        """Salva o relatório em arquivo"""
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if formato == 'txt':
            filename = f"relatorio_analise_{timestamp}.txt"
            filepath = os.path.join(output_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(self.gerar_relatorio_texto())
        elif formato == 'json':
            filename = f"relatorio_analise_{timestamp}.json"
            filepath = os.path.join(output_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(self.gerar_relatorio_json())
        
        return filepath


class VideoAnalyzer:
    """Classe principal para análise de vídeo"""
    
    def __init__(self):
        """Inicializa os módulos de análise"""
        print("Inicializando módulos de análise...")
        self.face_recognition = FaceRecognitionModule()
        self.emotion_detection = EmotionDetectionModule()
        self.activity_recognition = ActivityRecognitionModule()
        print("Módulos inicializados com sucesso!")
    
    def detectar_anomalias(self, frame_info, frame_numero):
        """Detecta anomalias baseado nas informações do frame"""
        anomalias = []
        
        # Exemplo de detecção de anomalias
        # Você pode personalizar estas regras
        
        # Anomalia: Múltiplas faces na mesma cena (mais de 3)
        if frame_info.get('num_faces', 0) > 3:
            anomalias.append({
                'tipo': 'Múltiplas Faces',
                'descricao': f'{frame_info["num_faces"]} faces detectadas simultaneamente',
                'frame': frame_numero
            })
        
        # Anomalia: Emoção negativa persistente
        if frame_info.get('emocao') in ['Triste', 'Raiva']:
            anomalias.append({
                'tipo': 'Emoção Negativa',
                'descricao': f'Emoção {frame_info["emocao"]} detectada',
                'frame': frame_numero
            })
        
        # Anomalia: Atividade suspeita
        if frame_info.get('atividade') in ['unknown', 'Desconhecido']:
            if frame_numero % 100 == 0:  # Registra a cada 100 frames para não poluir
                anomalias.append({
                    'tipo': 'Atividade Não Identificada',
                    'descricao': 'Não foi possível identificar a atividade',
                    'frame': frame_numero
                })
        
        return anomalias
    
    def process_video(self, video_source=0, gerar_relatorio=True):
        """
        Processa vídeo em tempo real ou de arquivo
        
        Args:
            video_source: 0 para webcam ou caminho para arquivo de vídeo
            gerar_relatorio: Se True, gera relatório ao final
        """
        cap = cv2.VideoCapture(video_source)
        
        if not cap.isOpened():
            print(f"Erro ao abrir vídeo: {video_source}")
            return
        
        # Inicializa relatório
        report = VideoAnalysisReport(str(video_source)) if gerar_relatorio else None
        
        print(f"Processando vídeo de: {video_source}")
        print("Pressione 'q' para sair")
        
        frame_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Fim do vídeo ou erro na captura")
                break
            
            frame_count += 1
            
            # Informações do frame atual
            frame_info = {
                'num_faces': 0,
                'emocao': None,
                'atividade': None
            }
            
            # Processa o frame com cada módulo
            frame = self.face_recognition.process_frame(frame)
            frame = self.emotion_detection.process_frame(frame)
            frame = self.activity_recognition.process_frame(frame)
            
            # Aqui você precisaria extrair as informações dos módulos
            # Por simplicidade, vamos simular
            # TODO: Modificar os módulos para retornar informações
            
            # Adiciona contador de frames
            cv2.putText(frame, f"Frame: {frame_count}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Registra no relatório
            if report:
                # Simular detecção (você deve pegar valores reais dos módulos)
                tem_face = frame_count % 2 == 0  # Exemplo
                emocao = "Neutro"  # Deve vir do módulo
                atividade = "standing"  # Deve vir do módulo
                
                report.registrar_frame(tem_face, emocao, atividade)
                
                # Detectar anomalias
                frame_info.update({'num_faces': 1 if tem_face else 0, 'emocao': emocao, 'atividade': atividade})
                anomalias = self.detectar_anomalias(frame_info, frame_count)
                for anomalia in anomalias:
                    report.registrar_anomalia(anomalia['tipo'], anomalia['descricao'], anomalia['frame'])
            
            # Exibe o frame processado
            cv2.imshow('Video Analysis', frame)
            
            # Verifica se o usuário pressionou 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Encerrando...")
                break
        
        cap.release()
        cv2.destroyAllWindows()
        
        # Gera relatório
        if report:
            report.finalizar()
            
            print(f"\nTotal de frames processados: {frame_count}")
            print("\n" + "="*80)
            print("GERANDO RELATÓRIO...")
            print("="*80)
            
            # Exibe relatório no terminal
            print("\n" + report.gerar_relatorio_texto())
            
            # Salva relatórios
            txt_path = report.salvar_relatorio('txt')
            json_path = report.salvar_relatorio('json')
            
            print(f"\n✓ Relatório em texto salvo em: {txt_path}")
            print(f"✓ Relatório em JSON salvo em: {json_path}")
        else:
            print(f"Total de frames processados: {frame_count}")


def print_usage():
    """Imprime instruções de uso"""
    print("\n" + "="*60)
    print("VIDEO ANALYSIS APPLICATION - COM RELATÓRIO")
    print("="*60)
    print("\nModos de uso:")
    print("\n1. Análise em tempo real (webcam):")
    print("   python main_com_relatorio.py")
    print("   python main_com_relatorio.py --webcam")
    print("\n2. Análise de arquivo de vídeo:")
    print("   python main_com_relatorio.py --video caminho/para/video.mp4")
    print("\n3. Sem gerar relatório:")
    print("   python main_com_relatorio.py --video video.mp4 --no-report")
    print("\nOpções:")
    print("  --help, -h       Mostra esta mensagem")
    print("  --webcam         Usa webcam (padrão)")
    print("  --video PATH     Processa arquivo de vídeo")
    print("  --camera ID      ID da câmera (padrão: 0)")
    print("  --no-report      Não gera relatório")
    print("\nPressione 'q' durante a execução para sair")
    print("="*60 + "\n")


def main():
    """Função principal"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Aplicação de análise de vídeo com IA e Relatório',
        add_help=False
    )
    parser.add_argument('--help', '-h', action='store_true',
                       help='Mostra ajuda')
    parser.add_argument('--webcam', action='store_true',
                       help='Usa webcam')
    parser.add_argument('--video', type=str,
                       help='Caminho para arquivo de vídeo')
    parser.add_argument('--camera', type=int, default=0,
                       help='ID da câmera (padrão: 0)')
    parser.add_argument('--no-report', action='store_true',
                       help='Não gera relatório')
    
    args = parser.parse_args()
    
    # Mostra ajuda se solicitado
    if args.help:
        print_usage()
        return
    
    try:
        # Inicializa o analisador
        analyzer = VideoAnalyzer()
        
        # Determina se vai gerar relatório
        gerar_relatorio = not args.no_report
        
        # Determina o modo de operação
        if args.video:
            analyzer.process_video(args.video, gerar_relatorio)
        else:
            # Modo padrão: webcam
            camera_id = args.camera
            analyzer.process_video(camera_id, gerar_relatorio)
    
    except KeyboardInterrupt:
        print("\n\nInterrompido pelo usuário")
    except Exception as e:
        print(f"\n\nErro durante execução: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
