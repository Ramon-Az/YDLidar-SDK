#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import os

VERSION = "1.2"

def filter_invalid_points(data):
    """Filtrar pontos inválidos"""
    original_count = len(data)
    
    if 'Distance' in data.columns:
        data = data[data['Distance'] > 0.01]
    
    data = data.dropna(subset=['X', 'Y'])
    data = data[~data['X'].isin([float('inf'), float('-inf')])]
    data = data[~data['Y'].isin([float('inf'), float('-inf')])]
    
    if 'Distance' in data.columns:
        q99 = data['Distance'].quantile(0.99)
        data = data[data['Distance'] <= q99 * 1.5]
    
    filtered_count = original_count - len(data)
    if filtered_count > 0:
        print(f"⚠️  Filtrados {filtered_count} pontos inválidos ({filtered_count/original_count*100:.1f}%)")
    
    return data

def downsample_data(data, max_points=50000):
    """Reduzir pontos para melhorar performance"""
    if len(data) > max_points:
        sample_ratio = max_points / len(data)
        data = data.sample(frac=sample_ratio, random_state=42)
        print(f"📉 Downsampling: {len(data)} pontos (ratio: {sample_ratio:.2%})")
    return data

def detect_point_type(data):
    """Detectar se os dados são 2D ou 3D"""
    if 'Z' not in data.columns:
        return '2D'
    
    has_valid_z = data['Z'].notna().any()
    if not has_valid_z:
        return '2D'
    
    z_std = data['Z'].std()
    has_variation = z_std > 1e-6
    
    return '3D' if has_variation else '2D'

def plot_2d(data):
    """Visualizar nuvem de pontos 2D"""
    data = downsample_data(data, max_points=10000)
    
    fig = plt.figure(figsize=(14, 6))
    
    # Plot XY
    ax1 = plt.subplot(121)
    if 'Distance' in data.columns:
        scatter = ax1.scatter(data['X'], data['Y'], c=data['Distance'], 
                            cmap='viridis', s=8, alpha=0.7, edgecolors='none')
        plt.colorbar(scatter, ax=ax1, label='Distância (m)')
    else:
        ax1.scatter(data['X'], data['Y'], s=8, alpha=0.7, edgecolors='none')
    
    ax1.set_title('Nuvem de Pontos 2D', fontsize=12, fontweight='bold')
    ax1.set_xlabel('X (m)')
    ax1.set_ylabel('Y (m)')
    ax1.set_aspect('equal')
    ax1.grid(True, alpha=0.3, linewidth=0.5)
    ax1.axhline(0, color='k', linewidth=0.5, alpha=0.3)
    ax1.axvline(0, color='k', linewidth=0.5, alpha=0.3)
    
    # Plot polar ou densidade
    if 'Angle' in data.columns and 'Distance' in data.columns:
        ax2 = plt.subplot(122, projection='polar')
        scatter = ax2.scatter(data['Angle'], data['Distance'], 
                            c=data['Distance'], cmap='viridis', 
                            s=8, alpha=0.7, edgecolors='none')
        ax2.set_title('Vista Polar', fontsize=12, fontweight='bold', pad=20)
        ax2.set_theta_zero_location('E')
        ax2.set_theta_direction(1)
        ax2.grid(True, alpha=0.3, linewidth=0.5)
    else:
        ax2 = plt.subplot(122)
        h = ax2.hist2d(data['X'], data['Y'], bins=50, cmap='hot')
        plt.colorbar(h[3], ax=ax2, label='Densidade')
        ax2.set_title('Densidade de Pontos')
        ax2.set_xlabel('X (m)')
        ax2.set_ylabel('Y (m)')
    
    plt.tight_layout()
    plt.show()
    
    print(f"\n=== ESTATÍSTICAS 2D ===")
    print(f"Pontos válidos: {len(data)}")
    print(f"X: {data['X'].min():.3f} a {data['X'].max():.3f}m (Δ={data['X'].max()-data['X'].min():.3f}m)")
    print(f"Y: {data['Y'].min():.3f} a {data['Y'].max():.3f}m (Δ={data['Y'].max()-data['Y'].min():.3f}m)")
    if 'Distance' in data.columns:
        print(f"Distância: {data['Distance'].min():.3f} a {data['Distance'].max():.3f}m (μ={data['Distance'].mean():.3f}m)")
    if 'Angle' in data.columns:
        print(f"Ângulo: {data['Angle'].min():.3f} a {data['Angle'].max():.3f} rad")

def plot_3d(data):
    """Visualizar nuvem de pontos 3D"""
    data = downsample_data(data, max_points=20000)
    
    fig = plt.figure(figsize=(15, 10))
    
    # Plot 3D principal
    ax1 = fig.add_subplot(2, 2, 1, projection='3d')
    scatter = ax1.scatter(data['X'], data['Y'], data['Z'], 
                        c=data['Z'], cmap='viridis', s=1, alpha=0.5, edgecolors='none')
    ax1.set_title('Nuvem de Pontos 3D', fontweight='bold')
    ax1.set_xlabel('X (m)')
    ax1.set_ylabel('Y (m)')
    ax1.set_zlabel('Z (m)')
    plt.colorbar(scatter, ax=ax1, shrink=0.5, label='Z (m)')
    
    # Vista superior (XY)
    ax2 = fig.add_subplot(2, 2, 2)
    scatter = ax2.scatter(data['X'], data['Y'], c=data['Z'], 
                         cmap='plasma', s=2, alpha=0.6, edgecolors='none')
    ax2.set_title('Vista Superior (XY)', fontweight='bold')
    ax2.set_xlabel('X (m)')
    ax2.set_ylabel('Y (m)')
    ax2.set_aspect('equal')
    ax2.grid(True, alpha=0.3, linewidth=0.5)
    plt.colorbar(scatter, ax=ax2, label='Z (m)')
    
    # Vista lateral (XZ)
    ax3 = fig.add_subplot(2, 2, 3)
    color_col = 'Distance' if 'Distance' in data.columns else 'Z'
    scatter = ax3.scatter(data['X'], data['Z'], c=data[color_col], 
                         cmap='coolwarm', s=2, alpha=0.6, edgecolors='none')
    ax3.set_title('Vista Lateral (XZ)', fontweight='bold')
    ax3.set_xlabel('X (m)')
    ax3.set_ylabel('Z (m)')
    ax3.grid(True, alpha=0.3, linewidth=0.5)
    plt.colorbar(scatter, ax=ax3, label=color_col)
    
    # Vista frontal (YZ)
    ax4 = fig.add_subplot(2, 2, 4)
    scatter = ax4.scatter(data['Y'], data['Z'], c=data[color_col], 
                         cmap='coolwarm', s=2, alpha=0.6, edgecolors='none')
    ax4.set_title('Vista Frontal (YZ)', fontweight='bold')
    ax4.set_xlabel('Y (m)')
    ax4.set_ylabel('Z (m)')
    ax4.grid(True, alpha=0.3, linewidth=0.5)
    plt.colorbar(scatter, ax=ax4, label=color_col)
    
    plt.tight_layout()
    plt.show()
    
    print(f"\n=== ESTATÍSTICAS 3D ===")
    print(f"Pontos válidos: {len(data)}")
    print(f"X: {data['X'].min():.3f} a {data['X'].max():.3f}m (Δ={data['X'].max()-data['X'].min():.3f}m)")
    print(f"Y: {data['Y'].min():.3f} a {data['Y'].max():.3f}m (Δ={data['Y'].max()-data['Y'].min():.3f}m)") 
    print(f"Z: {data['Z'].min():.3f} a {data['Z'].max():.3f}m (Δ={data['Z'].max()-data['Z'].min():.3f}m)")
    if 'altura' in data.columns:
        print(f"Camadas únicas: {data['altura'].nunique()}")
        print(f"Alturas: {sorted(data['altura'].unique())}")

def load_and_view(csv_file):
    """Carregar e visualizar nuvem de pontos (2D ou 3D)"""
    try:
        if not os.path.exists(csv_file):
            print(f"❌ Erro: Arquivo '{csv_file}' não encontrado")
            return
        
        print(f"📁 Nome do arquivo CSV: {os.path.basename(csv_file)}")
        print(f"📂 Carregando arquivo...")
        data = pd.read_csv(csv_file)
        print(f"✅ Carregados {len(data)} pontos")
        print(f"📋 Colunas: {list(data.columns)}")
        
        # Mapear colunas
        col_map = {}
        for col in data.columns:
            col_lower = col.lower().strip()
            if col_lower in ['x', 'pos_x', 'position_x']:
                col_map[col] = 'X'
            elif col_lower in ['y', 'pos_y', 'position_y']:
                col_map[col] = 'Y'
            elif col_lower in ['z', 'pos_z', 'position_z', 'height']:
                col_map[col] = 'Z'
            elif col_lower in ['distance', 'dist', 'distancia', 'range']:
                col_map[col] = 'Distance'
            elif col_lower in ['angle', 'angulo', 'theta']:
                col_map[col] = 'Angle'
        
        if col_map:
            data = data.rename(columns=col_map)
            print(f"🔄 Mapeamento: {col_map}")
        
        if 'X' not in data.columns or 'Y' not in data.columns:
            print(f"❌ Erro: Colunas X e Y não encontradas")
            print(f"Disponíveis: {list(data.columns)}")
            return
        
        # Filtrar pontos inválidos
        data = filter_invalid_points(data)
        
        if len(data) == 0:
            print("❌ Nenhum ponto válido após filtragem")
            return
        
        point_type = detect_point_type(data)
        print(f"🎯 Tipo detectado: {point_type}")
        
        if point_type == '3D':
            plot_3d(data)
        else:
            plot_2d(data)
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print(f"{'='*50}")
    print(f"  VISUALIZADOR DE NUVEM DE PONTOS LiDAR v{VERSION}")
    print(f"  Detecção automática 2D/3D")
    print(f"{'='*50}\n")
    
    filename = input("📁 Nome do arquivo CSV: ").strip()
    
    if filename:
        if not os.path.exists(filename) and not os.path.isabs(filename):
            # Tentar em diferentes diretórios
            possible_paths = [
                os.path.join(os.path.dirname(__file__), '..', 'data', 'pontos_reais', filename),
                os.path.join(os.path.dirname(__file__), '..', 'data', 'pontos_camadas', filename),
                os.path.join(os.path.dirname(__file__), '..', 'data', 'pontos_camadas_simulados', filename),
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    filename = path
                    break
        
        load_and_view(filename)
    else:
        print("❌ Nenhum arquivo especificado")
