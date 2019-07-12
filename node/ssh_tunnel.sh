#!/bin/bash
createTunnel() {
 current_time=$(date "+%Y.%m.%d-%H.%M.%S")
 echo '[' $current_time '] Attempting to establish new tunnel connection with AWS'
  /usr/bin/ssh -f -N -R 2222:localhost:22 ec2-jump -o ExitOnForwardFailure=True
  if [[ $? -eq 0 ]]; then
    echo  '[' $current_time '] Tunnel created successfully'
  else
    echo '[' $current_time '] An error occurred while attempting to make connection.'
  fi
}

sshpid=$(/bin/pidof ssh)
if [[ -z $sshpid ]]; then
  createTunnel
fi
