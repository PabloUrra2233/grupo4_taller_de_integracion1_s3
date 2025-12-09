# Reporte Técnico: Tuplas y Flujos de la Aplicación

## 1. Uso de Tuplas (Choices) en Django

Se han identificado 3 estructuras de tuplas utilizadas para definir opciones inmutables en los modelos (patrón `TextChoices`).

| Aplicación | Archivo | Modelo | Clase | Tupla / Choices | Valores |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Mesas** | `mesas/models.py` | `Mesa` | `Estado` | `DISPONIBLE`, `RESERVADA` | `'disponible'`, `'reservada'` |
| **Usuarios** | `usuarios/models.py` | `Usuario` | `Rol` | `ADMIN`, `ALUMNO`, `FUNCIONARIO` | `'admin'`, `'alumno'`, `'funcionario'` |
| **Accesos** | `accesos/models.py` | `LogAcceso` | `Accion` | `LOGIN`, `LOGOUT` | `'login'`, `'logout'` |

---

## 2. Flujos de la Aplicación

### A. Autenticación y Usuarios (`usuarios`)

Gestión de identidad y roles.
--**Registro**: Vista personalizada `registro` que crea el usuario y lo autentica automáticamente (`login(request, user)`).
--**Login/Logout**: Utiliza las vistas genéricas de Django (`LoginView`, `LogoutView`).
--**Roles**: Se distinguen roles (Admin, Alumno, Funcionario) que condicionan el acceso a otras áreas.
--**Gestión (Admin)**: CRUD completo protegido por `@user_passes_test(is_admin)`.

### B. Registro de Accesos (`accesos`)

Sistema automatizado de auditoría.
--**Generación**: No depende de vistas. Utiliza **Signals** de Django (`user_logged_in`, `user_logged_out`) en `accesos/signals.py` para crear registros automáticamente cada vez que un usuario inicia o cierra sesión.
--**Visualización**: Listado de logs visible solo para administradores.

### C. Gestión de Mesas (`mesas`)

Administración de recursos físicos.
--**FLUJO CRUD**: Crear, Leer, Actualizar y Eliminar mesas.
--**Seguridad**: Todas las vistas requieren rol de Administrador.

### D. Sistema de Reservas (`reservas`)

Núcleo lógico de la aplicación.
1.**Solicitud (Formulario)**:
    - El usuario envía datos (fecha, hora).
    - **Validación 1 (Vista)**: Reglas de frecuencia.
        - Máximo 1 reserva por día.
        - Máximo 3 reservas por semana.
2.**Persistencia (Modelo)**:
    - Al llamar a `save()`, se ejecuta `clean()`.
    - **Validación 2 (Reglas de Negocio)**:
        - No fechas pasadas.
        - Antelación máxima de 7 días.
        - Prohibido reservar sábados y domingos.
        - Horario permitido restringido (08:00 - 19:00).
3.**Reportes**:
    - Vista `reporte_sql` que ejecuta SQL nativo para estadísticas avanzadas (Admin).
