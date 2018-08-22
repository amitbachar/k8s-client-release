FROM python:3.6-alpine
MAINTAINER Amit Bachar


# Set env variables used in this Dockerfile (add a unique prefix, such as DOCKYARD)
# Local directory with project source
ENV DOCKYARD_SRC=src
# Directory in container for all project files
ENV DOCKYARD_SRVHOME=/k8s-client-python
# Directory in container for project source files
ENV DOCKYARD_SRVPROJ=/k8s-client-python/src 
# Application Environment variables
ENV APP_NAME k8s-client-python

# Creating Application Source Code Directory
RUN mkdir -p $DOCKYARD_SRVHOME

# copy sources to containers
COPY . $DOCKYARD_SRVHOME
#COPY $DOCKYARD_SRC $DOCKYARD_SRVPROJ

# Setting Home Directory for containers
WORKDIR $DOCKYARD_SRVPROJ

# Installing python dependencies
RUN python --version
RUN pip list 
RUN chmod +x ./script/entry.sh
RUN chmod +x ./app/Kubernetes_Python_Client-falsk.py

# Copying k8s config 
RUN cp -r /k8s-client-python/.kube /root/
#RUN ls /root/.kube

# Setting timezone
RUN ln -sf /usr/share/zoneinfo/Israel /etc/localtime

# Exposing Ports
EXPOSE 5555

# Setting Persistent data
#VOLUME ["/$APP_NAME"]

ENTRYPOINT ["./script/entry.sh"]

# Running Python Application
CMD ["python", "./app/Kubernetes_Python_Client-falsk.py"]
