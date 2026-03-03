# 🎯 Projeto IC: Sensor LiDAR para Varreduras em Ambientes Fechados

<div align="center">

![YDLIDAR](doc/images/YDLidar.jpg)

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE.txt)
[![YDLidar SDK](https://img.shields.io/badge/YDLidar-SDK-orange.svg)](https://github.com/YDLIDAR/YDLidar-SDK)

**Projeto de Iniciação Científica - PAIC/UEA**  
*Estudo de técnicas de utilização do sensor LiDAR X2L em ambientes fechados controlados*

</div>

---

## 📋 Sobre o Projeto

Este projeto acadêmico de Iniciação Científica da **Universidade do Estado do Amazonas (UEA)** investiga as aplicações e configurações do sensor LiDAR para varreduras em ambientes fechados, com foco em aquisição, tratamento e modelagem 3D de nuvens de pontos.

### 🎓 Objetivo Geral

Estudar as configurações do sensor LiDAR usadas para varreduras em ambientes fechados.

### 🔬 Objetivos Específicos

- **Aquisição de Dados**: Conhecer as formas de aquisição das nuvens de pontos geradas pelo sensor LiDAR
- **Tratamento de Dados**: Estudar técnicas de processamento e filtragem de nuvens de pontos
- **Modelagem 3D**: Estudar procedimentos para renderização e modelagem 3D das nuvens de pontos

---

## 🏗️ Estrutura do Projeto

```
YDLidar-SDK/
│
├── projeto-IC-lidar-x2l/          # 🎯 Projeto Principal de IC
│   ├── assets/                     # Recursos visuais e imagens
│   ├── data/                       # Dados coletados
│   │   ├── pontos-reais/          # Varreduras reais do sensor
│   │   └── pontos-reais-por-camadas/  # Dados organizados por altura
│   ├── docs/                       # Documentação técnica
│   ├── tests/                      # Testes e experimentos
│   │   ├── testes-pendentes/
│   │   ├── testes-reais-versoes-anteriores/
│   │   ├── testes-simulados/
│   │   └── testes-visualizacao-pontos-reais/
│   ├── lidar-config.py            # Configurações do sistema
│   ├── requirements.txt           # Dependências Python
│   ├── teste-lidar-x2l-camadas-v1.0.py
│   ├── teste-lidar-x2l-v1.2.py
│   └── teste-visualizador-2d-3d-pointcloud-v1.2.py
│
├── core/                          # Núcleo do SDK YDLidar
├── src/                           # Código fonte dos drivers
├── python/                        # Bindings Python
├── examples/                      # Exemplos oficiais do SDK
└── doc/                           # Documentação oficial YDLidar
```

---

## 🚀 Funcionalidades Implementadas

### ✅ Scanner Básico 2D
- Configuração otimizada para LiDAR X2L (115200 baud, TYPE_TRIANGLE)
- Coleta de pontos com conversão polar → cartesiano
- Salvamento em formato CSV
- Visualização 2D e polar

### ✅ Scanner por Camadas
- Organização de dados por altura
- Navegação interativa entre fatias horizontais
- Estatísticas por camada
- Análise de perfil radial 360°

### ✅ Visualização 3D
- Nuvem de pontos tridimensional (X, Y, Z)
- Múltiplas perspectivas
- Coloração por altura/distância

### ✅ Interface Tempo Real
- Controles interativos (botões + sliders)
- Coleta automática por alturas
- Exportação de dados processados

---

## 🛠️ Tecnologias Utilizadas

### Hardware
- **Sensor**: YDLidar X2L (2D LiDAR)
- **Interface**: USB Serial (115200 baud)
- **Alcance**: 0.1m - 8m
- **Frequência**: 8-10 Hz
- **Sample Rate**: 3000 pontos/segundo

### Software
| Tecnologia | Versão | Uso |
|------------|--------|-----|
| Python | 3.8+ | Linguagem principal |
| YDLidar SDK | 1.0.0+ | Driver do sensor |
| NumPy | 1.21.0+ | Computação numérica |
| Matplotlib | 3.5.0+ | Visualização de dados |
| PySerial | 3.5+ | Comunicação serial |

---

## 📦 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- Git
- Ambiente Windows/Linux

### Passo a Passo

1. **Clone o repositório**
```bash
git clone https://github.com/Ramon-Az/YDLidar-SDK.git
cd YDLidar-SDK/projeto-IC-lidar-x2l
```

2. **Crie um ambiente virtual**
```bash
python -m venv .venv
```

3. **Ative o ambiente virtual**
```bash
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

4. **Instale as dependências**
```bash
pip install -r requirements.txt
```

5. **Verifique a instalação**
```bash
python -c "import ydlidar; print('YDLidar SDK instalado com sucesso!')"
```

### 🔧 Configuração da Porta Serial

**Windows**: Verifique a porta COM no Gerenciador de Dispositivos (geralmente `COM3`)

**Linux**: Configure permissões USB
```bash
sudo chmod 666 /dev/ttyUSB0
```

---

## 💻 Como Usar

### Teste Básico do Sensor
```bash
python teste-lidar-x2l-v1.2.py
```

### Varredura por Camadas
```bash
python teste-lidar-x2l-camadas-v1.0.py
```

### Visualização 3D de Nuvem de Pontos
```bash
python teste-visualizador-2d-3d-pointcloud-v1.2.py
```

---

## 📊 Resultados e Aplicações

### Casos de Uso Demonstrados

#### 🏺 Varredura de Objetos
- Mapeamento de objetos cerâmicos
- Análise dimensional precisa
- Reconstrução de perfil 2D/3D

#### 🏠 Mapeamento de Ambientes
- Plantas baixas de ambientes fechados
- Detecção de obstáculos
- Medições de distância

#### 📐 Análise Geométrica
- Medições de distância
- Medições de perímetro
- Análise de simetria

---

## 📚 Documentação

A documentação completa está disponível na pasta [`projeto-IC-lidar-x2l/docs/`](projeto-IC-lidar-x2l/docs/):

- [01 - Manual de Instalação](projeto-IC-lidar-x2l/docs/01-install-manual.md)
- [02 - Guia de Configuração GitHub](projeto-IC-lidar-x2l/docs/02-guia-mudar-diretorio-github.md)
- [03 - Resumo Completo do Projeto](projeto-IC-lidar-x2l/docs/03-resumo-projeto-lidar-x2l.md)
- [04 - Solução de Problemas Python](projeto-IC-lidar-x2l/docs/04-solucao-pythoninterp.md)
- [05 - Análise de Visualizações](projeto-IC-lidar-x2l/docs/05-analise-visualizacoes-pontos-v1.1-v1.2.md)

---

## 🔬 Metodologia

### Processo de Varredura 3D

1. **Posicionamento**: Objeto fixado em altura específica
2. **Varredura**: Coleta de pontos 2D (5 segundos por camada)
3. **Elevação**: Ajuste manual da altura
4. **Repetição**: Múltiplas camadas até cobertura completa
5. **Integração**: Combinação de todas as camadas em nuvem 3D

### Formatos de Dados

**CSV Básico (2D)**
```csv
X, Y, Distance, Angle
```

**CSV Completo (3D)**
```csv
X, Y, Z, Distance, Angle, Height_cm, Layer
```

---

## 🎯 Próximos Passos

- [ ] Integração com sistema motorizado para varredura automática
- [ ] Algoritmos avançados de reconstrução 3D
- [ ] Detecção automática de objetos
- [ ] Exportação para formatos 3D padrão (STL, PLY, OBJ)
- [ ] Implementação de filtros de ruído avançados
- [ ] Sistema de calibração automática

---

## 👥 Equipe

| Nome | Papel |
|------|-------|
| **Sarah** | Orientanda |
| **Clarice** | Coorientadora |
| **Adriano** | Orientador |
| **Ramon Azevedo** | Colaborador Chefe|

---

## 📄 Licença

Este projeto utiliza o [YDLidar-SDK](https://github.com/YDLIDAR/YDLidar-SDK) sob a licença MIT. Consulte o arquivo [LICENSE.txt](LICENSE.txt) para mais detalhes.

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

---

## 📞 Contato

**Universidade do Estado do Amazonas (UEA)**  
Programa de Apoio à Iniciação Científica (PAIC)

Para dúvidas ou sugestões sobre o projeto, entre em contato com a equipe.

---

## 🙏 Agradecimentos

- **UEA** - Universidade do Estado do Amazonas
- **PAIC** - Programa de Apoio à Iniciação Científica
- **YDLidar** - Pelo SDK e suporte técnico
- Comunidade open-source Python

---

<div align="center">

**Desenvolvido com ❤️ pela equipe PAIC/UEA**

[⬆ Voltar ao topo](#-projeto-ic-sensor-lidar-para-varreduras-em-ambientes-fechados)

</div>
