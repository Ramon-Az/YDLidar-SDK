#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def load_and_visualize(csv_file):
    """Carregar e visualizar nuvem de pontos salva"""
    try:
        # Carregar dados do diretório data/nuvem de pontos
        data_dir = os.path.join("data", "nuvem de pontos")
        csv_path = os.path.join(data_dir, csv_file)
        
        data = pd.read_csv(csv_path)
        print(f"Carregados {len(data)} pontos de {csv_path}")
        
        # Visualização 2D
        plt.figure(figsize=(12, 5))
        
        plt.subplot(1, 2, 1)
        plt.scatter(data['X'], data['Y'], c='red', s=1, alpha=0.7)
        plt.title('Vista Superior do Jarro')
        plt.xlabel('X (metros)')
        plt.ylabel('Y (metros)')
        plt.grid(True, alpha=0.3)
        plt.axis('equal')
        
        # Visualização polar
        plt.subplot(1, 2, 2, projection='polar')
        plt.scatter(data['Angle'], data['Distance'], c='blue', s=1, alpha=0.7)
        plt.title('Vista Polar do Jarro')
        
        plt.tight_layout()
        plt.show()
        
        # Estatísticas
        print(f"\nEstatísticas:")
        print(f"Distância mín: {data['Distance'].min():.3f}m")
        print(f"Distância máx: {data['Distance'].max():.3f}m")
        print(f"Distância média: {data['Distance'].mean():.3f}m")
        
    except FileNotFoundError:
        print(f"Arquivo {csv_path} não encontrado")
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    # Exemplo de uso
    csv_file = input("Digite o nome do arquivo CSV: ")
    load_and_visualize(csv_file)
