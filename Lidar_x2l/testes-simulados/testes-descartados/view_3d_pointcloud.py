#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def load_and_view_3d(csv_file):
    """Carregar e visualizar nuvem de pontos"""
    try:
        # Carregar dados
        data = pd.read_csv(csv_file)
        print(f"Carregados {len(data)} pontos 3D")
        
        # Criar visualização 3D
        fig = plt.figure(figsize=(15, 10))
        
        # Plot principal
        ax1 = fig.add_subplot(2, 2, 1, projection='3d')
        scatter = ax1.scatter(data['X'], data['Y'], data['Z'], 
                            c=data['Z'], cmap='viridis', s=1, alpha=0.6)
        ax1.set_title('Nuvem de Pontos 3D - Jarro Completo')
        ax1.set_xlabel('X (m)')
        ax1.set_ylabel('Y (m)')
        ax1.set_zlabel('Z (m)')
        plt.colorbar(scatter, ax=ax1, shrink=0.5, label='Altura (m)')
        
        # Vista superior (XY)
        ax2 = fig.add_subplot(2, 2, 2)
        ax2.scatter(data['X'], data['Y'], c=data['Height'], cmap='plasma', s=2, alpha=0.7)
        ax2.set_title('Vista Superior (XY)')
        ax2.set_xlabel('X (m)')
        ax2.set_ylabel('Y (m)')
        ax2.set_aspect('equal')
        ax2.grid(True, alpha=0.3)
        
        # Vista lateral (XZ)
        ax3 = fig.add_subplot(2, 2, 3)
        ax3.scatter(data['X'], data['Z'], c=data['Distance'], cmap='coolwarm', s=2, alpha=0.7)
        ax3.set_title('Vista Lateral (XZ)')
        ax3.set_xlabel('X (m)')
        ax3.set_ylabel('Z (m)')
        ax3.grid(True, alpha=0.3)
        
        # Perfil por camadas
        ax4 = fig.add_subplot(2, 2, 4)
        layers = data.groupby('Layer')
        layer_heights = []
        avg_radius = []
        
        for layer_num, layer_data in layers:
            height = layer_data['Height'].mean()
            radius = (layer_data['Distance'] - 0.5).mean()  # Subtrair distância base
            layer_heights.append(height)
            avg_radius.append(radius)
        
        ax4.plot(avg_radius, layer_heights, 'ro-', markersize=4)
        ax4.set_title('Perfil do Jarro (Raio vs Altura)')
        ax4.set_xlabel('Raio médio (m)')
        ax4.set_ylabel('Altura (cm)')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
        
        # Estatísticas 3D
        print(f"\n=== ESTATÍSTICAS 3D ===")
        print(f"Dimensões:")
        print(f"  X: {data['X'].min():.3f} a {data['X'].max():.3f}m")
        print(f"  Y: {data['Y'].min():.3f} a {data['Y'].max():.3f}m") 
        print(f"  Z: {data['Z'].min():.3f} a {data['Z'].max():.3f}m")
        print(f"Altura total: {data['Height'].max():.1f}cm")
        print(f"Camadas: {data['Layer'].nunique()}")
        print(f"Pontos por camada: {len(data) // data['Layer'].nunique():.0f}")
        
    except Exception as e:
        print(f"Erro: {e}")

def create_sample_3d():
    """Criar amostra de nuvem de pontos 3D para teste"""
    data = []
    
    for height in np.arange(0, 30, 1):  # 30cm de altura
        angles = np.linspace(0, 2*np.pi, 36)
        
        for angle in angles:
            # Formato de jarro
            if height < 5:
                radius = 0.08
            elif height < 20:
                radius = 0.05 + (20-height) * 0.0015
            else:
                radius = 0.05 + (height-20) * 0.002
            
            distance = 0.5 + radius
            x = distance * np.cos(angle)
            y = distance * np.sin(angle)
            z = height / 100.0
            layer = int(height)
            
            data.append([x, y, z, distance, angle, height, layer])
    
    df = pd.DataFrame(data, columns=['X', 'Y', 'Z', 'Distance', 'Angle', 'Height', 'Layer'])
    print("Amostra 3D criada: sample_3d.csv")
    return './data/nuvem_de_pontos_simulada/sample_3d.csv'

if __name__ == "__main__":
    print("=== VISUALIZADOR 3D ===")
    
    # Criar amostra se não existir arquivo
    filename = input("Nome do arquivo CSV (Enter para criar amostra): ").strip()
    
    if not filename:
        filename = create_sample_3d()
    
    load_and_view_3d(filename)