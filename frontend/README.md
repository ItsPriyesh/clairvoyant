# Deploy

Secure copy the files in this directory to the Azure user directory, then SSH into the instance and move them with sudo into the NGINX served folder:
```
scp -i path_to_key * azureuser@40.114.122.121:/home/azureuser/fe/
ssh -i path_to_key azureuser@40.114.122.121
sudo mv fe/* /var/www/html/
```

