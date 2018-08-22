#helm install -n k8s-client-python ../charts/k8s-client-python --set namespace=default,image.tag=latest,deployment.replicaCount=1
#helm install -n k8s-client-python ../charts/k8s-client-python-v22.0.tgz --set image.tag=latest,deployment.replicaCount=1
#helm install -n k8s-client-python ../charts/k8s-client-python --namespace default --set image.tag=latest,deployment.replicaCount=1,service.nodeport=30011
#helm install -n k8s-client-python ../charts/k8s-client-python --namespace development --set image.tag=latest,deployment.replicaCount=1,service.nodeport=30022
#helm install -n k8s-client-python ../charts/k8s-client-python --namespace production --set image.tag=latest,deployment.replicaCount=1,service.nodeport=30033
#helm upgrade -i k8s-client-python ../charts/k8s-client-python --namespace default --set image.tag=latest,deployment.replicaCount=1,service.nodeport=30222
#helm upgrade -i k8s-client-python-v22.0 ../charts/k8s-client-python-v22.0.tgz --set image.tag=latest,deployment.replicaCount=1,service.nodeport=30022
#helm upgrade -i k8s-client-python ../charts/k8s-client-python --namespace development --set image.tag=latest,deployment.replicaCount=2,service.nodeport=30022
#helm upgrade -i k8s-client-python ../charts/k8s-client-python --namespace production --set image.tag=latest,deployment.replicaCount=2,service.nodeport=30022
#helm upgrade -i k8s-client-python ../charts/k8s-client-python --namespace default --set image.tag=alpine,deployment.replicaCount=1,service.nodeport=30011


### DEV
helm upgrade -i k8s-client-python-dev-v22.0.0 ../charts/k8s-client-python --namespace default --set version=dev-22,image.tag=latest,deployment.replicaCount=1,service.nodeport=30022
### RELEASE
helm upgrade -i k8s-client-python-release-v22.0.0 ../charts/k8s-client-python-v22.0.0.tgz --set version=relase-22,image.repository=illin5564.corp.amdocs.com:5000/k8s-client-python,image.tag=stable,deployment.replicaCount=2,service.nodeport=32222
