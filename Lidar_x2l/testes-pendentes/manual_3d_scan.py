#!/usr/bin/env python3
import ydlidar # type: ignore
import numpy as np
import time
import csv

class Manual3DScanner:
    def __init__(self):
        self.lidar = ydlidar.CYdLidar()
        self.point_cloud_3d = []
        
    def setup_lidar(self):
        """Configurar LiDAR X2L"""
        self.lidar.setlidaropt(ydlidar.LidarPropSerialPort, "COM3")
        self.lidar.setlidaropt(ydlidar.LidarPropSerialBaudrate, 115200)
        self.lidar.setlidaropt(ydlidar.LidarPropLidarType, ydlidar.TYPE_TRIANGLE)
        self.lidar.setlidaropt(ydlidar.LidarPropDeviceType, ydlidar.YDLIDAR_TYPE_SERIAL)
        self.lidar.setlidaropt(ydlidar.LidarPropScanFrequency, 8.0)
        return self.lidar.initialize()
    
    def scan_layer_manual(self, height_cm):
        """Escanear uma camada em altura específica"""
        print(f"\n=== CAMADA {height_cm}cm ===")
        print("1. Posicione o objeto na altura correta")
        print("2. Pressione Enter para escanear esta camada")
        input("Pressione Enter quando pronto...")
        
        if not self.lidar.turnOn():
            return False
        
        layer_points = []
        scans_collected = 0
        
        print("Coletando dados... (5 segundos)")
        start_time = time.time()
        
        while time.time() - start_time < 5:  # 5 segundos por camada
            scan = ydlidar.LaserScan()
            if self.lidar.doProcessSimple(scan):
                scans_collected += 1
                
                for point in scan.points:
                    if 0.1 < point.range < 2.0:  # Filtrar distâncias válidas
                        x = point.range * np.cos(point.angle)
                        y = point.range * np.sin(point.angle)
                        z = height_cm / 100.0  # Converter para metros
                        
                        layer_points.append([x, y, z, point.range, point.angle, height_cm])
            
            time.sleep(0.1)
        
        self.lidar.turnOff()
        self.point_cloud_3d.extend(layer_points)
        
        print(f"Camada {height_cm}cm: {len(layer_points)} pontos coletados")
        return True
    
    def scan_object_3d(self, height_start=0, height_end=20, step=2):
        """Escanear objeto em múltiplas alturas manualmente"""
        print("=== VARREDURA 3D MANUAL ===")
        print(f"Alturas: {height_start}cm a {height_end}cm (passo {step}cm)")
        print("\nINSTRUÇÕES:")
        print("- Use suporte ajustável para elevar o objeto")
        print("- Ou eleve o LiDAR com suporte mecânico")
        print("- Mantenha posição horizontal constante")
        
        heights = range(height_start, height_end + 1, step)
        
        for height in heights:
            success = self.scan_layer_manual(height)
            if not success:
                print(f"Erro na camada {height}cm")
                break
        
        print(f"\nVarredura 3D concluída!")
        print(f"Total de pontos: {len(self.point_cloud_3d)}")
        print(f"Camadas escaneadas: {len(heights)}")
    
    def save_3d_data(self):
        """Salvar nuvem de pontos 3D"""
        if not self.point_cloud_3d:
            print("Nenhum dado para salvar")
            return
        
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"manual_3d_scan_{timestamp}.csv"
        
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['X', 'Y', 'Z', 'Distance', 'Angle', 'Height_cm'])
            writer.writerows(self.point_cloud_3d)
        
        print(f"Dados 3D salvos: {filename}")
        return filename

def main():
    scanner = Manual3DScanner()
    
    if not scanner.setup_lidar():
        print("Erro ao configurar LiDAR")
        return
    
    # Configurar varredura
    print("Configuração da varredura:")
    start_height = int(input("Altura inicial (cm): ") or "0")
    end_height = int(input("Altura final (cm): ") or "20")
    step = int(input("Passo entre camadas (cm): ") or "2")
    
    # Executar varredura 3D manual
    scanner.scan_object_3d(start_height, end_height, step)
    
    # Salvar dados
    scanner.save_3d_data()

if __name__ == "__main__":
    main()