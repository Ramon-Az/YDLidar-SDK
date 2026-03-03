#!/usr/bin/env python3
import time
import csv
import math
import random
from datetime import datetime
import os
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Simulação das classes do ydlidar
class MockLaserPoint:
    def __init__(self, angle, range_val):
        self.angle = angle
        self.range = range_val

class MockLaserScan:
    def __init__(self):
        self.points = []

class MockCYdLidar:
    def setlidaropt(self, prop, value):
        pass
    
    def initialize(self):
        return True
    
    def turnOn(self):
        return True
    
    def doProcessSimple(self, scan):
        # Simular pontos do LiDAR com obstáculos
        scan.points = []
        for angle in range(0, 360, 2):
            # Simular distâncias variadas
            if 45 <= angle <= 135:  # Obstáculo próximo
                distance = random.uniform(0.5, 1.5)
            elif 200 <= angle <= 250:  # Outro obstáculo
                distance = random.uniform(1.0, 2.0)
            else:  # Parede distante
                distance = random.uniform(2.5, 3.5)
            
            scan.points.append(MockLaserPoint(angle, distance))
        return True
    
    def turnOff(self):
        pass
    
    def disconnecting(self):
        pass

def test_lidar_x2l_simulacao():
    """Teste simulado do LiDAR X2L com tratamento adequado de erros"""
    lidar = None
    
    try:
        # Configuração simulada
        config = {
            "port": "COM3",
            "baudrate": 230400,
            "settings": {"scan_frequency": 10}
        }
        
        logger.info("Sistema detectado: Windows (SIMULAÇÃO)")
        logger.info(f"Usando porta: {config['port']} (SIMULAÇÃO)")
        
        # Inicializar simulação
        lidar = MockCYdLidar()
        
        logger.info("Inicializando LiDAR...")
        ret = lidar.initialize()
        if not ret:
            raise ConnectionError("Falha ao inicializar LiDAR - Verifique conexão e porta")
        
        logger.info("Iniciando scan...")
        ret = lidar.turnOn()
        if not ret:
            raise RuntimeError("Falha ao iniciar scan - LiDAR pode estar ocupado")
        
        logger.info(f"LiDAR X2L iniciado em {config['port']} a {config['settings']['scan_frequency']}Hz. Coletando dados...")
        
        # Lista para armazenar todos os pontos
        todos_pontos = []
        scans_validos = 0
        
        try:
            for i in range(10):  # 10 scans de teste
                scan = MockLaserScan()
                ret = lidar.doProcessSimple(scan)
                
                if ret and scan.points:
                    scans_validos += 1
                    logger.info(f"Scan {i+1}: {len(scan.points)} pontos detectados")
                    logger.info(f"  Primeiro ponto: ângulo={scan.points[0].angle:.2f}°, distância={scan.points[0].range:.2f}m")
                    
                    # Adicionar pontos à lista com validação
                    for point in scan.points:
                        if 0 <= point.range <= 50:  # Validar distância razoável
                            todos_pontos.append({
                                'angulo': point.angle,
                                'distancia': point.range,
                                'x': point.range * math.cos(math.radians(point.angle)),
                                'y': point.range * math.sin(math.radians(point.angle))
                            })
                else:
                    logger.warning(f"Scan {i+1}: Falha na leitura ou sem pontos")
                
                time.sleep(0.1)  # Pausa menor para simulação
        
        except KeyboardInterrupt:
            logger.info("Interrompido pelo usuário")
        
        logger.info(f"Coleta finalizada: {scans_validos}/10 scans válidos, {len(todos_pontos)} pontos coletados")
        
        # Salvar pontos se coletados
        if todos_pontos:
            arquivo_salvo = salvar_pontos(todos_pontos)
            if arquivo_salvo:
                logger.info(f"Dados salvos com sucesso: {arquivo_salvo}")
            else:
                logger.error("Falha ao salvar dados")
        else:
            logger.warning("Nenhum ponto válido coletado")
        
        return True
        
    except ConnectionError as e:
        logger.error(f"Erro de conexão: {e}")
        return False
    except RuntimeError as e:
        logger.error(f"Erro de execução: {e}")
        return False
    except Exception as e:
        logger.error(f"Erro inesperado: {e}")
        return False
    
    finally:
        # Desconexão segura com tratamento específico de erros
        if lidar:
            try:
                logger.info("Desligando LiDAR...")
                lidar.turnOff()
            except Exception as e:
                logger.error(f"Erro ao desligar LiDAR: {e}")
            
            try:
                logger.info("Desconectando LiDAR...")
                lidar.disconnecting()
                logger.info("LiDAR desconectado com sucesso")
            except Exception as e:
                logger.error(f"Erro ao desconectar LiDAR: {e}")

def salvar_pontos(pontos_data):
    """Salvar pontos do LiDAR em arquivo CSV com timestamp e validação"""
    try:
        if not pontos_data:
            logger.warning("Nenhum ponto para salvar")
            return None
        
        # Criar nome do arquivo com timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"pontos_{timestamp}.csv"
        
        # Criar diretório se não existir
        data_dir = 'data/pontos_simulados'
        os.makedirs(data_dir, exist_ok=True)
        filepath = os.path.join(data_dir, filename)
        
        # Validar dados antes de salvar
        if len(pontos_data) == 0:
            raise ValueError("Lista de pontos está vazia")
        
        # Salvar usando csv nativo
        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['x', 'y', 'angulo', 'distancia'])  # Cabeçalho
            for ponto in pontos_data:
                writer.writerow([ponto['x'], ponto['y'], ponto['angulo'], ponto['distancia']])
        
        # Verificar se arquivo foi criado
        if not os.path.exists(filepath):
            raise IOError(f"Arquivo não foi criado: {filepath}")
        
        # Verificar tamanho do arquivo
        file_size = os.path.getsize(filepath)
        if file_size == 0:
            raise IOError("Arquivo criado está vazio")
        
        logger.info(f"Pontos salvos: {filepath} ({len(pontos_data)} pontos, {file_size} bytes)")
        return filepath
        
    except ValueError as e:
        logger.error(f"Erro de validação de dados: {e}")
        return None
    except IOError as e:
        logger.error(f"Erro de E/S ao salvar arquivo: {e}")
        return None
    except Exception as e:
        logger.error(f"Erro inesperado ao salvar pontos: {e}")
        return None

if __name__ == "__main__":
    logger.info("=== Iniciando teste SIMULADO do LiDAR X2L v1.2 ===")
    sucesso = test_lidar_x2l_simulacao()
    
    if sucesso:
        logger.info("=== Teste simulado concluído com sucesso ===")
    else:
        logger.error("=== Teste simulado falhou - Verifique logs acima ===")
        exit(1)