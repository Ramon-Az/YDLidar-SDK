#!/usr/bin/env python3
import platform
import glob
import os
try:
    import ydlidar # type: ignore
except ImportError:
    print("Aviso: ydlidar não instalado. Usando valores padrão.")
    ydlidar = None

class LidarConfig:
    """Configuração centralizada para LiDAR X2L"""
    
    # Configurações por sistema operacional
    SYSTEM_CONFIGS = {
        "Windows": {
            "port_patterns": ["COM*"],
            "default_port": "COM3",
            "baudrate": 115200
        },
        "Linux": {
            "port_patterns": ["/dev/ttyUSB*", "/dev/ttyACM*"],
            "default_port": "/dev/ttyUSB0",
            "baudrate": 115200
        },
        "Darwin": {  # macOS
            "port_patterns": ["/dev/tty.usbserial-*", "/dev/cu.usbserial-*"],
            "default_port": "/dev/tty.usbserial-0001",
            "baudrate": 115200
        }
    }
    
    # Configurações específicas do X2L
    X2L_SETTINGS = {
        "scan_frequency": 6.0,  # Hz - otimizado para X2L
        "sample_rate": 3000,    # Hz
        "single_channel": True,
        "auto_reconnect": True,
        "timeout": 5.0  # segundos
    }
    
    @classmethod
    def get_lidar_constants(cls):
        """Retorna constantes do ydlidar ou valores padrão"""
        if ydlidar:
            return {
                "lidar_type": ydlidar.TYPE_TRIANGLE,
                "device_type": ydlidar.YDLIDAR_TYPE_SERIAL,
                "prop_serial_port": ydlidar.LidarPropSerialPort,
                "prop_baudrate": ydlidar.LidarPropSerialBaudrate,
                "prop_lidar_type": ydlidar.LidarPropLidarType,
                "prop_device_type": ydlidar.LidarPropDeviceType,
                "prop_scan_frequency": ydlidar.LidarPropScanFrequency,
                "prop_sample_rate": ydlidar.LidarPropSampleRate,
                "prop_single_channel": ydlidar.LidarPropSingleChannel
            }
        else:
            # Valores padrão quando ydlidar não está disponível
            return {
                "lidar_type": 1,  # TYPE_TRIANGLE
                "device_type": 0,  # YDLIDAR_TYPE_SERIAL
                "prop_serial_port": 0,
                "prop_baudrate": 1,
                "prop_lidar_type": 2,
                "prop_device_type": 3,
                "prop_scan_frequency": 4,
                "prop_sample_rate": 5,
                "prop_single_channel": 6
            }
    
    @classmethod
    def detect_port(cls):
        """Detecta automaticamente a porta do LiDAR"""
        system = platform.system()
        config = cls.SYSTEM_CONFIGS.get(system, cls.SYSTEM_CONFIGS["Linux"])
        
        # Tentar detectar portas disponíveis
        for pattern in config["port_patterns"]:
            ports = glob.glob(pattern)
            for port in ports:
                if os.path.exists(port):
                    print(f"Porta detectada: {port}")
                    return port
        
        # Fallback para porta padrão
        default_port = config["default_port"]
        print(f"Usando porta padrão: {default_port}")
        return default_port
    
    @classmethod
    def get_system_config(cls):
        """Retorna configuração para o sistema atual"""
        system = platform.system()
        return cls.SYSTEM_CONFIGS.get(system, cls.SYSTEM_CONFIGS["Linux"])
    
    @classmethod
    def get_full_config(cls):
        """Retorna configuração completa para o sistema atual"""
        system_config = cls.get_system_config()
        constants = cls.get_lidar_constants()
        
        return {
            "port": cls.detect_port(),
            "baudrate": system_config["baudrate"],
            "constants": constants,
            "settings": cls.X2L_SETTINGS
        }

# Compatibilidade com código antigo
LIDAR_CONFIG = LidarConfig.SYSTEM_CONFIGS
X2L_SETTINGS = LidarConfig.X2L_SETTINGS