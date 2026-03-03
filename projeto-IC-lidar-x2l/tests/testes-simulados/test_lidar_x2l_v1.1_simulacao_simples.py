#!/usr/bin/env python3
import time
import csv
import math
from datetime import datetime
import os

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
        # Simular pontos do LiDAR (360 graus com alguns obstáculos)
        scan.points = []
        import random
        for angle in range(0, 360, 2):  # A cada 2 graus
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
    print("SIMULAÇÃO - LiDAR X2L iniciado em COM3 a 10Hz")
    
    # Usar mock do LiDAR
    lidar = MockCYdLidar()
    lidar.initialize()
    lidar.turnOn()
    
    print("Coletando dados simulados...")
    
    # Lista para armazenar todos os pontos
    todos_pontos = []
    
    try:
        for i in range(10):  # 10 scans de teste
            scan = MockLaserScan()
            ret = lidar.doProcessSimple(scan)
            
            if ret:
                print(f"Scan {i+1}: {len(scan.points)} pontos detectados")
                if scan.points:
                    print(f"  Primeiro ponto: ângulo={scan.points[0].angle:.2f}°, distância={scan.points[0].range:.2f}m")
                    # Adicionar pontos à lista
                    for point in scan.points:
                        todos_pontos.append({
                            'angulo': point.angle,
                            'distancia': point.range,
                            'x': point.range * math.cos(math.radians(point.angle)),
                            'y': point.range * math.sin(math.radians(point.angle))
                        })
            else:
                print(f"Scan {i+1}: Falha na leitura")
            
            time.sleep(0.1)  # Pausa menor para simulação
    
    except KeyboardInterrupt:
        print("\nInterrompido pelo usuário")
    
    finally:
        lidar.turnOff()
        lidar.disconnecting()
        print("LiDAR desconectado")
        
        # Salvar pontos se coletados
        if todos_pontos:
            salvar_pontos(todos_pontos)
    
    return True

def salvar_pontos(pontos_data):
    """Salvar pontos do LiDAR em arquivo CSV com timestamp"""
    if not pontos_data:
        print("Nenhum ponto para salvar")
        return None
    
    # Criar nome do arquivo com timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"pontos_{timestamp}.csv"
    
    # Criar diretório se não existir
    os.makedirs('./data/pontos_simulados', exist_ok=True)
    filepath = os.path.join('./data/pontos_simulados', filename)
    
    # Salvar usando csv nativo
    with open(filepath, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['x', 'y', 'angulo', 'distancia'])  # Cabeçalho
        for ponto in pontos_data:
            writer.writerow([ponto['x'], ponto['y'], ponto['angulo'], ponto['distancia']])
    
    print(f"Pontos salvos: {filepath} ({len(pontos_data)} pontos)")
    return filepath

if __name__ == "__main__":
    test_lidar_x2l_simulacao()