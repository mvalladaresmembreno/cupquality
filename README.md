# cupquality
📋 Requisitos
Python 3.8+
pip
Git
Base de datos (PostgreSQL)

🔧 Instalación

Clona el repositorio
git clone https://github.com/mvalladaresmembreno/cupquality.git
cd cupquality

Crea y activa un entorno virtual
python3 -m venv venv
source venv/bin/activate       # En Linux/macOS
venv\Scripts\activate          # En Windows


Instala las dependencias
pip install --upgrade pip
pip install -r requirements.txt


⚙️ Configuración
Variables de entorno

Crea un archivo .env en la raíz

Define al menos:

ini

SECRET_KEY=tu_clave_secreta
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
Si vas a usar otra base de datos, añade:
DATABASE_URL=...


🗄️ Migraciones y carga de datos
Ejecuta migraciones:

python manage.py migrate

Crea un superusuario:
python manage.py createsuperuser

▶️ Ejecución
Arranca el servidor de desarrollo:
python manage.py runserver
Por defecto, estará activo en http://127.0.0.1:8000/.

