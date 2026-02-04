@echo off
echo Instalando YDLidar-SDK no ambiente virtual...

REM Criar ambiente virtual
python -m venv .venv

REM Ativar ambiente virtual
call .venv\Scripts\activate.bat

REM Atualizar pip
python -m pip install --upgrade pip

REM Instalar dependências básicas
pip install numpy
pip install matplotlib
pip install pyserial

REM Instalar YDLidar-SDK
pip install ydlidar

REM Verificar instalação
python -c "import ydlidar; print('YDLidar-SDK instalado com sucesso!')"

echo.
echo Instalação concluída!
echo Para ativar o ambiente virtual, execute: .venv\Scripts\activate.bat
pause