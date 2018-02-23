Repositorio destinado a la implementación de servicios que permitan realizar consultas sobre un modelo basado en el estandar IndoorGML.

NOTA: este proyecto se está llevando a cabo siguiendo una metodología TDD (o eso se intenta).

NOTA: la interfaz ice aun está en estado PROPOSAL, por lo que no se encuentra aún en ningún paquete.

# Manual de usuario
Para instalar las dependencias:
- En la raíz del repositorio, hacer "sh install-dependencies.sh"

Para levantar el servicio:
- Si no tienes el repositorio itsi.indoorgml en ~/repos/, debes cambiar la ruta del modelo en el Makefile.
- En ./src/ hacer "make run-server".

Para realizar las pruebas y comprobar que todo funciona correctamente:
- Hacer "make tests" en la raíz del repositorio.
