# Instrucciones
Si clonas este repositorio primero debes de activar el entorno virtual

```
cd entornoApi
cd Scripts
activate
```
Después debes de salir con **cd ..** hasta la raíz del proyecto e instalar los requerimientos

# Comando para instalar los requerimientos
```
pip install -r requirements.txt
```
con esto ya puedes correr la Api con el siquiente comando:

# Comandos para correr fastapi
```
python -m fastapi dev main.py
```

# Comandos útiles relacionados:
Si quieres **ver qué se va a guardar** antes de escribirlo:
```
pip freeze
```

Si quieres **actualizar** solo los paquetes que cambiaron (sin sobrescribir todo manualmente):

```
pip freeze > requirements.txt
```