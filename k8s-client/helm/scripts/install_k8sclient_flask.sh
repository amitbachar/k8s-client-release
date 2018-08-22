kubectl delete service k8s-client-python-service
kubectl delete deployment k8s-client-python-deployment

#helm install ../charts/k8s-client-python --set namespace=default,image.tag=latest,deployment.replicaCount=1
#helm install ../charts/k8s-client-python-v22.0.tgz --set image.tag=latest,deployment.replicaCount=1
#helm install ../charts/k8s-client-python --namespace default --set image.tag=latest,deployment.replicaCount=1,service.nodeport=30011
#helm install ../charts/k8s-client-python --namespace development --set image.tag=latest,deployment.replicaCount=1,service.nodeport=30022
#helm install ../charts/k8s-client-python --namespace production --set image.tag=latest,deployment.replicaCount=1,service.nodeport=30033
helm upgrade -i k8s-client-python ../charts/k8s-client-python --namespace default --set image.tag=latest,deployment.replicaCount=1,service.nodeport=30222
#helm upgrade -i k8s-client-python ../charts/k8s-client-python --namespace development --set image.tag=latest,deployment.replicaCount=2,service.nodeport=30022
#helm upgrade -i k8s-client-python ../charts/k8s-client-python --namespace production --set image.tag=latest,deployment.replicaCount=2,service.nodeport=30022
#helm upgrade -i k8s-client-python ../charts/k8s-client-python --namespace default --set image.tag=alpine,deployment.replicaCount=1,service.nodeport=30011
