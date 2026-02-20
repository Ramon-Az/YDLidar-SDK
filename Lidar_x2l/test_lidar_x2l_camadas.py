#!/usr/bin/env python3
import ydlidar
import time
import pandas as pd
import numpy as np
from datetime import datetime
import os
import logging
from lidar_config import *

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def coletar_camada(lidar, altura, num_scans=5):
    """Coleta dados de uma única camada"""
    pontos_camada = []
    scans_validos = 0
    
    logger.info(f"Coletando camada na altura {altura}m...")
    input(f"Posicione o LiDAR na altura {altura}m e pressione ENTER para iniciar a varredura...")
    
    for i in range(num_scans):
        scan = ydlidar.LaserScan()
        ret = lidar.doProcessSimple(scan)
        
        if ret and scan.points:
            scans_validos += 1
            for point in scan.points:
                if 0 <= point.range <= 50:
                    pontos_camada.append({
                        'altura': altura,
                        'angulo': point.angle,
                        'distancia': point.range,
                        'x': point.range * np.cos(np.radians(point.angle)),
                        'y': point.range * np.sin(np.radians(point.angle)),
                        'z': altura
                    })
        
        time.sleep(0.2)
    
    logger.info(f"Camada {altura}m: {scans_validos}/{num_scans} scans válidos, {len(pontos_camada)} pontos")
    return pontos_camada

def test_lidar_camadas():
    """Coleta dados do LiDAR em múltiplas camadas"""
    lidar = None
    
    try:
        # Solicitar parâmetros ao usuário
        altura_inicial = float(input("Altura inicial (m): "))
        altura_final = float(input("Altura final (m): "))
        intervalo = float(input("Intervalo entre camadas (m): "))
        
        if intervalo <= 0:
            raise ValueError("Intervalo deve ser maior que zero")
        if altura_final <= altura_inicial:
            raise ValueError("Altura final deve ser maior que inicial")
        
        # Calcular camadas
        num_camadas = int((altura_final - altura_inicial) / intervalo) + 1
        alturas = [altura_inicial + i * intervalo for i in range(num_camadas)]
        
        logger.info(f"Serão coletadas {num_camadas} camadas: {alturas}")
        
        # Configurar LiDAR
        lidar = ydlidar.CYdLidar()
        config = LidarConfig.get_full_config()
        constants = config["constants"]
        settings = config["settings"]
        
        lidar.setlidaropt(constants["prop_serial_port"], config["port"])
        lidar.setlidaropt(constants["prop_baudrate"], config["baudrate"])
        lidar.setlidaropt(constants["prop_lidar_type"], constants["lidar_type"])
        lidar.setlidaropt(constants["prop_device_type"], constants["device_type"])
        lidar.setlidaropt(constants["prop_scan_frequency"], settings["scan_frequency"])
        lidar.setlidaropt(constants["prop_sample_rate"], settings["sample_rate"])
        lidar.setlidaropt(constants["prop_single_channel"], settings["single_channel"])
        
        logger.info("Inicializando LiDAR...")
        if not lidar.initialize():
            raise ConnectionError("Falha ao inicializar LiDAR")
        
        logger.info("Iniciando scan...")
        if not lidar.turnOn():
            raise RuntimeError("Falha ao iniciar scan")
        
        # Coletar todas as camadas
        todos_pontos = []
        for altura in alturas:
            pontos = coletar_camada(lidar, altura)
            todos_pontos.extend(pontos)
        
        logger.info(f"Coleta finalizada: {len(todos_pontos)} pontos totais")
        
        # Salvar dados
        if todos_pontos:
            arquivo = salvar_pontos_camadas(todos_pontos, altura_inicial, altura_final, intervalo)
            if arquivo:
                logger.info(f"Dados salvos: {arquivo}")
            else:
                logger.error("Falha ao salvar dados")
        else:
            logger.warning("Nenhum ponto coletado")
        
        return True
        
    except ValueError as e:
        logger.error(f"Erro nos parâmetros: {e}")
        return False
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
        if lidar:
            try:
                logger.info("Desligando LiDAR...")
                lidar.turnOff()
                lidar.disconnecting()
                logger.info("LiDAR desconectado")
            except Exception as e:
                logger.error(f"Erro ao desconectar: {e}")

def salvar_pontos_camadas(pontos_data, altura_inicial, altura_final, intervalo):
    """Salva pontos das camadas em arquivo CSV"""
    try:
        if not pontos_data:
            logger.warning("Nenhum ponto para salvar")
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"pontos_camadas_{altura_inicial}m_a_{altura_final}m_intervalo_{intervalo}m_{timestamp}.csv"
        
        data_dir = 'data/pontos_camadas'
        os.makedirs(data_dir, exist_ok=True)
        filepath = os.path.join(data_dir, filename)
        
        df = pd.DataFrame(pontos_data, columns=['altura', 'angulo', 'distancia', 'x', 'y', 'z'])
        df.to_csv(filepath, index=False)
        
        if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
            raise IOError("Erro ao criar arquivo")
        
        logger.info(f"Arquivo salvo: {len(pontos_data)} pontos, {os.path.getsize(filepath)} bytes")
        return filepath
        
    except Exception as e:
        logger.error(f"Erro ao salvar: {e}")
        return None

if __name__ == "__main__":
    logger.info("=== LiDAR X2L - Coleta por Camadas ===")
    sucesso = test_lidar_camadas()
    
    if sucesso:
        logger.info("=== Coleta concluída com sucesso ===")
    else:
        logger.error("=== Coleta falhou ===")
        exit(1)
