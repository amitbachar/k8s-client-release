#!/usr/bin/python

from kubernetes import client, config, watch
#from prettytable import PrettyTable
#from prettytable import MSWORD_FRIENDLY
from prettytable import *
import datetime
import os
import sys
import getopt
import argparse
from flask import Flask, render_template , redirect , url_for , request
import jinja2


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


app = Flask(__name__)
    
@app.route("/")
def usage():
    #usage_txt = "usage --> " + "\n" + "http://hostname:30002/getPodsInfo?namespace=default" +  "\n" + " -->  Example :: http://10.238.196.115:30002/getPodsInfo?namespace=default" 
    #return usage_txt
    return redirect(url_for('getPodsInfo'))

#@app.route("/Pdata/<string:namespace>/")
#def getPdata(namespace):
@app.route('/getPodsInfo')
def getPodsInfo():
    namespace = request.args.get('namespace', 'default' , type=str)
    # Configs can be set in Configuration class directly or using helper utility
    config.load_kube_config()
    v1 = client.CoreV1Api()
    #print "Listing pods information @(",time,"):"
    #ret = v1.list_pod_for_all_namespaces(watch=False)
    ret = v1.list_namespaced_pod(namespace)
    #ret = v1.list_node()
    #print ret
    title = ['pod name','pod ip','pod namespace','pod image','pod container name','pod status']
    x = len(title)
    #print "title count: %d" % (x,)
    y = len(ret.items)
    #print "pod count: %d" % (y,)
    podsdata = []
    poddatatable = PrettyTable()
    poddatatable.field_names = title
    poddatatable.align = "l"
    poddatatable.sortby = "pod name"
    #poddatatable.set_style(DEFAULT)
    #poddatatable.align['pod name'] = "l"
    #poddatatable.align['pod ip'] = "l"
    #poddatatable.align['pod namespace'] = "l"
    #poddatatable.align['pod image'] = "l"
    #poddatatable.align['pod container name'] = "l"
    #poddatatable.align['pod status'] = "l"


    p_data={}
    i_data={}
    podsdata.append(title)
    for i in ret.items:
        pod_name = i.metadata.name
        pod_ip = i.status.pod_ip
        pod_namespace = i.metadata.namespace
        for current_pod in i.spec.containers:
            pod_image = current_pod.image
            pod_container_name=current_pod.name
        pod_status = i.status.phase
        idata = [pod_name,pod_ip,pod_namespace,pod_image,pod_container_name,pod_status]
        i_data[pod_name]=[pod_ip,pod_namespace,pod_image,pod_container_name,pod_status]
	podsdata.append(idata)
        #p_data.append(i_data[pod_name])
        poddatatable.add_row(idata)
    #return render_template("p_data.html", titles=title)
    return render_template("p_data.html", pods_data=podsdata)
    #return render_template("p_data.html", titles=title)
    current_path = os.path.dirname(os.path.abspath(__file__))
    try:
        os.makedirs(current_path+"/output")
    except OSError:
        if not os.path.isdir(current_path+"/output"):
            raise
    output_path=current_path+"/output"
    file_name = "poddata"
    outputfilename = os.path.join(output_path, file_name+".txt")
    poddatatable_text = poddatatable.get_string()
    #return poddatatable_text
    if os.path.isfile(outputfilename):
            os.remove(outputfilename)
    print color.BOLD + "Listing",namespace,"namespace pods information @(",time,"):" + color.END


    with open(outputfilename, 'w') as file:
        file.write("\nListing ")
        file.write(namespace)
        file.write(" namespace pods information @ ")
        file.write(time)
        file.write("\n\n")
        file.write(poddatatable_text)
        file.close()

    poddatatable.format = True
    poddatatable_html = poddatatable.get_html_string()
    #return poddatatable_html 
    outputfilename = os.path.join(output_path, file_name+".html")
    if os.path.isfile(outputfilename):
            os.remove(outputfilename)
    with open(outputfilename,'w') as file:
        file.write("\nListing ")
        file.write(namespace)
        file.write(" namespace pods information @ ")
        file.write(time)
        file.write("\n\n")
        file.write(poddatatable_html)
        file.close()

if __name__ == '__main__':
#    main()
    app.debug = True
    app.run(host = '0.0.0.0',port=5005)
