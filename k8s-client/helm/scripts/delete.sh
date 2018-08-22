version=$1
helm delete k8s-client-python-$version
#kubectl delete service k8s-client-python-service-$version ; kubectl delete deployment k8s-client-python-deployment-$version
