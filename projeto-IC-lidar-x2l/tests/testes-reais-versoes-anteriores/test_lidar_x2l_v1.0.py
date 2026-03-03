#!/usr/bin/env python3
import ydlidar # type: ignore
import time
from lidar_config import *

def test_lidar_x2l():
    # Configurar LiDAR X2L usando lidar_config.py
    lidar = ydlidar.CYdLidar()
    
    # Obter configuração completa do sistema
    config = LidarConfig.get_full_config()
    constants = config["constants"]
    settings = config["settings"]
    
    print(f"Sistema detectado: {LidarConfig.get_system_config()}")
    print(f"Usando porta: {config['port']}")
    
    # Configurações básicas para X2L usando constantes do lidar_config
    lidar.setlidaropt(constants["prop_serial_port"], config["port"])
    lidar.setlidaropt(constants["prop_baudrate"], config["baudrate"])
    lidar.setlidaropt(constants["prop_lidar_type"], constants["lidar_type"])
    lidar.setlidaropt(constants["prop_device_type"], constants["device_type"])
    lidar.setlidaropt(constants["prop_scan_frequency"], settings["scan_frequency"])
    lidar.setlidaropt(constants["prop_sample_rate"], settings["sample_rate"])
    lidar.setlidaropt(constants["prop_single_channel"], settings["single_channel"])
    
    # Inicializar
    ret = lidar.initialize()
    if not ret:
        print("Erro: Falha ao inicializar LiDAR")
        try:
            lidar.disconnecting()
        except:
            pass
        return False
    
    # Iniciar scan
    ret = lidar.turnOn()
    if not ret:
        print("Erro: Falha ao iniciar scan")
        try:
            lidar.disconnecting()
        except:
            pass
        return False
    
    print(f"LiDAR X2L iniciado em {config['port']} a {settings['scan_frequency']}Hz. Coletando dados...")
    
    try:
        for i in range(10):  # 10 scans de teste
            scan = ydlidar.LaserScan()
            ret = lidar.doProcessSimple(scan)
            
            if ret:
                print(f"Scan {i+1}: {len(scan.points)} pontos detectados")
                if scan.points:
                    print(f"  Primeiro ponto: ângulo={scan.points[0].angle:.2f}°, distância={scan.points[0].range:.2f}m")
            else:
                print(f"Scan {i+1}: Falha na leitura")
            
            time.sleep(0.5)  # Pausa entre scans
    
    except KeyboardInterrupt:
        print("\nInterrompido pelo usuário")
    
    finally:
        try:
            lidar.turnOff()
        except Exception as e:
            print(f"Erro ao desligar LiDAR: {e}")
        try:
            lidar.disconnecting()
        except Exception as e:
            print(f"Erro ao desconectar LiDAR: {e}")
        print("LiDAR desconectado")
    
    return True

if __name__ == "__main__":
    test_lidar_x2l()