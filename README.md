# About the repository

Repository for the implementation of services that allow queries about a model based on the IndoorGML standard and calculate routes. The content of the repository is described below:

## Content

- *Folder **/src**:*
  - *IndoorGMLreader.py:* script to read a model in IndoorGML format and load it into memory.
  - *Server.py:* server in charge of starting the services. On the one hand there is the one in charge of serving the IndoorGML model indicated to the server through the "IgmlLayer" interface (it is located in the UrbanSercice.ice slice in the /slice directory of this same repository). On the other hand there is the service in charge of calculating routes between two points of the model (the same as the one offered by the previous service) and implements the interface "RoutingService" of the "SmartServices" module of the libcitisim package.
  - *Folder **/examples**:* contains all the material necessary for the execution of the three examples proposed in the user manual.

  - *Folder **/lib**:* contains the necessary library to work with Open Location Codes ([repository](https://github.com/google/open-location-code) of the library).

  - *Folder **/slice**:* contains the slice UrbanService.ice necessary for the service in charge of serving the IndoorGML model. It is important to note that it is in PROPORSAL status and is susceptible to being incorporated into libcitisim.

  - *Folder **/test**:* contains everything necessary to run various unit tests of both services.

## User Manual

### Installation of dependencies

To install the dependencies it is necessary to execute the following command in the repository root through the terminal:

~~~~bash
user@machine:~/repos/urban-model-service$ sh install-dependencies.sh
~~~~

### Execution of unit tests

In order to perform the tests and check that everything is working correctly, several steps are required. First of all it is necessary to have the model that is taken as a base to carry out the tests. To do this it is necessary to clone the repository [itsi-indoorGML](https://bitbucket.org/arco_group/itsi-indoorgml/src/master/) in the same directory where the repository [urban-model-service](https://bitbucket.org/arco_group/urban-model-service/src/master/) is located. To do this, the following command is executed in the terminal:

~~~~bash
user@machine:~/repos/$ git clone git@bitbucket.org:arco_group/itsi-indoorgml.git
~~~~

Once the IndoorGML model (model of the building of the Instituto Tecnológico de Sistemas de la Información) is available, we proceed to raise the server that puts into operation the services described above. To do this, execute the following command in the **/test** folder through the terminal:

~~~~bash
user@machine:~/repos/urban-model-service/test$ make run-server-itsi-building 
~~~~

Finally, by executing the following command in the **/test** folder on the terminal, the different unit tests of both services will be launched.

~~~~bash
user@machine:~/repos/urban-model-service/test$ make tests
~~~~

If everything went well, you should see a message like this:

~~~~bash
user@machine:~/repos/urban-model-service/test$ make tests 
nosetests3 unit_tests.py
...................
----------------------------------------------------------------------
Ran 19 tests in 5.541s

OK
~~~~

### Execution of examples

In addition to the unit tests, three examples belonging to different use cases are made available in this repository (in the folder **/example**). It is important to point out that for each of them a different model will be used, so the server will have to be configured according to these needs.

#### Case of use of the building Instituto Tecnológico de Sistemas de la Información

In this example, both services are implemented using the model of the building Instituto Tecnológico de Sistemas de la Información as a reference (available in [itsi-indoorGML](https://bitbucket.org/arco_group/itsi-indoorgml/src/master/)). To do this it is necessary to have the *ITSI.gml* model following the steps mentioned in the previous section. Once these previous steps have been carried out, the server is launched using the following command:

~~~~bash
user@machine:~/repos/urban-model-service/example$ make run-server-itsi-building
~~~~

Once both services have started (the execution of the above command should show the proxy's by the terminal), it is possible to run the example client. This example will make different queries to the services: recover two random cells, show their information and check the relationship between them. To do this, execute the following command in the terminal:

~~~~bash
user@machine:~/repos/urban-model-service/example$ make run-IgmlLayerClient
~~~~

#### Case of use of Citisim

In this example, both services are implemented using the Citisim case model as a reference (available in [itsi-indoorGML](https://bitbucket.org/arco_group/itsi-indoorgml/src/master/)). In order to do this it is necessary to have the *outdoor-indoor-citisim.gml* model following the steps mentioned in the previous section. Once these previous steps have been carried out, the server is launched using the following command:

~~~~bash
user@machine:~/repos/urban-model-service/example$ make run-server-case-citisim
~~~~

Once both services have started (the execution of the above command should show the proxy's by the terminal), it is possible to run the example client. This example will calculate the path between two cells of the model. To do this, run the following command on the terminal:

~~~~bash
user@machine:~/repos/urban-model-service/example$ make run-CaseCITISIM
~~~~

#### Case of paper use [Adapting the IndoorGML Standard to Outdoor Spaces](TODO)

In this example, both services are implemented using the model of the use case proposed in the paper [Adapting the IndoorGML Standard to Outdoor Spaces] (TODO) as a reference. To do this it is necessary to have the model *case_paper_example.gml* found in the **/example** directory. To launch the server, use the following command:

~~~~bash
user@machine:~/repos/urban-model-service/example$ make run-server-case-paper
~~~~

Once both services have started (the execution of the above command should show the proxy's by the terminal), it is possible to run the example client. This example will calculate the path between two cells of the model. To do this, run the following command on the terminal:

~~~~bash
user@machine:~/repos/urban-model-service/example$ TODO
~~~~