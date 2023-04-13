# create renovate namespace, if it doesn't exist
kubectl get ns nexus 2> /dev/null
if [ $? -eq 1 ]
then
    kubectl create namespace nexus
fi

# create service
kubectl apply -f nexus.svc.yml

# create vmoptions
kubectl apply -f nexus.vmoptions.yml

# create deployment
cp nexus.deploy.yml.template nexus.deploy.yml
sed -i "s/PWD/$PWD/" nexus.deploy.yml
kubectl apply -f nexus.deploy.yml

# check status
kubectl get all -n nexus
