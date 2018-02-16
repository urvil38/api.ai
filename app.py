from kubernetes import client, config
from kubernetes.client.rest import ApiException
from flask import Flask
from flask import request,make_response
import json
import math

app=Flask(__name__)

config.load_kube_config()

v1 = client.CoreV1Api()
k8_client = client.AppsV1beta1Api()

namespace = "default"
node_name = []


@app.route("/webhook",methods=["POST"])
def webhook():
    req = request.get_json(silent=True,force=True)
    action = req.get('result').get('action')
    parameters = req.get('result').get('parameters')
    list_nodes = v1.list_node()
    for node in list_nodes.items:
            node_name.append(node.metadata.name)

    if action == "list_pod":
        return format_response(list_all_pods())
    if action == "cluster_status":
        return format_response(cluster_status())
    if action == "create_deployment":
        return format_response(create_deployment(parameters))
    if action == "scale_deployment":
        return format_response(scale_deployment(parameters))
    if action == "update_deployment":
        return format_response(update_deployment(parameters))

def format_response(res):
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers["Content-Type"] = "application/json"
    return r

def list_all_pods():
    pods = v1.list_namespaced_pod(namespace=namespace)
    speech = "there are {} pods are running in {} namespace in your cluster".format(len(pods.items),namespace)
    return {
        "speech": speech,
        "displayText": speech
    }

def cluster_status():
    node_info = v1.read_node_status(node_name[0],pretty=True)
    cpu_info = node_info.status.capacity['cpu']
    ram = node_info.status.capacity['memory']
    ram_floor = math.floor(int(ram[:-2])/1024/1000)
    if ram_floor >= 3 and ram_floor < 4:
        ram_info = 4
    else:
        ram_info = ram_floor

    speech = "The {} cluster is running with {} CPUs and {} gigs of ram.".format(node_name[0],cpu_info,ram_info)

    return {
        "speech": speech,
        "displayText": speech
    }

def create_deployment(parameters):
    image_name = parameters['image_name']
    deployment_name = image_name
    if '_' in image_name:
        deployment_name = image_name.replace('_','')
    image_tag = parameters['image_tag']
    body = client.AppsV1beta1Deployment()
    body.metadata = {
        "name": deployment_name,
        "labels": {
            "app": deployment_name
        }
    }

    body.spec = {
        "template": {
            "metadata": {
                "labels": {
                    "app": deployment_name
                }
            },
            "spec": {
                "containers": [
                    {
                        "name": deployment_name,
                        "image": "urvil38/{}:{}".format(image_name,image_tag)
                    }
                ]
            }
        }
    }

    speech = ""
    try:
        response = k8_client.create_namespaced_deployment(namespace, body)
        speech = "Deploying {} {} into the {} cluster.".format(image_name, image_tag, node_name[0])
    except ApiException as e:
        print("Exception when calling AppsV1beta1Api->create_namespaced_deployment: %s\n" % e)
        speech = "There was an error while creating the {} deployment".format(image_name)

    return {
        "speech": speech,
        "displayText": speech
    }

def scale_deployment(parameters):
    deployment_name = parameters['deployment_name']
    replica_count = int(parameters['replica_count'])

    body = client.AppsV1beta1Deployment()
    body.spec = {
        "replicas": replica_count
    }

    speech = ""

    try:
        response = k8_client.patch_namespaced_deployment(deployment_name,namespace,body)
        speech = "Scaling the {} deployment to {}".format(deployment_name, replica_count)
    except ApiException as e:
        print("Exception when calling AppsV1beta1Api->patch_namespaced_deployment: %s\n" % e)
        speech = "There was an error when scaling {} deployment".format(deployment_name)

    return {
        "speech": speech,
        "displayText": speech
    }

def update_deployment(parameters):
    new_tag_name = parameters['image_tag']
    image_name = parameters['deployment_name']
    deployment_name = image_name
    if '_' in image_name:
        deployment_name = image_name.replace('_','')
    body = client.AppsV1beta1Deployment()
    body.spec = {
        "template":{
            "spec": {
                "containers":[
                    {
                        "name":deployment_name,
                        "image":"urvil38/{}:{}".format(image_name,new_tag_name)
                    }
                ]
            }
        }
    }
    speech = ""

    try:
        response = k8_client.patch_namespaced_deployment(deployment_name,namespace,body)
        speech = "Updating {} deployment to new version {}".format(deployment_name,new_tag_name)
    except ApiException as e:
        print("Exception when calling AppsV1beta1Api->patch_namespaced_deployment: %s\n" % e)
        speech = "There was an error when updating {} deployment".format(deployment_name)

    return {
        "speech":speech,
        "displayText":speech
    }

if __name__ == "__main__":
    app.run(host="localhost",port=3000)
