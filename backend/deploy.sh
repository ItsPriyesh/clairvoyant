JAR=backend-1.0-SNAPSHOT-jar-with-dependencies.jar
INSTANCE=ppatel@168.62.177.105

mvn clean compile assembly:single

if [ -f "target/$JAR" ]; then
    scp target/$JAR run-jar.sh $INSTANCE:/home/ppatel/
    echo "Copied JAR with executable script to server"
else
    echo "Build failed, JAR doesn't exist."
fi

