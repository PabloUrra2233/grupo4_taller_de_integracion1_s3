# Documentación Técnica: Sistema de Reserva de Mesas

## 1. Introducción y Objetivos

El **Sistema de Reserva de Mesas** es una aplicación web desarrollada para gestionar de manera eficiente el uso de mesas de estudio o trabajo dentro de una institución universitaria. El objetivo principal es reemplazar los sistemas manuales o basados en papel, proporcionando una plataforma centralizada, accesible y segura para alumnos, funcionarios y administradores.

### Objetivos Específicos
- **Automatización:** Eliminar la necesidad de gestión manual de reservas.
- **Control:** Evitar conflictos de horarios (dobles reservas).
- **Seguridad:** Restringir el acceso según roles de usuario.
- **Auditoría:** Mantener un registro de quién accede al sistema.

---

## 2. Arquitectura del Sistema

El proyecto sigue el patrón de diseño **MVT (Model-View-Template)** propio de Django, que promueve una separación clara de responsabilidades.

### Estructura Modular
Para mantener el código organizado y escalable, el sistema se ha dividido en cuatro aplicaciones Django independientes (`apps`), cada una con una responsabilidad única:

1.  **`usuarios`**: Gestiona la autenticación, el modelo de usuario personalizado y los roles.
2.  **`mesas`**: Administra el inventario de mesas (creación, edición, estado).
3.  **`reservas`**: Contiene la lógica central del negocio (reservar, validar disponibilidad, cancelar).
4.  **`accesos`**: Se encarga de la auditoría y registro de logs de seguridad.

---

## 3. Diseño de Base de Datos

El sistema utiliza una base de datos relacional (PostgreSQL en producción, SQLite en desarrollo).

### Modelos Principales

#### 3.1. Usuario (`usuarios.Usuario`)
Extiende del modelo `AbstractUser` de Django para añadir campos específicos sin perder la funcionalidad de autenticación nativa.
- **Campos clave:** `email` (identificador único), `rol` (Admin, Alumno, Funcionario).
- **Decisión de diseño:** Se usa el email como nombre de usuario para facilitar el login.

#### 3.2. Mesa (`mesas.Mesa`)
Representa el recurso físico a reservar.
- **Campos clave:** `numero_mesa` (único), `capacidad`, `estado`.

#### 3.3. Reserva (`reservas.Reserva`)
La tabla pivote que conecta Usuarios y Mesas en el tiempo.
- **Relaciones:** ForeignKey a `Usuario` y `Mesa`.
- **Validaciones:** Incluye lógica para asegurar que `hora_inicio < hora_fin`.

#### 3.4. LogAcceso (`accesos.LogAcceso`)
Tabla de auditoría.
- **Funcionamiento:** No se crean registros manualmente en las vistas. Se utilizan **Django Signals** (`user_logged_in`, `user_logged_out`) para interceptar los eventos de autenticación y registrar el log automáticamente.

---

## 4. Lógica de Negocio y Validaciones

### Prevención de Solapamiento (Overlapping)
El desafío técnico más importante es evitar que dos usuarios reserven la misma mesa a la misma hora. Esto se maneja en el método `clean()` del formulario `ReservaForm`.

**Lógica implementada:**
Se busca si existe alguna reserva para la misma mesa en la misma fecha que cumpla cualquiera de estas condiciones:
1.  Comience antes y termine después del inicio de la nueva reserva.
2.  Comience antes del fin de la nueva reserva y termine después.
3.  Esté completamente contenida dentro del horario de la nueva reserva.

Se utiliza `Q objects` de Django para construir esta consulta compleja de manera eficiente.

### Consultas SQL Manuales
Aunque el ORM de Django es potente, el sistema incluye un módulo de reportes que ejecuta **SQL crudo** (`connection.cursor()`) para demostrar la capacidad de integración con consultas directas a la base de datos, optimizando reportes complejos que requieren múltiples `JOINs`.

---

## 5. Seguridad

- **Autenticación:** Uso de `django.contrib.auth`.
- **Autorización:** Decoradores `@login_required` y `@user_passes_test` para proteger vistas según el rol del usuario (ej. solo administradores pueden crear mesas).
- **Protección CSRF:** Todos los formularios incluyen el token CSRF para prevenir ataques de falsificación de solicitudes.
- **Variables de Entorno:** Las credenciales de base de datos y claves secretas se gestionan mediante archivos `.env`, no hardcodeadas en el código (siguiendo la metodología 12-Factor App).

---

## 6. Tecnologías Utilizadas

- **Backend:** Python 3.14, Django 5.2.8.
- **Base de Datos:** PostgreSQL (driver `psycopg` v3).
- **Frontend:** HTML5, CSS3, Bootstrap 5 (para diseño responsivo).
- **Control de Versiones:** Git y GitHub.

---

## 7. Despliegue e Instalación

El proyecto está configurado para ser agnóstico del entorno.
- **Desarrollo:** Puede correr con SQLite para pruebas rápidas.
- **Producción:** Se conecta a PostgreSQL mediante configuración en `settings.py` y variables de entorno.

### Requisitos
- `requirements.txt`: Lista todas las dependencias necesarias.
- `crear_datos_iniciales`: Comando personalizado (`management command`) para poblar la base de datos con usuarios y mesas de prueba, facilitando el despliegue inicial.
