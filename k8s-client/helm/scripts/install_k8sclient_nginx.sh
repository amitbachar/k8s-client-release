kubectl delete service ngnix-dash-service
kubectl delete service k8s-client-python-service 
kubectl delete deployment ngnix-dashboard-deployment
kubectl delete deployment k8s-client-python-deployment

#helm install ../charts/k8s-client-python --set namespace=default,image.tag=latest,deployment.replicaCount=1
#helm install ../charts/k8s-client-ngnix --set image.tag=latest,deployment.replicaCount=1
helm upgrade -i k8s-client-python ../charts/k8s-client-python --namespace default --set image.tag=latest,deployment.replicaCount=1,service.nodeport=30011
helm upgrade -i k8s-client-ngnix ../charts/k8s-client-ngnix --namespace default --set image.tag=latest,deployment.replicaCount=1 
