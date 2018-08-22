#!/usr/bin/python

from kubernetes import client, config, watch
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


time = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')

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

config.load_kube_config()
api_instance = client.CoreV1Api()

app = Flask(__name__)
    
@app.route("/")
def usage():
    return redirect(url_for('getPodsInfo'))

@app.route('/getPodsInfo')
def getPodsInfo():
    namespace = request.args.get('namespace', 'default' , type=str)
    api_response = api_instance.list_namespaced_pod(namespace)
    title = ['pod name','pod namespace','pod ip','pod host ip','pod image','pod container name','pod status']
    podsdata = []
    podsdata.append(title)
    for i in api_response.items:
        pod_name = i.metadata.name
        pod_ip = i.status.pod_ip
        pod_namespace = i.metadata.namespace
        pod_host_ip = i.status.host_ip
        for current_pod in i.spec.containers:
            pod_image = current_pod.image
            pod_container_name=current_pod.name
        pod_status = i.status.phase
        idata = [pod_name,pod_namespace,pod_ip,pod_host_ip,pod_image,pod_container_name,pod_status]
	podsdata.append(idata)
    sorted_podsdata = sorted(podsdata, key=itemgetter(0))  
    return render_template("p_data.html", pods_data=podsdata)
    #return jsonify(api_response)

@app.route('/getNodsInfo')
def getNodsInfo():
    pretty = 'true'
    api_response = api_instance.list_node(pretty=pretty)
    nodes = []
    for i in api_response.items:
        node_name = i.metadata.name
        nodes.append(node_name)
    #return ''.join(nodes)
    return render_template("nodes.html", nodes=nodes)
    #return jsonify(api_response)


@app.route('/list_namespace')
def list_namespace():
    pretty = 'true'
    api_response = api_instance.list_namespace(pretty=pretty)
    namespace_list = []
    for i in api_response.items:
       inamespace = i.metadata.name
       namespace_list.append(inamespace)
    return render_template("namespace_list.html", namespace_list=namespace_list)
    #return ''.join(namespace_list)
    #return jsonify(api_response)


if __name__ == '__main__':
#    main()
    app.debug = True
    app.run(host = '0.0.0.0',port=5555)
