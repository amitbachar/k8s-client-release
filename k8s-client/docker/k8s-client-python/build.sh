echo -e "\n\t **** buiding k8s-client-python latest image *********** \n\t"
docker build -t k8s-client-python .
echo -e "\n\t **** buiding k8s-client-python latest image *********** \n\t"
docker build -t k8s-client-python:stable .
#docker build -t amitbachar/k8s-client-python .
