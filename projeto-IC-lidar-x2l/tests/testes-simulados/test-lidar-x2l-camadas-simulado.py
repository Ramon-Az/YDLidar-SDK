#!/usr/bin/env python3
import time
import pandas as pd
import numpy as np
from datetime import datetime
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def simular_scan_circular(altura, num_pontos=360, raio_min=0.5, raio_max=5.0):
    """Simula um scan circular do LiDAR com obstáculos aleatórios"""
    pontos = []
    
    for i in range(num_pontos):
        angulo = i  # 0 a 359 graus
        # Simula distâncias variadas com alguns obstáculos
        distancia = np.random.uniform(raio_min, raio_max)
        
        # Adiciona alguns "obstáculos" em ângulos específicos
        if 45 <= angulo <= 55 or 135 <= angulo <= 145:
            distancia = np.random.uniform(raio_min, raio_min + 1.0)
        elif 225 <= angulo <= 235 or 315 <= angulo <= 325:
            distancia = np.random.uniform(raio_max - 1.0, raio_max)
        
        pontos.append({
            'altura': altura,
            'angulo': angulo,
            'distancia': distancia,
            'x': distancia * np.cos(np.radians(angulo)),
            'y': distancia * np.sin(np.radians(angulo)),
            'z': altura
        })
    
    return pontos

def coletar_camada_simulada(altura, num_scans=5):
    """Simula coleta de dados de uma única camada"""
    pontos_camada = []
    
    logger.info(f"Coletando camada na altura {altura}m...")
    input(f"[SIMULAÇÃO] Posicione o LiDAR na altura {altura}m e pressione ENTER para iniciar a varredura...")
    
    for i in range(num_scans):
        logger.info(f"  Scan {i+1}/{num_scans}...")
        pontos = simular_scan_circular(altura)
        pontos_camada.extend(pontos)
        time.sleep(0.2)
    
    logger.info(f"Camada {altura}m: {num_scans}/{num_scans} scans válidos, {len(pontos_camada)} pontos")
    return pontos_camada

def test_lidar_camadas_simulado():
    """Simula coleta de dados do LiDAR em múltiplas camadas"""
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
        logger.info("[MODO SIMULAÇÃO] - Dados sintéticos serão gerados")
        
        # Simular inicialização
        logger.info("Inicializando LiDAR simulado...")
        time.sleep(0.5)
        logger.info("Iniciando scan simulado...")
        time.sleep(0.5)
        
        # Coletar todas as camadas
        todos_pontos = []
        for altura in alturas:
            pontos = coletar_camada_simulada(altura)
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
    except Exception as e:
        logger.error(f"Erro inesperado: {e}")
        return False
    
    finally:
        logger.info("Desligando LiDAR simulado...")
        time.sleep(0.3)
        logger.info("LiDAR simulado desconectado")

def salvar_pontos_camadas(pontos_data, altura_inicial, altura_final, intervalo):
    """Salva pontos das camadas em arquivo CSV"""
    try:
        if not pontos_data:
            logger.warning("Nenhum ponto para salvar")
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"pontos_camadas_SIM_{timestamp}.csv"
        
        data_dir = 'data/pontos_camadas_simulados'
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
    logger.info("=== LiDAR X2L - Coleta por Camadas [SIMULAÇÃO] ===")
    sucesso = test_lidar_camadas_simulado()
    
    if sucesso:
        logger.info("=== Simulação concluída com sucesso ===")
    else:
        logger.error("=== Simulação falhou ===")
        exit(1)
