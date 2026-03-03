#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt

def create_demo_jar_scan():
    """Simular dados de varredura de um jarro para demonstração"""
    # Simular formato de jarro (cilíndrico com variações)
    angles = np.linspace(0, 2*np.pi, 360)
    
    # Base do jarro (raio maior)
    base_radius = 0.08
    # Corpo do jarro (raio menor)
    body_radius = 0.06
    # Boca do jarro (raio médio)
    mouth_radius = 0.07
    
    distances = []
    for angle in angles:
        # Simular formato do jarro com variações
        if 0 <= angle < np.pi/3:  # Base
            radius = base_radius + np.random.normal(0, 0.005)
        elif np.pi/3 <= angle < 5*np.pi/3:  # Corpo
            radius = body_radius + np.random.normal(0, 0.003)
        else:  # Boca
            radius = mouth_radius + np.random.normal(0, 0.004)
        
        # Adicionar distância do centro (jarro a 0.5m do LiDAR)
        distance = 0.5 + radius
        distances.append(distance)
    
    # Converter para coordenadas cartesianas
    x = np.array(distances) * np.cos(angles)
    y = np.array(distances) * np.sin(angles)
    
    return x, y, distances, angles

def show_demo_graphs():
    """Mostrar como ficariam os gráficos da varredura"""
    x, y, distances, angles = create_demo_jar_scan()
    
    # Criar figura com subplots
    fig = plt.figure(figsize=(15, 6))
    
    # Gráfico 1: Vista Superior (Cartesiano)
    plt.subplot(1, 3, 1)
    plt.scatter(x, y, c='red', s=3, alpha=0.8)
    plt.title('Vista Superior do Jarro\n(Coordenadas Cartesianas)', fontsize=12)
    plt.xlabel('X (metros)')
    plt.ylabel('Y (metros)')
    plt.grid(True, alpha=0.3)
    plt.axis('equal')
    
    # Adicionar anotações
    plt.annotate('Base\n(maior)', xy=(0.05, -0.55), fontsize=9, ha='center')
    plt.annotate('Corpo\n(menor)', xy=(-0.55, 0), fontsize=9, ha='center')
    plt.annotate('Boca\n(média)', xy=(0, 0.55), fontsize=9, ha='center')
    
    # Gráfico 2: Vista Polar
    plt.subplot(1, 3, 2, projection='polar')
    plt.scatter(angles, distances, c='blue', s=3, alpha=0.8)
    plt.title('Vista Polar do Jarro\n(Ângulo vs Distância)', fontsize=12)
    plt.ylim(0.4, 0.6)
    
    # Gráfico 3: Perfil de Distâncias
    plt.subplot(1, 3, 3)
    plt.plot(np.degrees(angles), distances, 'g-', linewidth=1)
    plt.title('Perfil de Distâncias\n(Ângulo vs Distância)', fontsize=12)
    plt.xlabel('Ângulo (graus)')
    plt.ylabel('Distância (metros)')
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 360)
    
    # Marcar seções do jarro
    plt.axvspan(0, 60, alpha=0.2, color='red', label='Base')
    plt.axvspan(60, 300, alpha=0.2, color='blue', label='Corpo')
    plt.axvspan(300, 360, alpha=0.2, color='green', label='Boca')
    plt.legend()
    
    plt.tight_layout()
    plt.suptitle('Demonstração: Varredura LiDAR de um Jarro Cerâmico', fontsize=14, y=1.02)
    plt.show()
    
    # Mostrar estatísticas
    print("=== DEMONSTRAÇÃO DE VARREDURA ===")
    print(f"Pontos simulados: {len(x)}")
    print(f"Distância mínima: {min(distances):.3f}m")
    print(f"Distância máxima: {max(distances):.3f}m")
    print(f"Distância média: {np.mean(distances):.3f}m")
    print(f"Variação: {max(distances) - min(distances):.3f}m")

if __name__ == "__main__":
    show_demo_graphs()