JAR=backend-1.0-SNAPSHOT-jar-with-dependencies.jar
INSTANCE=azureuser@40.114.122.121

mvn clean compile assembly:single

if [ -f "target/$JAR" ]; then
    scp target/$JAR run-jar.sh $INSTANCE:/home/azureuser/
    echo "Copied JAR with executable script to server"
else
    echo "Build failed, JAR doesn't exist."
fi

