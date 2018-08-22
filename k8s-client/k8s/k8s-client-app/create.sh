#!/bin/sh
if [ $# -lt 1 ]
then
 echo "usage::"
 echo "$(basename $0) <version>"
 echo "example $(basename $0) v2"
 exit 0
fi

version="$1"

kubectl apply -f html-pv-PersistentVolume.yml
kubectl apply -f html-claim-PersistentVolumeClaim.yml
kubectl apply -f k8s-client-dashboard-app-${version}.yml

#kubectl create --save-config -f html-pv-PersistentVolume.yml
#kubectl create --save-config -f html-claim-PersistentVolumeClaim.yml
#kubectl create --save-config -f k8s-client-dashboard-app-${version}.yml
