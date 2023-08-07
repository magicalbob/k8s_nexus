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
envsubst < nexus.deploy.pv.linux.yml.template > nexus.deploy.pv.yml
kubectl apply -f nexus.deploy.pv.yml

# create common deployment
kubectl apply -f nexus.deploy.common.yml

until kubectl logs deployment.apps/nexus -n nexus |grep "Started Sonatype Nexus OSS"; do echo waiting for nexus; sleep 5; done

# check status
kubectl get all -n nexus
