# Instalação Manual YDLidar-SDK

## Comandos para executar no terminal:

### Criar ambiente virtual
```bash
python -m venv .venv
```

### Ativar ambiente virtual
**Windows:**
```bash
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```
## Instalar o pip
```bash
sudo apt update
sudo apt install python3-pip
```

### Atualizar pip
```bash
python -m pip install --upgrade pip
```

### Instalar dependências
```bash
pip install -r requirements.txt
```

**OU instalar individualmente:**
```bash
pip install numpy matplotlib pyserial ydlidar
```

# Instalar conda-forge dentro do .venv
```bash
pip install conda
conda install -c conda-forge swig
```

## Instalar o SWIG no sistema
```bash
sudo apt-get install swig
```

### Verificar instalação
```bash
python -c "import ydlidar; print('YDLidar-SDK instalado!')"
```

## Desativar ambiente virtual
```bash
deactivate
```


