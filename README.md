# Proyecto DB_Proyecto – Web + MySQL (BeautyControl)

Este repositorio contiene una aplicación web creada con **Python + Reflex** conectada a una base de datos **MySQL** para el proyecto de Manejo de Bases de Datos.

La app permite conectarse a la base local `BeautyControl` (creada desde MySQL Workbench) y ejecutar lógica desde una página web (por ejemplo: crear datos de prueba en las tablas `Countries` y `Cities` desde un botón).

---

## 1. Requisitos previos

Cada integrante del equipo necesita tener instalado:

- **Python 3.11**
- **MySQL Server 8** (o compatible)  
- **MySQL Workbench** (para ejecutar el script .sql)
- **Git** + **GitHub Desktop** (para clonar el repositorio)
- Navegador web (Chrome, Edge, etc.)

> Verifica que `python` o `py` esté en el PATH:
> ```bash
> python --version
> ```

---

## 2. Clonar el repositorio

1. Abrir **GitHub Desktop**.
2. Ir a **File → Clone repository…**.
3. Seleccionar el repositorio `DB_Proyecto` del equipo.
4. Elegir una carpeta local, por ejemplo:
   `C:\Users\TU_USUARIO\Desktop\DB_Proyecto`
5. Hacer clic en **Clone**.

Luego pueden abrir la carpeta clonada en **VS Code**.

---

## 3. Crear y activar el entorno virtual

Dentro de la carpeta del proyecto (raíz, donde está `rxconfig.py`):

1. Abrir una terminal (PowerShell, CMD o terminal integrada de VS Code).

2. Crear el entorno virtual:

```bash
py -3.11 -m venv .venv
```

3. Activar el entorno virtual (Windows):

```bash
.\.venv\Scripts\activate
```
Si no funciona intentar con este:

```bash
source .venv/Scripts/activate
```

Si se activó bien, deberías ver algo como `(.venv)` al inicio de la línea de la terminal.

---

## 4. Instalar las dependencias (requirements)

En el entorno virtual activo, ejecutar:

```bash
pip install -r requirements.txt
```

Este comando instala:

- **Reflex** (framework web).
- **mysql-connector-python** (conexión a MySQL).
- Y cualquier otra librería necesaria para el proyecto.

---

## 5. Crear la base de datos local en MySQL Workbench

Cada integrante debe tener su propia base de datos local.

1. Abrir **MySQL Workbench**.
2. Conectarse al servidor local (por ejemplo `localhost`, usuario `root`).
3. Abrir el archivo SQL del proyecto:

   `SQL_DB_Template/ControlBeautyDB.sql`

4. Ejecutar todo el script:
   - Crea el esquema `BeautyControl`.
   - Crea todas las tablas (`Countries`, `Cities`, etc.).

5. Verificar:

```sql
SHOW DATABASES;
USE BeautyControl;
SHOW TABLES;
```

Deberías ver todas las tablas del modelo (Countries, Cities, ...).

---

## 6. Configurar conexión a la base de datos

El archivo que maneja la conexión está en:

`DB_Proyecto/db.py`

Dentro hay un diccionario `DB_CONFIG` como este:

```python
DB_CONFIG = {
    "host": "localhost",
    "user": "tu_usuario_mysql",
    "password": "tu_password_mysql",
    "database": "BeautyControl",
    "port": 3306,
}
```

Cada integrante debe cambiar:

- `"user"` → por su usuario de MySQL (ej. `"root"`).
- `"password"` → por su contraseña de MySQL.
- `"database"` → debe ser `"BeautyControl"` (si el schema se llama así).

> No subir usuarios/contraseñas reales en capturas, solo usarlos localmente.

---

## 7. Ejecutar la aplicación Reflex

Desde la carpeta raíz del proyecto (donde está `rxconfig.py`) y con el entorno virtual activo:

```bash
reflex run
```

- El backend corre en un puerto interno (ej. 8001).
- El frontend de Reflex se sirve en:

👉 `http://localhost:3000`

Abrir esa URL en el navegador.

---

## 8. Probar que todo funciona

En la página principal verás un botón, por ejemplo:

- **"Crear datos de Cities"**

Flujo de prueba:

1. Asegúrate que las tablas `Countries` y `Cities` están vacías:

   ```sql
   USE BeautyControl;
   SELECT * FROM Countries;
   SELECT * FROM Cities;
   ```

2. En la web, haz clic en **"Crear datos de Cities"**.
3. Si todo sale bien, se mostrará un mensaje tipo:

   > ✅ Datos de Countries y Cities creados correctamente.

4. Vuelve a MySQL Workbench y revisa:

   ```sql
   SELECT * FROM Countries;
   SELECT * FROM Cities;
   ```

Ahora deberían aparecer registros de ejemplo (países y ciudades), creados desde la página web.

---

## 9. Trabajo colaborativo (GitHub Desktop)

### Para mandar cambios al repositorio:

1. Abrir el proyecto en **VS Code**, hacer cambios.
2. Abrir **GitHub Desktop**:
   - Verás los archivos modificados en la pestaña **Changes**.
3. Escribir un mensaje de commit descriptivo (ej. `Agrego módulo de productos`).
4. Clic en **Commit to main** (o a la rama que corresponda).
5. Clic en **Push origin** para subir al repositorio remoto en GitHub.

### Para traer cambios de otros compañeros:

1. En GitHub Desktop, clic en **Fetch origin**.
2. Luego **Pull origin** (si hay cambios nuevos).

---

## 10. Notas importantes

- La carpeta del entorno virtual `.venv/` está incluida en `.gitignore`, por lo tanto **no se sube al repositorio**.
- Cada integrante debe crear su propio entorno virtual local.
- La base de datos es **local**; el script `.sql` garantiza que todos tengan la misma estructura.
- Para agregar nuevas funcionalidades (CRUD de productos, órdenes, vistas, etc.) todos deben seguir este flujo:
  1. `git pull` (traer cambios).
  2. Activar `.venv` y `reflex run` para probar.
  3. Implementar cambios.
  4. `git commit` + `git push`.

---
