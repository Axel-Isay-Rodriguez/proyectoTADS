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
> Es nesesario usar los comandos
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

