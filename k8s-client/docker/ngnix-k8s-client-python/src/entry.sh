#!/bin/sh
echo "running entry.sh"
#export http_proxy=http://genproxy:8080/
#export https_proxy=http://genproxy:8080/
nginx
nginx -s reload

exec $@
