# ADO


## Requisitos

Este ejercicio esta construido usando docker y docker-compose.

Instalar docker
* Windows: https://docs.docker.com/desktop/windows/install/
* Mac: https://docs.docker.com/desktop/mac/install/
* Ubuntu: https://docs.docker.com/engine/install/ubuntu/

Instalar docker-compose

* https://docs.docker.com/compose/install/ 

El nombre viene de una empresa de autobuses que existe aquí en el sur de México https://www.ado.com.mx
me parecio adecuado ya que ellos se dedican al giro de este ejercicio.


# Levantar el proyecto 

Debes clonar el siguiente repositorio: https://github.com/edderleonardo/ado 

Una vez clonado entra a la carpeta: *ado* y solo necesitas hacer 

~~~
docker-compose -f local.yml up --build 
~~~

Esto descargara las imagenes de docker que el proyecto necesita para ejecutarse
## Crear super usuario en django 

~~~
docker-compose -f local.yml run --rm django python manage.py createsuperuser
~~~

## Cargar fixtures (opcional)

Si lo desea he creado unos datos dummies, para poder importarlos solo debe hacer

~~~
docker-compose -f local.yml run --rm django python manage.py loaddata fixtures/dummy_data.json 
~~~

# Test

Para correr todos los test debes usar el comando

~~~
docker-compose -f local.yml run --rm django pytest
~~~


