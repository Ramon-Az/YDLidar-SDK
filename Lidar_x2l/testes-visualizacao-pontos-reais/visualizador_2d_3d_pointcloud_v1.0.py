#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import os
# from mpl_toolkits.mplot3d import Axes3D


def filter_invalid_points(data):
    """Filtrar pontos inválidos"""
    original_count = len(data)
    
    # Remover pontos com distância zero ou muito pequena
    if 'Distance' in data.columns:
        data = data[data['Distance'] > 0.01]
    
    # Remover pontos com coordenadas NaN ou infinitas
    data = data.dropna(subset=['X', 'Y'])
    data = data[~data['X'].isin([float('inf'), float('-inf')])]
    data = data[~data['Y'].isin([float('inf'), float('-inf')])]
    
    # Remover outliers extremos
    if 'Distance' in data.columns:
        q99 = data['Distance'].quantile(0.99)
        data = data[data['Distance'] <= q99 * 1.5]
    
    filtered_count = original_count - len(data)
    if filtered_count > 0:
        print(f"\n⚠️  Filtrados {filtered_count} pontos inválidos ({filtered_count/original_count*100:.1f}%)")
    
    return data

def detect_point_type(data):
    """Detectar se os dados são 2D ou 3D"""
    has_z = 'Z' in data.columns and data['Z'].notna().any() and data['Z'].std() > 1e-6
    return '3D' if has_z else '2D'

def plot_2d(data):
    """Visualizar nuvem de pontos 2D"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Plot XY com cor por distância
    if 'Distance' in data.columns:
        scatter = ax1.scatter(data['X'], data['Y'], c=data['Distance'], cmap='viridis', s=10, alpha=0.8)
        plt.colorbar(scatter, ax=ax1, label='Distância (m)')
    else:
        ax1.scatter(data['X'], data['Y'], s=10, alpha=0.8)
    
    ax1.set_title('Nuvem de Pontos 2D', fontsize=12, fontweight='bold')
    ax1.set_xlabel('X (m)')
    ax1.set_ylabel('Y (m)')
    ax1.set_aspect('equal')
    ax1.grid(True, alpha=0.3)
    ax1.axhline(0, color='k', linewidth=0.5, alpha=0.3)
    ax1.axvline(0, color='k', linewidth=0.5, alpha=0.3)
    
    # Plot polar se houver ângulo
    if 'Angle' in data.columns and 'Distance' in data.columns:
        ax2 = plt.subplot(122, projection='polar')
        ax2.scatter(data['Angle'], data['Distance'], s=10, alpha=0.8, c=data['Distance'], cmap='viridis')
        ax2.set_title('Vista Polar', fontsize=12, fontweight='bold', pad=20)
        ax2.set_theta_zero_location('E')
        ax2.set_theta_direction(1)
        ax2.grid(True, alpha=0.3)
    else:
        ax2.hist2d(data['X'], data['Y'], bins=50, cmap='hot')
        ax2.set_title('Densidade de Pontos')
        ax2.set_xlabel('X (m)')
        ax2.set_ylabel('Y (m)')
    
    plt.tight_layout()
    plt.show()
    
    print(f"\n=== ESTATÍSTICAS 2D ===")
    print(f"Total de pontos: {len(data)}")
    print(f"X: {data['X'].min():.3f} a {data['X'].max():.3f}m (amplitude: {data['X'].max()-data['X'].min():.3f}m)")
    print(f"Y: {data['Y'].min():.3f} a {data['Y'].max():.3f}m (amplitude: {data['Y'].max()-data['Y'].min():.3f}m)")
    if 'Distance' in data.columns:
        print(f"Distância: {data['Distance'].min():.3f} a {data['Distance'].max():.3f}m (média: {data['Distance'].mean():.3f}m)")
    if 'Angle' in data.columns:
        print(f"Ângulo: {data['Angle'].min():.3f} a {data['Angle'].max():.3f} rad")

def plot_3d(data):
    """Visualizar nuvem de pontos 3D"""
    fig = plt.figure(figsize=(15, 10))
    
    # Plot 3D principal
    ax1 = fig.add_subplot(2, 2, 1, projection='3d')
    scatter = ax1.scatter(data['X'], data['Y'], data['Z'], 
                        c=data['Z'], cmap='viridis', s=1, alpha=0.6)
    ax1.set_title('Nuvem de Pontos 3D')
    ax1.set_xlabel('X (m)')
    ax1.set_ylabel('Y (m)')
    ax1.set_zlabel('Z (m)')
    plt.colorbar(scatter, ax=ax1, shrink=0.5, label='Z (m)')
    
    # Vista superior (XY)
    ax2 = fig.add_subplot(2, 2, 2)
    color_col = 'Z' if 'Height' not in data.columns else 'Height'
    ax2.scatter(data['X'], data['Y'], c=data[color_col], cmap='plasma', s=2, alpha=0.7)
    ax2.set_title('Vista Superior (XY)')
    ax2.set_xlabel('X (m)')
    ax2.set_ylabel('Y (m)')
    ax2.set_aspect('equal')
    ax2.grid(True, alpha=0.3)
    
    # Vista lateral (XZ)
    ax3 = fig.add_subplot(2, 2, 3)
    color_col = 'Distance' if 'Distance' in data.columns else 'Z'
    ax3.scatter(data['X'], data['Z'], c=data[color_col], cmap='coolwarm', s=2, alpha=0.7)
    ax3.set_title('Vista Lateral (XZ)')
    ax3.set_xlabel('X (m)')
    ax3.set_ylabel('Z (m)')
    ax3.grid(True, alpha=0.3)
    
    # Vista frontal (YZ)
    ax4 = fig.add_subplot(2, 2, 4)
    ax4.scatter(data['Y'], data['Z'], c=data[color_col], cmap='coolwarm', s=2, alpha=0.7)
    ax4.set_title('Vista Frontal (YZ)')
    ax4.set_xlabel('Y (m)')
    ax4.set_ylabel('Z (m)')
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    print(f"\n=== ESTATÍSTICAS 3D ===")
    print(f"Total de pontos: {len(data)}")
    print(f"X: {data['X'].min():.3f} a {data['X'].max():.3f}m")
    print(f"Y: {data['Y'].min():.3f} a {data['Y'].max():.3f}m") 
    print(f"Z: {data['Z'].min():.3f} a {data['Z'].max():.3f}m")
    if 'Layer' in data.columns:
        print(f"Camadas: {data['Layer'].nunique()}")

def load_and_view(csv_file):
    """Carregar e visualizar nuvem de pontos (2D ou 3D)"""
    try:
        if not os.path.exists(csv_file):
            print(f"Erro: Arquivo '{csv_file}' não encontrado")
            return
        
        data = pd.read_csv(csv_file)
        print(f"\nCarregados {len(data)} pontos")
        print(f"Colunas encontradas: {list(data.columns)}")
        
        # Mapear colunas automaticamente
        col_map = {}
        for col in data.columns:
            col_lower = col.lower().strip()
            if col_lower in ['x', 'pos_x', 'position_x']:
                col_map[col] = 'X'
            elif col_lower in ['y', 'pos_y', 'position_y']:
                col_map[col] = 'Y'
            elif col_lower in ['z', 'pos_z', 'position_z', 'height', 'altura']:
                col_map[col] = 'Z'
            elif col_lower in ['distance', 'dist', 'distancia', 'range']:
                col_map[col] = 'Distance'
            elif col_lower in ['angle', 'angulo', 'theta']:
                col_map[col] = 'Angle'
        
        # Renomear colunas
        if col_map:
            data = data.rename(columns=col_map)
            print(f"Colunas mapeadas: {col_map}")
        
        # Verificar se tem colunas X e Y
        if 'X' not in data.columns or 'Y' not in data.columns:
            print(f"\nErro: Arquivo deve conter colunas X e Y (ou equivalentes)")
            print(f"Colunas disponíveis: {list(data.columns)}")
            return
        
        # Filtrar pontos inválidos
        data = filter_invalid_points(data)
        
        if len(data) == 0:
            print("\nErro: Nenhum ponto válido após filtragem")
            return
        
        point_type = detect_point_type(data)
        print(f"\nTipo detectado: {point_type}")
        
        if point_type == '3D':
            plot_3d(data)
        else:
            plot_2d(data)
        
    except Exception as e:
        print(f"Erro ao processar arquivo: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("=== VISUALIZADOR DE NUVEM DE PONTOS ===")
    print("Detecta automaticamente pontos 2D ou 3D\n")
    
    filename = input("Nome do arquivo CSV (ou caminho completo): ").strip()
    
    if filename:
        # Se não for caminho completo, buscar em ../data/pontos_Reais/
        if not os.path.exists(filename) and not os.path.isabs(filename):
            data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'pontos_Reais', filename)
            if os.path.exists(data_path):
                filename = data_path
        
        load_and_view(filename)
    else:
        print("Nenhum arquivo especificado.")