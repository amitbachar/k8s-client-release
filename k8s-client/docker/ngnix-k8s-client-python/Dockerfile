FROM nginx:stable
MAINTAINER amitbac
 
# Creating Application Source Code Directory
RUN mkdir -p /ngnix-k8s-client-python

# Setting Home Directory for containers
WORKDIR /ngnix-k8s-client-python

# copying source to container 
COPY . /ngnix-k8s-client-python
RUN mv /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf.orig 
RUN cp /ngnix-k8s-client-python/src/default.conf /etc/nginx/conf.d/
RUN chmod +x /ngnix-k8s-client-python/src/entry.sh

# Application Environment variables
ENV APP_NAME ngnix-k8s-client-python

# Exposing Ports
#EXPOSE 8080 

# Setting Persistent data
#VOLUME ["/app-data"]

#ENTRYPOINT ["./src/entry.sh"]

# Running Python Application
#CMD ["python", "./app/Kubernetes_Python_Client.py"]
