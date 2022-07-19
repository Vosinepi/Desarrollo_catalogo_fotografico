<h2 align="center">Albums</h2>

## Contenido

- [Inicio](#inicio)
- [Modulos](#librerias)
- [A fututo](#A_futuro)

## Inicio:

- App realizada en Django y Python que permite la carga de albumes de fotografias para su visualizacion es galerias tipo mosaicos basado en el estilo de Google Photos.
  La app permite cargar directamente desde un archivo zip y genera la compresion de las imaganes y los thumbs necesarios.
- Permite la generacion de usuarios, su registro y la posibilida de resetear contraseña. (el envio de maail esta seteado para la prueba por consola, si desea dejarlo funcional cambiar el EMAIL_BACKEND en settings.py)
- la carga de albumes se realiza mediante admin panel o mediante un usuario con acceso especial a la seccion de la planilla de carga.
- Tiene una seccion buscador.
- App de contacto.

## Modulos / librerias

- Instalar las librerias de Requirement.txt
- Se utliza Sass para la generacion de estilos. Instalar con pip sass processor y agregar a APPS.
- Tambien usamos Imagekit para el procesado de las imagenes. Instalar con pip y agregar a APPS.

## A Futuro

pr

- Implementacion de niveles de usuarios.
- Marca de agua a las fotografias.
- Creacion de un sistema de E-commerce con su correspondiente carro de compras.
- Modo oscuro de la app.
