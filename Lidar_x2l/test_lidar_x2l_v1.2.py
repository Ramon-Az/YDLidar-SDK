#!/usr/bin/env python3
import ydlidar # type: ignore
import time
import pandas as pd
import numpy as np
from datetime import datetime
import os
import logging
from lidar_config import *

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_lidar_x2l():
    """Teste do LiDAR X2L com tratamento adequado de erros"""
    lidar = None
    
    try:
        # Configurar LiDAR X2L usando lidar_config.py
        lidar = ydlidar.CYdLidar()
        
        # Obter configuração completa do sistema
        config = LidarConfig.get_full_config()
        constants = config["constants"]
        settings = config["settings"]
        
        logger.info(f"Sistema detectado: {LidarConfig.get_system_config()}")
        logger.info(f"Usando porta: {config['port']}")
        
        # Configurações básicas para X2L
        lidar.setlidaropt(constants["prop_serial_port"], config["port"])
        lidar.setlidaropt(constants["prop_baudrate"], config["baudrate"])
        lidar.setlidaropt(constants["prop_lidar_type"], constants["lidar_type"])
        lidar.setlidaropt(constants["prop_device_type"], constants["device_type"])
        lidar.setlidaropt(constants["prop_scan_frequency"], settings["scan_frequency"])
        lidar.setlidaropt(constants["prop_sample_rate"], settings["sample_rate"])
        lidar.setlidaropt(constants["prop_single_channel"], settings["single_channel"])
        
        # Inicializar com tratamento de erro específico
        logger.info("Inicializando LiDAR...")
        ret = lidar.initialize()
        if not ret:
            raise ConnectionError("Falha ao inicializar LiDAR - Verifique conexão e porta")
        
        # Iniciar scan com tratamento de erro específico
        logger.info("Iniciando scan...")
        ret = lidar.turnOn()
        if not ret:
            raise RuntimeError("Falha ao iniciar scan - LiDAR pode estar ocupado")
        
        logger.info(f"LiDAR X2L iniciado em {config['port']} a {settings['scan_frequency']}Hz. Coletando dados...")
        
        # Lista para armazenar todos os pontos
        todos_pontos = []
        scans_validos = 0
        
        try:
            for i in range(10):  # 10 scans de teste
                scan = ydlidar.LaserScan()
                ret = lidar.doProcessSimple(scan)
                
                if ret and scan.points:
                    scans_validos += 1
                    logger.info(f"Scan {i+1}: {len(scan.points)} pontos detectados")
                    logger.info(f"  Primeiro ponto: ângulo={scan.points[0].angle:.2f}°, distância={scan.points[0].range:.2f}m")
                    
                    # Adicionar pontos à lista com validação
                    for point in scan.points:
                        if 0 <= point.range <= 50:  # Validar distância razoável, ajustar para o tamanho do ambiente em metros(no caso aqui vai de 0 a 50m)
                            todos_pontos.append({
                                'angulo': point.angle,
                                'distancia': point.range,
                                'x': point.range * np.cos(np.radians(point.angle)),
                                'y': point.range * np.sin(np.radians(point.angle))
                            })
                else:
                    logger.warning(f"Scan {i+1}: Falha na leitura ou sem pontos")
                
                time.sleep(0.5)  # Pausa entre scans
        
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
        data_dir = 'data/pontos_reais'
        os.makedirs(data_dir, exist_ok=True)
        filepath = os.path.join(data_dir, filename)
        
        # Validar dados antes de salvar
        if len(pontos_data) == 0:
            raise ValueError("Lista de pontos está vazia")
        
        # Criar DataFrame e salvar
        df = pd.DataFrame(pontos_data, columns=['x', 'y', 'angulo', 'distancia'])
        
        # Validar DataFrame
        if df.empty:
            raise ValueError("DataFrame está vazio")
        
        # Salvar arquivo
        df.to_csv(filepath, index=False)
        
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
    logger.info("=== Iniciando teste do LiDAR X2L v1.2 ===")
    sucesso = test_lidar_x2l()
    
    if sucesso:
        logger.info("=== Teste concluído com sucesso ===")
    else:
        logger.error("=== Teste falhou - Verifique logs acima ===")
        exit(1)