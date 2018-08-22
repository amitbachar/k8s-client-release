#!/usr/bin/python

from kubernetes import client, config, watch
from kubernetes.client.rest import ApiException
from kubernetes.stream import stream
from kubernetes.client.apis import core_v1_api
from kubernetes.client.rest import ApiException
from prettytable import *
import datetime
import os
import sys
import getopt
import argparse
from flask import Flask, render_template , redirect , url_for , request , jsonify
import jinja2
import json
from operator import itemgetter
from flasgger import Swagger
from flasgger.utils import swag_from
import logging
import re

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def get_numbers_from_filename(filename):
    return re.search(r'\d+', filename).group(0)

config.load_kube_config()
api_instance = client.CoreV1Api()
api = core_v1_api.CoreV1Api()

app = Flask(__name__)
Swagger(app)

# Functions
def validate_ns(ns):
    pretty = 'true'
    namespace_lst = []
    for i in api_instance.list_namespace(pretty=pretty).items:
       inamespace = i.metadata.name
       namespace_lst.append(inamespace)
    if ns not in namespace_lst :
      return "invalid namespace " + ns + ", valid namespace are: " + " , ".join(namespace_lst) , 500
    
@app.route("/")
def usage():
    return redirect(url_for('flasgger.apidocs'))
    #return "to view api documentation append to the url /apidocs"

@app.route('/ms_dashbord/<string:namespace>')
@swag_from('Swagger/ms_dashbord_Swagger.yml')
def ms_dashbord(namespace):
    time = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    pretty = 'true'
    namespace_lst = []
    for i in api_instance.list_namespace(pretty=pretty).items:
       inamespace = i.metadata.name
       #idata = [inamespace]
       namespace_lst.append(inamespace)

    if namespace not in namespace_lst :
      return "invalid namespace " + namespace + ", valid namespace are: " + " , ".join(namespace_lst) , 500
    else:
      title = ['MS Name','Current Version in Env','Docker Image Name','MS^Next Runtime','msb-async-messaging Ver','msb-couchbase Ver','msb-repository Ver','msb-resource Ver','msb-swagger Ver']
      msddata_array = []
      msddata_dict = {}
      for i in api_instance.list_namespaced_pod(namespace).items:
        logging.info("[START]*************validating container is running ****************")
        pod_name = i.metadata.name
        pod_phase = api.read_namespaced_pod(pod_name, namespace).status.phase
        #logging.info("pod_name:{:<60}  | pod_phase:{:<80} ".format(pod_name,pod_phase))
        containerStatuses = api.read_namespaced_pod(pod_name, namespace).status.container_statuses
        #logging.info(containerStatuses)
        for jtem in containerStatuses:
          container_ready=jtem.ready
        logging.info("pod_name:{:<40}  | pod_phase:{:<40} | container_ready:{:<40}".format(pod_name,pod_phase,container_ready))
        #logging.info(i) 
        #if pod_phase not in [ 'Succeeded','Failed','Pending']:
        logging.info("[END]*************validating container is running ****************")
        if container_ready :
            pod_labels = i.metadata.labels
            #return jsonify(pod_labels) , 200
            if 'microservice' in pod_labels.keys():
              #pod_name = i.metadata.name
              ms_name = i.metadata.labels['microservice']
              for current_pod in i.spec.containers:
                pod_image = current_pod.image
                docker_image_name= pod_image.split("/")[1].split(":")[0]
                ms_ver_in_env = pod_image.split("/")[1].split(":")[1]
              #logging.info("pod_name:{:<60}  | pod_labels:{:<80}".format(pod_name,ms_name,pod_image))
              #MSNEXT_VERSION = api_instance.connect_get_namespaced_pod_exec(pod_name, namespace, command="ls -l /opt/amdocs/msnext |grep -v 'No such file'|awk '{print $NF}'")
              logging.info("[START]*************retrieving MSNEXT_VERSION****************")
              try:
                #exec_command = ['/bin/sh','-c',"ls -l /opt/amdocs/msnext |grep -v 'No such file'|awk '{print $NF}'"]
                exec_command = ['/bin/sh','-c',"readlink /opt/amdocs/msnext"]
                #exec_command =  ['/bin/sh','-c','pwd']
                #MSNEXT_VERSION = api_instance.connect_get_namespaced_pod_exec(pod_name,namespace,command=exec_command,stderr=True, stdin=False,stdout=True, tty=False)
                logging.info("Pod name:  {}".format(pod_name))
                MSNEXT_VERSION = stream(api.connect_get_namespaced_pod_exec,pod_name,namespace,command=exec_command)
                #pod_phase = api.read_namespaced_pod(pod_name, namespace).status.phase
                #logging.info("Pod phase {} without returning test results".format(pod_phase))
                if "non-zero exit code" not in MSNEXT_VERSION:
                  logging.info("MSNEXT_VERSION: {}".format(MSNEXT_VERSION))
              except ApiException as e:
                pod_phase = api.read_namespaced_pod(pod_name, namespace).status.phase
                if pod_phase == 'Succeeded' or pod_phase == 'Failed' or pod_phase == 'Pending':
                  logging.info("Pod phase {} without returning test results".format(pod_phase))
                  return None
              except Exception as e:
                logging.info("execption: %s" % e)
                return None
              logging.info("[END]*************retrieving MSNEXT_VERSION****************")
              logging.info("[START]*************retrieving MSB_VERSIONS****************")
              try:
                #exec_command = ['/bin/sh','-c',"[ -f /opt/amdocs/msnext/deploy/ ] && exe_jar=`find /opt/amdocs/msnext/deploy/ -name '*-exe-*.jar' |grep -v 'No such file' |tr -d '\r'` || echo 'NA NA NA NA NA'; jar tf ${exe_jar} >> /dev/null 2>&1 ; if [ $? -ne 0 ]; then echo 'NA NA NA NA NA'; else jar tf ${exe_jar} |grep msb |grep spring-boot-starter|tr -d '\r'|awk -F'/' '{print $NF}' | sort; fi "]
                exec_command = [
                      '/bin/sh',
                      '-c',
                      '''if [ -d /opt/amdocs/msnext/deploy/ ]  
			 then
				exe_jar=`find /opt/amdocs/msnext/deploy/ -name '*-exe-*.jar' |grep -v 'No such file' |tr -d '\r'`;
			 else
				echo 'NA NA NA NA NA';
			 fi
                       if [ ! -z "${exe_jar}" ] 
                       then
                       	jar tf ${exe_jar} >> /dev/null 2>&1 ; 
                       	if [ $? -ne 0 ]; 
                          then echo 'NA NA NA NA NA'; 
                       	else 
                          jar tf ${exe_jar} |grep msb |grep spring-boot-starter|tr -d '\r'|awk -F'/' '{print $NF}' | sort;
			fi
                       fi ''']
                
                #MSNEXT_VERSION = api_instance.connect_get_namespaced_pod_exec(pod_name,namespace,command=exec_command,stderr=True, stdin=False,stdout=True, tty=False)
                logging.info("Pod name:  {}".format(pod_name))
                MSB_VERSIONS = stream(api.connect_get_namespaced_pod_exec,pod_name,namespace,command=exec_command)
                #pod_phase = api.read_namespaced_pod(pod_name, namespace).status.phase
                #logging.info("Pod phase {} without returning test results".format(pod_phase))
                if "non-zero exit code" not in MSB_VERSIONS:
                  logging.info("MSB_VERSIONS: {}".format(MSB_VERSIONS))
                #MSB_VERSIONS_array = MSB_VERSIONS.split().split("-spring-boot-starter-")
                MSB_VERSIONS_array = MSB_VERSIONS.split()
                logging.info("MSB_VERSIONS_array: {}".format(MSB_VERSIONS_array))
                #MSB_VERSIONS_array_len = len(MSB_VERSIONS_array)
                #logging.info(MSB_VERSIONS_array_len)
                
                for i in range(len(MSB_VERSIONS_array)):
                  #MSB_VERSIONS_array[i]=MSB_VERSIONS_array[i].split('-spring-boot-starter-')
                  file_name=MSB_VERSIONS_array[i]
                  logging.info("file_name {} ".format(file_name))
                  regex = re.compile(r'\d+')
                  MSB_VERSIONS_array[i]=regex.findall(file_name)
                  MSB_VERSIONS_array[i]=".".join(MSB_VERSIONS_array[i])
                  #MSB_VERSIONS_array[i]=get_numbers_from_filename(file_name)
              except ApiException as e:
                pod_phase = api.read_namespaced_pod(pod_name, namespace).status.phase
                if pod_phase == 'Succeeded' or pod_phase == 'Failed' or pod_phase == 'Pending':
                  logging.info("Pod phase {} without returning test results".format(pod_phase))
                  return None
              except Exception as e:
                logging.info("execption: %s" % e)
                return None
              logging.info("[END]*************retrieving MSB_VERSIONS****************")
              #logging.info(MSNEXT_VERSION)
              idata = [ms_name,ms_ver_in_env,docker_image_name,MSNEXT_VERSION] + MSB_VERSIONS_array
              #idata = [ms_name,ms_ver_in_env,docker_image_name]
              msddata_array.append(idata)

      sorted_msddata_array = sorted(msddata_array, key=itemgetter(0))
      #logging.info(sorted_msddata_array) 
      #return 'true'
      return render_template("ms_dashbord.html", title=title, sorted_msddata_array=sorted_msddata_array , time=time)

@app.route('/list_namespaced_pod/<string:namespace>')
@swag_from('Swagger/list_namespaced_pod_Swagger.yml')
def list_namespaced_pod(namespace):
    #namespace = request.args.get('namespace', 'default' , type=str)
    #"""
    #Use this api By passing namespace to get pods information
    #---
    #tags:
    #  - list_namespaced_pod API
    #parameters:
    #  - name: namespace
    #    in: path
    #    type: string
    #    required: true
    #    description: The namespace name you want its pods info
    #responses:
    #  500:
    #    description: Error The namespace is not valid!
    #  200:
    #    description: namespace is valid!
    #"""

    #try:
    #    validate(data, 'namespace_name', 'Swagger/list_namespaced_pod_Swagger.yml', root=__file__)
    #except ValidationError as e:
    #    return "Validation Error: %s" % e, 400
    time = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    pretty = 'true'
    namespace_lst = []
    for i in api_instance.list_namespace(pretty=pretty).items:
       inamespace = i.metadata.name
       #idata = [inamespace]
       namespace_lst.append(inamespace)

    if namespace not in namespace_lst :
      return "invalid namespace " + namespace + ", valid namespace are: " + " , ".join(namespace_lst) , 500
      #valid_namespaces = jsonify(namespace_lst)
      #return valid_namespaces
    #if validate_ns(namespace)
    else:
      api_response = api_instance.list_namespaced_pod(namespace)
      title = ['pod name','pod namespace','pod ip','pod host ip','pod image','pod container name','pod startTime', 'pod status']
      #title = ['pod name','pod namespace','pod ip','pod host ip','pod image','pod container name','pod status']
      podsdata = []
      dict_poddata = {}
      #podsdata.append(title)
      for i in api_instance.list_namespaced_pod(namespace).items:
          pod_name = i.metadata.name
          pod_ip = i.status.pod_ip
          pod_namespace = i.metadata.namespace
          pod_host_ip = i.status.host_ip
          for current_pod in i.spec.containers:
              #print ("debug:",pod_name,current_pod.image,current_pod.name, file=sys.stdout)
              #logging.error("name:{:<60}  | image:{:<80} |contaner name:{:<50}".format(pod_name,current_pod.image,current_pod.name))
              pod_image = current_pod.image
              pod_container_name=current_pod.name
          pod_start_time = i.status.start_time
          pod_status = i.status.phase
          idata = [pod_name,pod_namespace,pod_ip,pod_host_ip,pod_image,pod_container_name,pod_start_time,pod_status]
          #logging.info("name:{:<60}  | namespace:{:<80} |pod ip:{:<50}".format(pod_name,pod_namespace,pod_host_ip))
          #idata = [pod_name,pod_namespace,pod_ip,pod_host_ip,pod_image,pod_container_name,pod_status]
          podsdata.append(idata)
      sorted_podsdata = sorted(podsdata, key=itemgetter(0))
      #logging.info(sorted_podsdata)
      #logging.info(api_instance.list_namespaced_pod(namespace)) 
      return render_template("list_namespaced_pod.html", title=title, pods_data=sorted_podsdata , time=time)
      #return jsonify(api_response) , 200


@app.route('/get_pod_info/<string:namespace>')
def get_pod_info(namespace):
    """
    Use this api By passing namespace and pod_name to get pod information
    ---
    tags:
      - get_pod_info API
    parameters:
      - name: namespace
        in: path
        type: string
        required: true
        description: The namespace name you want its pods info
      - name: pod_name
        in: query
        type: string
        description: pod name to get info for
    responses:
      500:
        description: Error The namespace is not valid!
      200:
        description: namespace is valid!
    """
    pod_name = request.args.get('pod_name', '' , type=str)
    pretty = 'true'
    namespace_lst = []
    for i in api_instance.list_namespace(pretty=pretty).items:
       inamespace = i.metadata.name
       #idata = [inamespace]
       namespace_lst.append(inamespace)
    #namespace_list = api_instance.list_namespace(pretty=pretty).items.metadata.name
    if namespace not in namespace_lst :
      return "invalid namespace " + namespace + ", valid namespace are: " + " , ".join(namespace_lst) , 500
      #valid_namespaces = jsonify(namespace_lst)
      #return valid_namespaces
    else:
      api_response = api_instance.list_namespaced_pod(namespace)
      dict_poddata = {}
      #podsdata.append(title)
      for i in api_instance.list_namespaced_pod(namespace).items:
        if pod_name == i.metadata.name:
            pod_name = i.metadata.name
            pod_ip = i.status.pod_ip
            pod_namespace = i.metadata.namespace
            pod_host_ip = i.status.host_ip
            for current_pod in i.spec.containers:
              #print ("debug:",pod_name,current_pod.image,current_pod.name, file=sys.stdout)
              #logging.error("name:{:<60}  | image:{:<80} |contaner name:{:<50}".format(pod_name,current_pod.image,current_pod.name))
              pod_image = current_pod.image
              pod_container_name=current_pod.name
            pod_start_time = i.status.start_time
            pod_status = i.status.phase
            dict_poddata = {'pod_name': pod_name ,'pod_namespace': pod_namespace ,'pod_ip': pod_ip ,'pod_host_ip': pod_host_ip,'pod_image': pod_image,'pod_container_name': pod_container_name,'pod_start_time' : pod_start_time,'pod_status': pod_status}
            #idata = [pod_name,pod_namespace,pod_ip,pod_host_ip,pod_image,pod_container_name,pod_start_time,pod_status]
            #logging.info("dict_poddata:{:<100}".format(dict_poddata))
            #idata = [pod_name,pod_namespace,pod_ip,pod_host_ip,pod_image,pod_container_name,pod_status]
            #podsdata.append(idata)
      #sorted_podsdata = sorted(podsdata, key=itemgetter(0))
      logging.info("pod_ip:{:<20}".format(dict_poddata['pod_ip'])) 
      #return render_template("list_namespaced_pod.html", title=title, pods_data=sorted_podsdata , time=time)
      #return dict_poddata['pod_ip'] , 200
      return jsonify(dict_poddata) , 200

@app.route('/list_node')
def list_node():
    """
    Use this api to get back k8s cluster list of nodes.
    ---
    tags:
      - list_node API
    responses:
      500:
        description: Error
      200:
        description: k8s node list will recieved.

    """
    pretty = 'true'
    title = ['k8s clsuter nodes']
    api_response = api_instance.list_node(pretty=pretty)
    nodes = []
    for i in api_instance.list_node(pretty=pretty).items:
        node_name = i.metadata.name
        nodes.append(node_name)
    #return ''.join(nodes)
    return render_template("list_node.html", title=title , nodes=nodes)
    #return jsonify(api_response)


@app.route('/list_namespace')
def list_namespace():
    """
    Use this api to get back list of valid namespaces
    This is the list_namespace k8s client API
    ---
    tags:
      - list_namespace API
    responses:
      500:
        description: Error
      200:
        description: namespace list will recieved.

    """
    pretty = 'true'
    api_response = api_instance.list_namespace(pretty=pretty)
    title = ['namespace','status']
    namespace_list = []
    for i in api_instance.list_namespace(pretty=pretty).items:
       inamespace = i.metadata.name
       istatus = i.status.phase
       idata = [inamespace , istatus ]
       namespace_list.append(idata)
    return render_template("list_namespace.html", title=title, namespace_list=namespace_list)
    #return ''.join(namespace_list)
    #return jsonify(api_response)

@app.route('/list_namespaced_deployment/<string:namespace>')
def list_namespaced_deployment(namespace):
    #namespace = request.args.get('namespace', 'default' , type=str)
    """
    Use this api By passing namespace to get k8s deployments information
    ---
    tags:
      - list_namespaced_deployment API
    parameters:
      - name: namespace
        in: path
        type: string
        required: true
        description: The namespace name you want its deployments info
    responses:
      500:
        description: Error The namespace is not valid!
      200:
        description: namespace is valid!
    """

    #try:
    #    validate(data, 'namespace_name', 'Swagger/list_namespaced_pod_Swagger.yml', root=__file__)
    #except ValidationError as e:
    #    return "Validation Error: %s" % e, 400
    time = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    pretty = 'true'
    namespace_lst = []
    for i in api_instance.list_namespace(pretty=pretty).items:
       inamespace = i.metadata.name
       #idata = [inamespace]
       namespace_lst.append(inamespace)
    #namespace_list = api_instance.list_namespace(pretty=pretty).items.metadata.name
    if namespace not in namespace_lst :
      return "invalid namespace " + namespace + ", valid namespace are: " + " , ".join(namespace_lst) , 500
      #valid_namespaces = jsonify(namespace_lst)
      #return valid_namespaces
    else:
      #return namespace
      logging.info("namespace:{:<20}".format(namespace))
      deploymentsdata = []
      #app_api_instance = kubernetes.client.AppsV1Api()
      app_api_instance = client.AppsV1Api()
      app_api_response = app_api_instance.list_namespaced_deployment(namespace)
      #logging.info("app_api_response:{:<20}".format(app_api_response))
      #title = ['pod name','pod namespace','pod ip','pod host ip','pod image','pod container name','pod startTime', 'pod status']
      #title = ['pod name','pod namespace','pod ip','pod host ip','pod image','pod container name','pod status']
      #podsdata = []
      #podsdata.append(title)
      for i in app_api_instance.list_namespaced_deployment(namespace).items:
          deployment_name = i.metadata.name
          #pod_ip = i.status.pod_ip
          #pod_namespace = i.metadata.namespace
          #pod_host_ip = i.status.host_ip
          #for current_pod in i.spec.containers:
          #    pod_image = current_pod.image
          #    pod_container_name=current_pod.name
          #pod_start_time = i.status.start_time
          #pod_status = i.status.phase
          idata = [deployment_name]
          deploymentsdata.append(deployment_name)
      #sorted_podsdata = sorted(podsdata, key=itemgetter(0))  
      #return render_template("list_namespaced_pod.html", title=title, pods_data=sorted_podsdata , time=time)
      #return jsonify(deploymentsdata) , 200
      return namespace
      #return jsonify(api_response) , 200

if __name__ == '__main__':
#    main()
    logging.basicConfig(format='%(message)s', level=logging.INFO)  
    app.debug = True
    app.run(host = '0.0.0.0',port=5555)
