# Acerca del repositorio

Repositorio destinado a la implementación de servicios que permitan realizar consultas sobre un modelo basado en el estándar IndoorGML y calcular rutas. A continuación se procede a describir el contenido del repositorio:

## Contenido

- *Carpeta **/src**:*
  - *IndoorGMLreader.py:* script encargado de leer un modelo en formato IndoorGML y cargarlo en memoria.
  - *Server.py:* servidor encargado de arrancar los servicios. Por un lado se encuentra el encargado de servir el modelo IndoorGML indicado al servidor a través de la interfaz "IgmlLayer" (se encuentra en el slice UrbanSercice.ice en el directorio /slice de este mismo repositorio). Por otro lado se encuentra el servicio encargado de calcular rutas entre dos puntos del modelo (el mismo que el ofrecido por el anterior servicio) e implementa la interfaz "RoutingService" del módulo "SmartServices" del paquete libcitisim.

- *Carpeta **/examples**:* contiene todo el material necesario para la ejecución de los tres ejemplos que se proponen en el manual de usuario.

- *Carpeta **/lib**:* contiene la librería necesaria para trabajar con códigos Open Location Codes ([repositorio](https://github.com/google/open-location-code) de la librería).

- *Carpeta **/slice**:* contiene el slice UrbanService.ice necesario para el servicio encargado de servir el modelo IndoorGML. Es importante destacar que se encuentra en estado PROPORSAL y es susceptible de ser incorporado a libcitisim.

- *Carpeta **/test**:* contiene todo lo necesario para ejecutar diversas pruebas unitarias de ambos servicios.

## Manual de usuario

### Instalación de dependencias

Para instalar las dependencias es necesario ejecutar el siguiente comando en la raíz del repositorio a través del terminal:

~~~~bash
user@machine:~/repos/urban-model-service$ sh install-dependencies.sh
~~~~

### Ejecución de pruebas unitarias

Para realizar las pruebas y comprobar que todo funciona correctamente hay que llevar a cabo varios pasos. En primer lugar es necesario disponer del modelo que se toma como base para realizar las pruebas. Para ello es necesario clonar el repositorio [itsi-indoorGML](https://bitbucket.org/arco_group/itsi-indoorgml/src/master/) en el mismo directorio donde se encuentra el repositorio [urban-model-service](https://bitbucket.org/arco_group/urban-model-service/src/master/). Para ello se ejecuta el siguiente comando en la terminal:

~~~~bash
user@machine:~/repos/$ git clone git@bitbucket.org:arco_group/itsi-indoorgml.git
~~~~

Una vez disponible el modelo IndoorGML (modelo del edificio del Instituto Tecnológico de Sistemas de la Información) se encuentra disponible, se procede a levantar el servidor que ponga en funcionamiento los servicios descritos anteriormente. Para ello ejecutar el siguiente comando la carpeta **/test** a través de la terminal:

~~~~bash
user@machine:~/repos/urban-model-service/test$ make run-server-itsi-building 
~~~~

Finalmente, ejecutando el siguiente comando en la carpeta **/test** en la terminal, se lanzarán los diferentes tests unitarios de ambos servicios.

~~~~bash
user@machine:~/repos/urban-model-service/test$ make tests
~~~~

Si todo ha ido bien, debería verse un mensaje como este:

~~~~bash
user@machine:~/repos/urban-model-service/test$ make tests 
nosetests3 unit_tests.py
...................
----------------------------------------------------------------------
Ran 19 tests in 5.541s

OK
~~~~

### Ejecución de ejemplos

Además de las pruebas unitarias, en este repositorio se pone a disposición del usuario (en la carpeta **/example**) tres ejemplos pertenecientes a diferentes casos de uso. Es importante destacar que para cada uno de ellos se hará uso de un modelo diferente, por lo que el servidor deberá ser configurado de acuerdo a estas necesidades.

#### Caso de uso del edificio Instituto Tecnológico de Sistemas de la Información

En este ejemplo se pone en marcha ambos servicios teniendo el modelo del edificio Instituto Tecnológico de Sistemas de la Información como referencia (disponible en [itsi-indoorGML](https://bitbucket.org/arco_group/itsi-indoorgml/src/master/)). Para ello es necesario disponer del modelo *ITSI.gml* siguiendo los pasos mencionados en la sección anterior. Una vez realizado estos pasos previos, se procede a lanzar el servidor mediante el siguiente comando:

~~~~bash
user@machine:~/repos/urban-model-service/example$ make run-server-itsi-building
~~~~

Una vez que ambos servicios han arrancado (la ejecución del comando anterior debe mostrar los proxy's por la terminal), es posible ejecutar el cliente de ejemplo. Este ejemplo se encargará de hacer diferentes consultas a los servicios: recuperar dos celdas aleatorias, mostrar la información de las mismas y comprobar la relación existente entre ambas. Para ello ejecute el siguiente comando en la terminal:

~~~~bash
user@machine:~/repos/urban-model-service/example$ make run-IgmlLayerClient
~~~~

#### Caso de uso de Citisim

En este ejemplo se pone en marcha ambos servicios teniendo el modelo del caso de uso de Citisim como referencia (disponible en [itsi-indoorGML](https://bitbucket.org/arco_group/itsi-indoorgml/src/master/)). Para ello es necesario disponer del modelo *outdoor-indoor-citisim.gml* siguiendo los pasos mencionados en la sección anterior. Una vez realizado estos pasos previos, se procede a lanzar el servidor mediante el siguiente comando:

~~~~bash
user@machine:~/repos/urban-model-service/example$ make run-server-case-citisim
~~~~

Una vez que ambos servicios han arrancado (la ejecución del comando anterior debe mostrar los proxy's por la terminal), es posible ejecutar el cliente de ejemplo. Este ejemplo se encargará de calcular la ruta entre dos celdas del modelo. Para ello ejecute el siguiente comando en la terminal:

~~~~bash
user@machine:~/repos/urban-model-service/example$ make run-CaseCITISIM
~~~~

#### Caso de uso del paper [Adapting the IndoorGML Standard to Outdoor Spaces](TODO)

En este ejemplo se pone en marcha ambos servicios teniendo el modelo del caso de uso propuesto en el paper [Adapting the IndoorGML Standard to Outdoor Spaces](TODO) como referencia. Para ello es necesario disponer del modelo *case_paper_example.gml* que se encuentra en el directorio **/example**. Para lanzar el servidor se empleará el siguiente comando:

~~~~bash
user@machine:~/repos/urban-model-service/example$ make run-server-case-paper
~~~~

Una vez que ambos servicios han arrancado (la ejecución del comando anterior debe mostrar los proxy's por la terminal), es posible ejecutar el cliente de ejemplo. Este ejemplo se encargará de calcular la ruta entre dos celdas del modelo. Para ello ejecute el siguiente comando en la terminal:

~~~~bash
user@machine:~/repos/urban-model-service/example$ TODO
~~~~