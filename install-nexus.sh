# Make sure cluster exists if Mac
kind  get clusters 2>&1 | grep "kind-nexus"
if [ $? -gt 0 ]
then
    envsubst < kind-config.yaml.template > kind-config.yaml
    kind create cluster --config kind-config.yaml --name kind-nexus
fi

# Make sure create cluster succeeded
kind  get clusters 2>&1 | grep "kind-nexus"
if [ $? -gt 0 ]
then
    echo "Creation of cluster failed. Aborting."
    exit 666
fi

# add metrics
kubectl apply -f https://dev.ellisbs.co.uk/files/components.yaml

# install local storage
kubectl apply -f  local-storage-class.yml

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
export NODE_NAME=$(kubectl get nodes |grep control-plan|cut -d\  -f1)
if [ $KIND -eq 1 ]
then
  envsubst < nexus.deploy.pv.kind.yml.template > nexus.deploy.pv.kind.yml
  kubectl apply -f nexus.deploy.pv.kind.yml
else
  envsubst < nexus.deploy.pv.linux.yml.template > nexus.deploy.pv.linux.yml
  kubectl apply -f nexus.deploy.pv.linux.yml
fi

# create common deployment
kubectl apply -f nexus.deploy.common.yml

# check status
kubectl get all -n nexus
