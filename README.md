# Sistema de Reserva de Mesas - Universidad

Aplicación web completa en Django para gestionar reservas de mesas en la universidad.

## Características

- ✅ Sistema de autenticación con roles (Admin, Alumno, Funcionario)
- ✅ CRUD completo para Usuarios, Mesas, Reservas y Logs de Acceso
- ✅ Validación de disponibilidad de mesas (prevención de solapamiento)
- ✅ Panel de administración Django personalizado
- ✅ Consultas SQL manuales y Django ORM
- ✅ Interfaz responsive con Bootstrap 5
- ✅ Registro automático de accesos (login/logout)

## Requisitos

- Python 3.8+
- Django 5.2.8
- MySQL 8+ (recomendado) o SQLite (desarrollo)
- mysqlclient (adaptador MySQL)

## Instalación

### 1. Instalar dependencias

```bash
python -m pip install -r requirements.txt
```

### 2. Configurar Base de Datos MySQL

**Opción A: MySQL (Producción)**

1. Instalar MySQL en tu sistema
2. Crear la base de datos y el usuario (si tu perfil lo permite):
```sql
CREATE DATABASE reserva_mesas_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'reserva_user'@'%' IDENTIFIED BY 'tu_contraseña';
GRANT ALL PRIVILEGES ON reserva_mesas_db.* TO 'reserva_user'@'%';
FLUSH PRIVILEGES;
```

   > **Si ya tienes una base asignada y no puedes crear otra (por ejemplo `A2025_purra`):**
   > - No necesitas ejecutar `CREATE DATABASE` ni crear otro usuario.
   > - Solo asegúrate de que tu usuario MySQL tenga permisos de lectura/escritura en esa base.
   > - Configura `DB_NAME=A2025_purra` (o el nombre de tu base existente) y usa tus propias credenciales en los pasos siguientes. Las migraciones de Django crearán todas las tablas allí.

3. Configurar variables de entorno (opcional):
```bash
# Copia el archivo de ejemplo
copy .env.example .env

# Edita .env con tus credenciales
DB_NAME=reserva_mesas_db   # cámbialo a A2025_purra si usas tu base asignada
DB_USER=reserva_user       # o tu usuario existente
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=3306
```

**Opción B: SQLite (Desarrollo Local)**

Si prefieres usar SQLite en lugar de PostgreSQL:
1. Abre `reserva_mesas/settings.py`
2. Comenta la configuración de PostgreSQL
3. Descomenta la configuración de SQLite

### 3. Aplicar migraciones

```bash
python manage.py migrate
```

### 4. Crear datos iniciales

```bash
python manage.py crear_datos_iniciales
```

## Credenciales de Acceso

### Administrador
- **Usuario:** admin
- **Contraseña:** admin123

### Alumno de Prueba
- **Usuario:** juan@alumno.cl
- **Contraseña:** test123

### Otros Usuarios
- admin2@universidad.cl / admin123 (Admin)
- maria@alumno.cl / test123 (Alumno)
- carlos@funcionario.cl / test123 (Funcionario)

## Ejecutar el Servidor

```bash
python manage.py runserver
```

Acceder a: http://localhost:8000

## Estructura del Proyecto

```
reserva_mesas/
├── usuarios/           # App de usuarios con roles
├── mesas/             # App de gestión de mesas
├── reservas/          # App de reservas con validaciones
├── accesos/           # App de logs de acceso
├── templates/         # Templates HTML
├── static/            # Archivos estáticos (CSS, JS, imágenes)
└── reserva_mesas/     # Configuración del proyecto
```

## Funcionalidades por Rol

### Administrador
- Gestión completa de usuarios
- Gestión de mesas
- Ver todas las reservas
- Ver logs de acceso
- Acceso al panel Django Admin
- Ver reportes SQL

### Alumno / Funcionario
- Crear reservas
- Ver mis reservas
- Editar mis reservas
- Cancelar mis reservas

## Modelos

### Usuario
- Extiende AbstractUser de Django
- Campos: rol, email (único)
- Roles: admin, alumno, funcionario

### Mesa
- numero_mesa (único)
- capacidad
- ubicacion
- estado (disponible/reservada)

### Reserva
- usuario (FK)
- mesa (FK)
- fecha_reserva
- hora_inicio
- hora_fin
- comentario

### LogAcceso
- usuario (FK)
- accion (login/logout)
- fecha_hora

## Consultas SQL y ORM

### SQL Manual
El sistema incluye un reporte con consulta SQL directa en:
- Ruta: `/reservas/reporte/`
- Vista: `reporte_sql` en `reservas/views.py`

### Django ORM
Ejemplos implementados:
- `select_related()` para optimización de queries
- `filter()` y `exclude()`
- `order_by()` para ordenamiento
- `Q()` para búsquedas complejas
- Validación de solapamiento de reservas

## Panel Admin Django

Acceso: http://localhost:8000/admin/

Características configuradas:
- list_display para todas las entidades
- list_filter para filtrado
- search_fields para búsqueda
- Inline de reservas en el admin de mesas
- Permisos personalizados

## Validaciones Implementadas

1. **Reservas:**
   - Hora inicio < Hora fin
   - No solapamiento de reservas en misma mesa
   - Validación en formulario y modelo

2. **Usuarios:**
   - Email único
   - Username auto-asignado desde email
   - Validación de contraseñas Django

## Migraciones

Las migraciones ya están aplicadas. Para recrearlas:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Datos Iniciales

El comando `crear_datos_iniciales` crea:
- 2 usuarios admin
- 3 usuarios de prueba
- 10 mesas en diferentes ubicaciones

## Tecnologías Utilizadas

- **Backend:** Django 5.2.8
- **Frontend:** HTML5, CSS3, Bootstrap 5
- **Base de Datos:** SQLite (desarrollo) / MySQL (producción)
- **Autenticación:** Django Auth
- **Admin:** Django Admin personalizado

## Navegación

- `/` - Página de inicio
- `/login/` - Iniciar sesión
- `/registro/` - Registrarse
- `/reservas/` - Mis reservas
- `/reservas/crear/` - Nueva reserva
- `/mesas/` - Gestión de mesas (Admin)
- `/usuarios/` - Gestión de usuarios (Admin)
- `/accesos/` - Logs de acceso (Admin)
- `/admin/` - Panel Django Admin

## Notas de Desarrollo

- El proyecto usa SQLite por defecto para facilitar la ejecución
- Para usar MySQL, modificar `DATABASES` en `settings.py`
- Los logs de acceso se registran automáticamente vía signals
- El CSS personalizado está en `static/css/styles.css`

## Cumplimiento de Rúbrica

✅ Modelos con relaciones y validaciones
✅ Migraciones aplicadas
✅ CRUD completo para todas las entidades
✅ Formularios Django con validación
✅ Login y control de acceso por roles
✅ Consultas SQL manuales y ORM
✅ Panel admin configurado
✅ HTML semántico y CSS externo
✅ Arquitectura modular (apps separadas)
✅ Datos iniciales
