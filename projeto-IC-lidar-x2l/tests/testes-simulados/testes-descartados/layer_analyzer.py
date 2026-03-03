#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import pandas as pd

class LayerAnalyzer:
    def __init__(self, csv_file=None):
        self.data = None
        self.layers = {}
        if csv_file:
            self.load_data(csv_file)
    
    def load_data(self, csv_file):
        """Carregar dados de varredura por camadas"""
        try:
            self.data = pd.read_csv(csv_file)
            self.organize_layers()
            print(f"Carregados {len(self.data)} pontos de {len(self.layers)} camadas")
        except Exception as e:
            print(f"Erro ao carregar: {e}")
    
    def organize_layers(self):
        """Organizar dados por camadas de altura"""
        if self.data is None:
            return
        
        # Agrupar por altura (arredondada para 0.5cm)
        self.data['HeightLayer'] = (self.data['Height'] // 0.5) * 0.5
        
        for height in self.data['HeightLayer'].unique():
            layer_data = self.data[self.data['HeightLayer'] == height]
            self.layers[height] = layer_data
    
    def create_interactive_viewer(self):
        """Criar visualizador interativo de camadas"""
        if not self.layers:
            print("Nenhum dado carregado")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        plt.subplots_adjust(bottom=0.15)
        
        # Configurar eixos
        ax_layer = axes[0, 0]
        ax_3d = axes[0, 1]
        ax_profile = axes[1, 0]
        ax_stats = axes[1, 1]
        
        # Slider para seleção de camada
        ax_slider = plt.axes([0.2, 0.05, 0.5, 0.03])
        height_range = [min(self.layers.keys()), max(self.layers.keys())]
        slider = Slider(ax_slider, 'Altura (cm)', height_range[0], height_range[1], 
                       valinit=height_range[0], valfmt='%.1f')
        
        def update_display(height):
            """Atualizar visualização para altura selecionada"""
            height = round(height * 2) / 2  # Arredondar para 0.5
            
            if height not in self.layers:
                return
            
            layer = self.layers[height]
            
            # Limpar eixos
            for ax in [ax_layer, ax_3d, ax_profile, ax_stats]:
                ax.clear()
            
            # 1. Vista da camada atual
            ax_layer.scatter(layer['X'], layer['Y'], c='red', s=10, alpha=0.7)
            ax_layer.set_title(f'Camada {height}cm - {len(layer)} pontos')
            ax_layer.set_xlabel('X (m)')
            ax_layer.set_ylabel('Y (m)')
            ax_layer.grid(True, alpha=0.3)
            ax_layer.set_aspect('equal')
            
            # Calcular e mostrar contorno
            if len(layer) > 3:
                # Ordenar pontos por ângulo para criar contorno
                angles = np.arctan2(layer['Y'], layer['X'])
                sorted_indices = np.argsort(angles)
                x_sorted = layer['X'].iloc[sorted_indices]
                y_sorted = layer['Y'].iloc[sorted_indices]
                
                ax_layer.plot(x_sorted, y_sorted, 'b-', alpha=0.5, linewidth=2)
            
            # 2. Vista 3D (simulada com cores)
            all_heights = []
            all_x = []
            all_y = []
            
            for h in sorted(self.layers.keys()):
                if abs(h - height) <= 5:  # Mostrar camadas próximas
                    layer_data = self.layers[h]
                    all_x.extend(layer_data['X'])
                    all_y.extend(layer_data['Y'])
                    all_heights.extend([h] * len(layer_data))
            
            if all_heights:
                scatter = ax_3d.scatter(all_x, all_y, c=all_heights, cmap='viridis', s=5, alpha=0.7)
                ax_3d.set_title('Vista 3D (±5cm da camada atual)')
                ax_3d.set_xlabel('X (m)')
                ax_3d.set_ylabel('Y (m)')
                ax_3d.set_aspect('equal')
                plt.colorbar(scatter, ax=ax_3d, label='Altura (cm)')
            
            # 3. Perfil radial da camada
            if len(layer) > 0:
                distances = np.sqrt(layer['X']**2 + layer['Y']**2)
                angles_deg = np.degrees(np.arctan2(layer['Y'], layer['X']))
                angles_deg[angles_deg < 0] += 360  # Converter para 0-360
                
                # Ordenar por ângulo
                sorted_idx = np.argsort(angles_deg)
                ax_profile.plot(angles_deg[sorted_idx], distances.iloc[sorted_idx], 'g-o', markersize=3)
                ax_profile.set_title(f'Perfil Radial - Camada {height}cm')
                ax_profile.set_xlabel('Ângulo (graus)')
                ax_profile.set_ylabel('Distância do centro (m)')
                ax_profile.grid(True, alpha=0.3)
                ax_profile.set_xlim(0, 360)
            
            # 4. Estatísticas da camada
            ax_stats.axis('off')
            if len(layer) > 0:
                distances = np.sqrt(layer['X']**2 + layer['Y']**2)
                
                stats_text = f"""
ESTATÍSTICAS - Camada {height}cm

Pontos: {len(layer)}
Distância mín: {distances.min():.3f}m
Distância máx: {distances.max():.3f}m
Distância média: {distances.mean():.3f}m
Desvio padrão: {distances.std():.3f}m

Raio estimado: {distances.mean() - 0.5:.3f}m
Circunferência: {2 * np.pi * (distances.mean() - 0.5):.3f}m

Coordenadas X:
  Min: {layer['X'].min():.3f}m
  Max: {layer['X'].max():.3f}m
  
Coordenadas Y:
  Min: {layer['Y'].min():.3f}m
  Max: {layer['Y'].max():.3f}m
                """
                
                ax_stats.text(0.05, 0.95, stats_text, transform=ax_stats.transAxes,
                            fontsize=10, verticalalignment='top', fontfamily='monospace')
            
            plt.draw()
        
        # Conectar slider
        slider.on_changed(update_display)
        
        # Mostrar primeira camada
        update_display(min(self.layers.keys()))
        
        plt.suptitle('Analisador de Camadas - Varredura 3D', fontsize=14)
        plt.show()

def demo_layer_analysis():
    """Demonstração com dados simulados 3D"""
    # Criar dados simulados de múltiplas camadas
    data = []
    
    for height in np.arange(0, 40, 0.5):  # 0 a 40cm em passos de 0.5cm
        angles = np.linspace(0, 2*np.pi, 72)  # 72 pontos por camada
        
        for angle in angles:
            # Simular formato 3D de jarro variando com altura
            if height < 8:  # Base larga
                radius = 0.08 + np.random.normal(0, 0.002)
            elif height < 20:  # Corpo afunilando
                taper = (20 - height) / 12
                radius = 0.05 + taper * 0.03 + np.random.normal(0, 0.001)
            elif height < 30:  # Pescoço
                radius = 0.045 + np.random.normal(0, 0.001)
            else:  # Boca alargando
                flare = (height - 30) / 10
                radius = 0.045 + flare * 0.02 + np.random.normal(0, 0.002)
            
            distance = 0.5 + radius
            x = distance * np.cos(angle)
            y = distance * np.sin(angle)
            z = height / 100.0  # Converter cm para metros
            layer = int(height / 0.5)  # Número da camada
            
            data.append([x, y, z, distance, angle, height, layer])
    
    # Salvar dados demo 3D
    import pandas as pd
    df = pd.DataFrame(data, columns=['X', 'Y', 'Z', 'Distance', 'Angle', 'Height', 'Layer'])
    df.to_csv('demo_pointcloud_3d.csv', index=False)
    
    print(f"Nuvem de pontos 3D criada: {len(data)} pontos")
    print(f"Camadas: {df['Layer'].nunique()}")
    print(f"Altura total: {df['Height'].max()}cm")
    
    # Analisar
    analyzer = LayerAnalyzer('demo_pointcloud_3d.csv')
    analyzer.create_interactive_viewer()

if __name__ == "__main__":
    print("=== ANALISADOR DE CAMADAS ===")
    print("1. Executando demonstração com dados simulados")
    print("2. Use o slider para navegar entre camadas")
    print("3. Observe as diferentes visualizações e estatísticas")
    
    demo_layer_analysis()