rm -f k8s-client-python/templates/deployment*
cp ../deployments/deployment.yaml_release k8s-client-python/templates/
helm package k8s-client-python
rm -f k8s-client-python/templates/deployment.yaml_release
cp ../deployments/deployment.yaml_dev k8s-client-python/templates/
