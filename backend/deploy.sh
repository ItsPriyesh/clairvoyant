JAR=backend-1.0-SNAPSHOT-jar-with-dependencies.jar
INSTANCE=rp1@ec2-3-93-231-152.compute-1.amazonaws.com

mvn clean compile assembly:single

if [ -f "target/$JAR" ]; then
    scp target/$JAR run-ec2.sh $INSTANCE:/home/rp1/
    echo "Copied JAR with executable script to server"
else
    echo "Build failed, JAR doesn't exist."
fi

