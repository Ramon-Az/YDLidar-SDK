#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider, Button
import time
import threading
import queue

class RealtimeScanner:
    def __init__(self):
        self.fig, self.axes = plt.subplots(2, 2, figsize=(15, 10))
        self.data_queue = queue.Queue()
        self.scanning = False
        self.point_cloud = []
        self.current_height = 0
        self.height_layers = {}
        
        # Configurar subplots
        self.setup_plots()
        self.setup_controls()
        
    def setup_plots(self):
        """Configurar os 4 painéis de visualização"""
        # Painel 1: Vista em tempo real (polar)
        self.ax_polar = plt.subplot(2, 2, 1, projection='polar')
        self.ax_polar.set_title('Varredura em Tempo Real')
        self.ax_polar.set_ylim(0, 1.0)
        self.scatter_polar = self.ax_polar.scatter([], [], c='red', s=2)
        
        # Painel 2: Vista superior completa
        self.ax_top = self.axes[0, 1]
        self.ax_top.set_title('Vista Superior - Todas as Camadas')
        self.ax_top.set_xlabel('X (m)')
        self.ax_top.set_ylabel('Y (m)')
        self.ax_top.grid(True, alpha=0.3)
        self.ax_top.set_aspect('equal')
        
        # Painel 3: Camada atual
        self.ax_layer = self.axes[1, 0]
        self.ax_layer.set_title('Camada Atual: 0.0cm')
        self.ax_layer.set_xlabel('X (m)')
        self.ax_layer.set_ylabel('Y (m)')
        self.ax_layer.grid(True, alpha=0.3)
        self.ax_layer.set_aspect('equal')
        
        # Painel 4: Perfil vertical
        self.ax_profile = self.axes[1, 1]
        self.ax_profile.set_title('Perfil Vertical')
        self.ax_profile.set_xlabel('Distância (m)')
        self.ax_profile.set_ylabel('Altura (cm)')
        self.ax_profile.grid(True, alpha=0.3)
        
    def setup_controls(self):
        """Configurar controles interativos"""
        plt.subplots_adjust(bottom=0.25)
        
        # Slider para altura
        ax_height = plt.axes([0.2, 0.1, 0.5, 0.03])
        self.height_slider = Slider(ax_height, 'Altura (cm)', 0, 50, valinit=0, valfmt='%.1f')
        self.height_slider.on_changed(self.update_layer)
        
        # Botões
        ax_start = plt.axes([0.1, 0.05, 0.1, 0.04])
        ax_stop = plt.axes([0.25, 0.05, 0.1, 0.04])
        ax_save = plt.axes([0.4, 0.05, 0.1, 0.04])
        
        self.btn_start = Button(ax_start, 'Iniciar')
        self.btn_stop = Button(ax_stop, 'Parar')
        self.btn_save = Button(ax_save, 'Salvar')
        
        self.btn_start.on_clicked(self.start_scan)
        self.btn_stop.on_clicked(self.stop_scan)
        self.btn_save.on_clicked(self.save_data)
        
    def simulate_lidar_data(self):
        """Simular dados do LiDAR em tempo real"""
        while self.scanning:
            # Simular varredura de jarro em diferentes alturas
            angles = np.linspace(0, 2*np.pi, 36)
            height = self.current_height
            
            points = []
            for angle in angles:
                # Simular formato 3D do jarro baseado na altura
                if height < 8:  # Base larga
                    radius = 0.08 + np.random.normal(0, 0.002)
                elif height < 20:  # Corpo afunilando
                    taper = (20 - height) / 12
                    radius = 0.05 + taper * 0.03 + np.random.normal(0, 0.001)
                elif height < 35:  # Pescoço
                    radius = 0.045 + np.random.normal(0, 0.001)
                else:  # Boca alargando
                    flare = (height - 35) / 15
                    radius = 0.045 + flare * 0.025 + np.random.normal(0, 0.002)
                
                distance = 0.5 + radius
                x = distance * np.cos(angle)
                y = distance * np.sin(angle)
                
                z = height / 100.0  # Converter cm para metros
                points.append([x, y, z, distance, angle, height])
            
            self.data_queue.put(points)
            
            # Incrementar altura automaticamente
            self.current_height += 0.5
            if self.current_height > 50:
                self.current_height = 0
                
            time.sleep(0.1)
    
    def update_plots(self, frame):
        """Atualizar plots em tempo real"""
        try:
            while not self.data_queue.empty():
                new_points = self.data_queue.get_nowait()
                self.point_cloud.extend(new_points)
                
                # Organizar por camadas
                for point in new_points:
                    height_key = round(point[5], 1)  # Altura em cm agora é índice 5
                    if height_key not in self.height_layers:
                        self.height_layers[height_key] = []
                    self.height_layers[height_key].append(point)
                
                # Atualizar vista polar (últimos pontos)
                if new_points:
                    angles = [p[4] for p in new_points]  # Ângulo agora é índice 4
                    distances = [p[3] for p in new_points]  # Distância agora é índice 3
                    self.ax_polar.clear()
                    self.ax_polar.scatter(angles, distances, c='red', s=3)
                    self.ax_polar.set_title(f'Tempo Real - Altura: {self.current_height:.1f}cm')
                    self.ax_polar.set_ylim(0.4, 0.6)
                
                # Atualizar vista superior (todas as camadas)
                if self.point_cloud:
                    all_x = [p[0] for p in self.point_cloud]
                    all_y = [p[1] for p in self.point_cloud]
                    heights = [p[5] for p in self.point_cloud]  # Altura em cm agora é índice 5
                    
                    self.ax_top.clear()
                    scatter = self.ax_top.scatter(all_x, all_y, c=heights, cmap='viridis', s=1, alpha=0.7)
                    self.ax_top.set_title(f'Vista Superior - {len(self.point_cloud)} pontos')
                    self.ax_top.set_xlabel('X (m)')
                    self.ax_top.set_ylabel('Y (m)')
                    self.ax_top.grid(True, alpha=0.3)
                    self.ax_top.set_aspect('equal')
                
                # Atualizar perfil vertical
                if len(self.height_layers) > 1:
                    heights = list(self.height_layers.keys())
                    avg_distances = []
                    for h in heights:
                        distances = [p[3] for p in self.height_layers[h]]  # Distância agora é índice 3
                        avg_distances.append(np.mean(distances))
                    
                    self.ax_profile.clear()
                    self.ax_profile.plot(avg_distances, heights, 'b-o', markersize=3)
                    self.ax_profile.set_title('Perfil Vertical do Jarro')
                    self.ax_profile.set_xlabel('Distância Média (m)')
                    self.ax_profile.set_ylabel('Altura (cm)')
                    self.ax_profile.grid(True, alpha=0.3)
        
        except queue.Empty:
            pass
        
        return []
    
    def update_layer(self, val):
        """Atualizar visualização da camada selecionada"""
        selected_height = round(self.height_slider.val, 1)
        
        if selected_height in self.height_layers:
            layer_points = self.height_layers[selected_height]
            x_coords = [p[0] for p in layer_points]
            y_coords = [p[1] for p in layer_points]
            
            self.ax_layer.clear()
            self.ax_layer.scatter(x_coords, y_coords, c='orange', s=5)
            self.ax_layer.set_title(f'Camada: {selected_height}cm - {len(layer_points)} pontos')
            self.ax_layer.set_xlabel('X (m)')
            self.ax_layer.set_ylabel('Y (m)')
            self.ax_layer.grid(True, alpha=0.3)
            self.ax_layer.set_aspect('equal')
        else:
            self.ax_layer.clear()
            self.ax_layer.set_title(f'Camada: {selected_height}cm - Sem dados')
            self.ax_layer.grid(True, alpha=0.3)
        
        plt.draw()
    
    def start_scan(self, event):
        """Iniciar varredura"""
        if not self.scanning:
            self.scanning = True
            self.scan_thread = threading.Thread(target=self.simulate_lidar_data)
            self.scan_thread.daemon = True
            self.scan_thread.start()
            print("Varredura iniciada")
    
    def stop_scan(self, event):
        """Parar varredura"""
        self.scanning = False
        print("Varredura parada")
    
    def save_data(self, event):
        """Salvar nuvem de pontos 3D"""
        if self.point_cloud:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"pointcloud_3d_{timestamp}.csv"
            
            import csv
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['X', 'Y', 'Z', 'Distance', 'Angle', 'Height_cm', 'Layer'])
                
                for point in self.point_cloud:
                    x, y, z, distance, angle, height = point
                    layer = int(height / 0.5)  # Número da camada
                    writer.writerow([x, y, z, distance, angle, height, layer])
            
            print(f"Nuvem de pontos 3D salva: {filename}")
            print(f"Pontos: {len(self.point_cloud)}")
            print(f"Camadas: {len(self.height_layers)}")
            print(f"Altura: {max([p[5] for p in self.point_cloud]):.1f}cm")
    
    def run(self):
        """Executar scanner em tempo real"""
        ani = animation.FuncAnimation(self.fig, self.update_plots, interval=100, blit=False)
        plt.show()

if __name__ == "__main__":
    scanner = RealtimeScanner()
    print("=== SCANNER TEMPO REAL ===")
    print("Controles:")
    print("- Botão 'Iniciar': Começar varredura")
    print("- Botão 'Parar': Pausar varredura")
    print("- Slider: Navegar entre camadas")
    print("- Botão 'Salvar': Exportar dados")
    scanner.run()