# Clonar el proyecto
git clone https://github.com/milesivit/EFI_1_Lopez_Rebeca_ComA
cd EFI-Milena

# Crear el entorno virtual
python3 -m venv env

# Activar el entorno virtual
source env/bin/activate

# Instalar requerimientos
pip install -r requirements.txt

# Correr el proyecto
flask run --reload
