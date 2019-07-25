Clairvoyant Backend
===================

Setup
-----
Ensure JDK 8 is installed (`javac -version` should report 1.8+), then open this directory (backend) in IntelliJ as an existing Maven project. Once the project has finished indexing set the following:

- IntelliJ > Preferences > Java Compiler: set project and target bytecode version to 1.8

- File > Project Structure > Project: 
  - set Project SDK to location of Java 1.8 home directory
  - set Project Language Level to 8
  
- File > Project Structure > Module: 
  - Sources: set Project Language Level to 8
  - Dependencies: set Module SDK to Project SDK (1.8)
  
- File > Project Structure > SDKs: add 1.8 JDK

To build the code and generate gRPC server stubs, run the `compile` step from the Maven projects pane in IntelliJ. Then create a run configuration pointing to the main method in `ClairvoyantServer.java` to easily deploy the server locally.

Or compile and run from terminal:
```
mvn compile
mvn exec:java -Dexec.mainClass=io.clairvoyant.ClairvoyantServer 8080 8081
```

Deployment
----------
To build the JAR, copy it to the Azure instance, and run the server:
```
./deploy.sh
ssh -i path_to_key azureuser@40.114.122.121
chmod +x run-jar.sh
./run-jar.sh
```

The instance also has a MySQL server running with the following DB:
```
database: clairvoyant
user: root
password: "" (empty)
port: 3306
```

Create a test user (required for authenticating requests):
```
curl --data "firstName=Test&lastName=User&email=test@test.com&password=pass" http://40.114.122.121:8081/createUser
```

=======
DB with test data Setup
-----------------------
- Create a db with the name `clairvoyant`

- Navigate to `clairvoyant/backend/src/scripts/`

- Run the `create_test_db.sh` script to create the db with test data:
```
sh create_test_db.sh
```
