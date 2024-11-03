# proyectoTADS
Vamos a usar Mysql https://dev.mysql.com/downloads/installer/ instalenlo 
al momento de instalacion hagan un usuario 
Usuario:tec
Pass:tecnologico
para crear la base de datos 

CREATE DATABASE tecInv CHARACTER SET UTF8; 

para que este parejo durante el desarrollo 
ya esta algo arriba , creo asi que pues ya iremos trabajando 
primero lo importante es que corra , des pues vemos lo demas



# Pa bajarlo desde el CMD
Clonar el repositorio
```javascript
git clone https://github.com/wazazky/proyectoTADS.git
```
Cambiar al directorio del proyecto
```javascript
cd proyectoTADS
```

Antes de trabajar se tiene que traer los cambios del repositorio remoto
```javascript
git pull origin main
```
> [!IMPORTANT]  
> Es nesesario usar los comandos antes de ejecutar el server , porque se estan ajustando los modelos aun
> ```javascript
> python manage.py makemigrations
> ```
> ```javascript
> python manage.py migrate
> ```

# Pa subirlo
Cambiar al directorio del proyecto 

```javascript
cd proyectoTADS
```
Agregar los cambios al área de ensayo
```javascript
git add . 
```
Crear una confirmación
```javascript
 git commit -m "Actualización del proyecto" 
```
Subir las confirmaciones al repositorio remoto , de preferencia no usen el main usen el suyo
```javascript
 git push origin main
```
# Proyecto de Sistema de Gestión de Inventario y Préstamos

Este proyecto tiene como objetivo desarrollar un sistema para gestionar el inventario de materiales y herramientas, así como el préstamo de dichos materiales en una escuela. El sistema está dirigido principalmente al control de inventario para herramientas, conectores, materiales de mantenimiento, pintura, etc., y tiene un sistema de préstamos que permite registrar materiales en diferentes presentaciones (por ejemplo, rollos y metros de cable).

## Características Principales del Sistema

- **Gestor de Inventario**: Registro y actualización de materiales, herramientas y productos, incluyendo el manejo de cantidades disponibles y presentaciones diferentes.
- **Sistema de Préstamos**: Préstamos de múltiples productos a la vez, vinculados a un usuario y opcionalmente a una orden de trabajo.
- **Orden de Trabajo**: Registro de órdenes de trabajo con descripción de los materiales utilizados, lugar y estado del trabajo.
- **Control de Usuarios y Roles**: Diferentes tipos de usuarios con permisos distintos para realizar tareas específicas en el sistema.

## Modelos de Datos

### 1. `Partida`
Representa la clasificación del gasto de los materiales según las especificaciones del gobierno.

- `nombre`: Nombre de la partida.
- `descripcion`: Descripción opcional de la partida.

### 2. `UnidadMedida`
Define las unidades de medida para los productos, como metros, litros, unidades, etc.

- `nombre`: Nombre de la unidad de medida.

### 3. `Categoria`
Clasifica los productos en diferentes categorías como herramientas, pintura, conectores, etc.

- `nombre`: Nombre de la categoría.

### 4. `Producto`
Almacena información sobre los productos disponibles en el inventario.

- `nombre`: Nombre del producto.
- `descripcion`: Descripción opcional del producto.
- `partida`: Relación con la partida correspondiente.
- `categoria`: Relación con la categoría correspondiente.
- `unidad_medida`: Unidad de medida del producto.
- `cantidad_disponible`: Cantidad disponible en inventario.
- `estado`: Estado del producto ("bueno", "malo", "regular", "sin estado").

### 5. `Prestamo`
Representa el préstamo de uno o más productos a un usuario.

- `usuario`: Usuario que realizó el préstamo.
- `fecha_inicio`: Fecha en que se inició el préstamo (por defecto el día actual).
- `fecha_fin`: Fecha de finalización del préstamo (puede ser cambiada).
- `activo`: Indica si el préstamo está activo o no.

### 6. `PrestamoDetalle`
Detalla los productos que forman parte de un préstamo.

- `prestamo`: Relación con el préstamo correspondiente.
- `producto`: Producto que se está prestando.
- `cantidad`: Cantidad de producto prestado.
- `estado`: Estado del detalle del préstamo ("prestado", "regresado", "consumido").

### 7. `OrdenTrabajo`
Representa una orden de trabajo que podría involucrar el uso de ciertos materiales.

- `lugar`: Lugar donde se realiza el trabajo.
- `tipo_trabajo`: Tipo de trabajo a realizar.
- `descripcion`: Descripción del trabajo.
- `estado`: Estado de la orden de trabajo ("sin asignar", "en proceso", "finalizado", "truncada").
- `usuario_creador`: Usuario que creó la orden de trabajo.
- `usuario_asignado`: Usuario al que se le asignó la orden de trabajo.

## Procedimientos Implementados

- **Reducción de Inventario**: Al registrar un `PrestamoDetalle`, el sistema verifica si la cantidad solicitada del producto está disponible y, si es así, la reduce del inventario.
- **Devolución de Productos**: Si se elimina un `PrestamoDetalle` con estado "prestado", la cantidad prestada es devuelta al inventario.
- **Cierre de Préstamo**: Cuando todos los detalles de un préstamo están en estado "regresado" o "consumido", el préstamo es marcado como inactivo.

## Vistas Principales

- **Login y Registro de Usuarios**: Páginas para iniciar sesión y registrar usuarios, asignando por defecto los permisos más bajos.
- **Panel de Administración**: 
  - **Admin Dashboard**: Vista para que los administradores gestionen usuarios, asignen grupos, y vean la lista de usuarios pendientes por asignar.
  - **Gestionar Productos**: Permite agregar, modificar y listar los productos del inventario.
  - **Gestionar Préstamos y Órdenes de Trabajo**: Gestiona la creación y actualización de préstamos, así como de órdenes de trabajo.

## Control de Accesos
- **Grupos de Usuarios**: 
  - **Administrador**: Tiene acceso a todas las funcionalidades del sistema, incluyendo agregar/modificar inventario y gestionar usuarios.
  - **Operador**: Puede generar órdenes de trabajo y préstamos.
  - **Usuario Avanzado**: Puede ver sus órdenes de trabajo y préstamos pendientes.
  - **Usuario Básico**: Solo puede ver sus préstamos pendientes.

El acceso a las vistas y funcionalidades está restringido según el grupo al que pertenezca el usuario, asegurándose de que solo pueda ver y realizar las acciones que le estén permitidas.

## Instrucciones de Instalación
1. **Clonar el Repositorio**: Clona el repositorio del proyecto a tu máquina local.

   ```bash
   git clone <URL del repositorio>
   cd proyectoTADS
   ```

2. **Instalar Dependencias**: Instala los paquetes requeridos utilizando `pip`.

   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar la Base de Datos**:
   - Configura los detalles de la base de datos en el archivo `settings.py` (asegúrate de tener MySQL configurado).

4. **Aplicar Migraciones**:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Crear un Superusuario**:

   ```bash
   python manage.py createsuperuser
   ```

6. **Correr el Servidor de Desarrollo**:

   ```bash
   python manage.py runserver
   ```

7. **Acceder al Sistema**: Ingresa a `http://127.0.0.1:8000/` para comenzar a utilizar la aplicación.

## Notas Adicionales
- **Cerrar Sesión Automática**: La sesión del usuario se cierra automáticamente al cerrar la ventana del navegador.
- **Seguridad CSRF**: Los formularios del sistema cuentan con protección CSRF para evitar ataques de falsificación de solicitudes.

## Futuras Mejoras
- **Reportes y Estadísticas**: Implementar reportes de uso de inventario y estadísticas de préstamos.
- **Notificaciones**: Notificar a los usuarios sobre órdenes de trabajo pendientes o préstamos que necesiten devolución.
- **Mejoras en la Interfaz**: Optimizar la interfaz para una mejor experiencia de usuario.

## Contribuciones
Las contribuciones son bienvenidas. Si deseas contribuir al proyecto, por favor abre un `issue` o realiza un `pull request` con tus cambios.

## Licencia
Este proyecto está bajo la licencia MIT.


