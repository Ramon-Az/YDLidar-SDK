#!/usr/bin/env python3
import ydlidar # type: ignore
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import time
import csv
import os
import glob
from lidar_config import *

class ObjectScanner:
    # Constantes para melhor legibilidade
    MIN_DISTANCE = 0.1
    MAX_DISTANCE = 2.0
    PROGRESS_INTERVAL = 10
    SCAN_SLEEP = 0.1
    
    def __init__(self, object_name="object"):
        self.lidar = ydlidar.CYdLidar()
        self.point_cloud = []
        self.object_name = object_name
        self.is_initialized = False
'''    
    def find_lidar_port(self):
        """Detecta automaticamente a porta do LiDAR no Linux"""
        possible_ports = glob.glob('/dev/ttyUSB*') + glob.glob('/dev/ttyACM*')
        for port in possible_ports:
            if os.path.exists(port):
                print(f"Porta detectada: {port}")
                return port
        print("Aviso: Nenhuma porta detectada, usando /dev/ttyUSB0")
        return "/dev/ttyUSB0"
    
    def setup_lidar(self):
        """Configurar LiDAR X2L com tratamento de erros robusto"""
        try:
            # Detectar porta automaticamente
            port = self.find_lidar_port()
            
            # Configurar LiDAR X2L
            self.lidar.setlidaropt(ydlidar.LidarPropSerialPort, port)
            self.lidar.setlidaropt(ydlidar.LidarPropSerialBaudrate, 115200)
            self.lidar.setlidaropt(ydlidar.LidarPropLidarType, ydlidar.TYPE_TRIANGLE)
            self.lidar.setlidaropt(ydlidar.LidarPropDeviceType, ydlidar.YDLIDAR_TYPE_SERIAL)
            self.lidar.setlidaropt(ydlidar.LidarPropScanFrequency, 8.0)
            self.lidar.setlidaropt(ydlidar.LidarPropSampleRate, 3000)
            self.lidar.setlidaropt(ydlidar.LidarPropSingleChannel, False)
            
            # Inicializar
            if self.lidar.initialize():
                self.is_initialized = True
                return True
            else:
                print("Erro: Falha ao inicializar LiDAR")
                self._cleanup()
                return False
                
        except Exception as e:
            print(f"Erro na configuração do LiDAR: {e}")
            self._cleanup()
            return False
'''
    def _cleanup(self):
        """Limpeza segura de recursos"""
        try:
            if hasattr(self, 'lidar'):
                self.lidar.turnOff()
        except Exception as e:
            print(f"Erro ao desligar LiDAR: {e}")
        try:
            if hasattr(self, 'lidar'):
                self.lidar.disconnecting()
        except Exception as e:
            print(f"Erro ao desconectar LiDAR: {e}")
    
    def scan_object(self, duration=30):
        """Escanear objeto por X segundos com tratamento robusto de erros"""
        if not self.is_initialized:
            print("Erro: LiDAR não foi inicializado")
            return False
            
        try:
            if not self.lidar.turnOn():
                print("Erro ao iniciar LiDAR")
                return False
            
            print(f"Iniciando varredura por {duration} segundos...")
            print("Posicione o objeto no centro e pressione Enter para começar")
            input()
            
            start_time = time.time()
            scan_count = 0
            
            while time.time() - start_time < duration:
                try:
                    scan = ydlidar.LaserScan()
                    if self.lidar.doProcessSimple(scan):
                        scan_count += 1
                        
                        # Converter pontos polares para cartesianos
                        for point in scan.points:
                            if self.MIN_DISTANCE < point.range < self.MAX_DISTANCE:
                                x = point.range * np.cos(point.angle)
                                y = point.range * np.sin(point.angle)
                                self.point_cloud.append([x, y, point.range, point.angle])
                        
                        if scan_count % self.PROGRESS_INTERVAL == 0:
                            print(f"Scans: {scan_count}, Pontos coletados: {len(self.point_cloud)}")
                    
                    time.sleep(self.SCAN_SLEEP)
                    
                except Exception as e:
                    print(f"Erro durante scan: {e}")
                    continue
            
        except KeyboardInterrupt:
            print("\nVarredura interrompida pelo usuário")
        except Exception as e:
            print(f"Erro durante varredura: {e}")
            return False
        finally:
            self._cleanup()
        
        print(f"Varredura concluída: {len(self.point_cloud)} pontos coletados")
        return len(self.point_cloud) > 0
    
    def save_point_cloud(self, filename=None):
        """Salvar nuvem de pontos em CSV com validação e tratamento de erros"""
        if not self.point_cloud:
            print("Aviso: Nenhum ponto para salvar")
            return None
            
        try:
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                # Sanitizar nome do arquivo
                safe_name = "".join(c for c in self.object_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
                filename = f"{safe_name}_scan_{timestamp}.csv"
            
            # Validar caminho do arquivo
            if os.path.dirname(filename) and not os.path.exists(os.path.dirname(filename)):
                os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['X', 'Y', 'Distance', 'Angle'])
                writer.writerows(self.point_cloud)
            
            print(f"Nuvem de pontos salva em: {filename}")
            return filename
            
        except (IOError, PermissionError, OSError) as e:
            print(f"Erro ao salvar arquivo: {e}")
            return None
    
    def visualize_2d(self):
        """Visualizar nuvem de pontos em 2D"""
        if not self.point_cloud:
            print("Nenhum ponto para visualizar")
            return
        
        points = np.array(self.point_cloud)
        x, y = points[:, 0], points[:, 1]
        
        plt.figure(figsize=(10, 8))
        plt.scatter(x, y, c='red', s=1, alpha=0.6)
        plt.title(f'Varredura do {self.object_name.title()} - Vista Superior')
        plt.xlabel('X (metros)')
        plt.ylabel('Y (metros)')
        plt.grid(True, alpha=0.3)
        plt.axis('equal')
        plt.show()
    
    def visualize_polar(self):
        """Visualizar em coordenadas polares"""
        if not self.point_cloud:
            print("Nenhum ponto para visualizar")
            return
        
        points = np.array(self.point_cloud)
        angles, distances = points[:, 3], points[:, 2]
        
        plt.figure(figsize=(10, 8))
        plt.subplot(projection='polar')
        plt.scatter(angles, distances, c='blue', s=1, alpha=0.6)
        plt.title(f'Varredura do {self.object_name.title()} - Vista Polar')
        plt.show()

def main():
    scanner = ObjectScanner(object_name="jarro")
    
    if not scanner.setup_lidar():
        print("Erro ao configurar LiDAR")
        return
    
    # Escanear objeto
    if scanner.scan_object(duration=20):  # 20 segundos de varredura
        # Salvar dados
        filename = scanner.save_point_cloud()
        
        if filename:
            # Visualizar apenas se salvou com sucesso
            scanner.visualize_2d()
            #scanner.visualize_polar()
    else:
        print("Falha na varredura - não há dados para salvar ou visualizar")

if __name__ == "__main__":
    main()