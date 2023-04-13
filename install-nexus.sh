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

# sort out persistent volume
NODE_NAME=$(kubectl get nodes |grep control-plan|cut -d\  -f1)
envsubst < nexus.persistence.yml.template > nexus.persistence.yml
kubectl apply -f nexus.persistence.yml

# create deployment
kubectl apply -f nexus.deploy.yml

# check status
kubectl get all -n nexus
