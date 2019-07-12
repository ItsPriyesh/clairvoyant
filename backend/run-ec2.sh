tmux kill-server
sleep 3
tmux new-session -d -s clairvoyant_session 'java -jar backend-1.0-SNAPSHOT-jar-with-dependencies.jar io.clairvoyant.ClairvoyantServer 8080 8081' C-m

