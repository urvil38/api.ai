# Kubernetes-dialogflow

In this project I demonstred how you could integret google assitance app using dialogflow to talk to the kubernetes api server.

For example:
```
    You : Talk to kubernetes cluster
    K8  : Ok, Talking to kubernetes cluster.

    You : What is my cluster status?
    k8  : Kubernetes cluster is running with 2 cpus and 1 Gis of RAM.

    You : How many pods are running in my cluster?
    k8  : There are 2 pods are running on your cluster.

    You : Create a deployment
    k8  : which docker image you want to use?
    You : matrix
    k8  : which tag you want to use?
    You : 1.0.0
    k8  : Creating matrix deployment in default namespace

    You : Scale a deployment or Scale a matrix deployment
    k8  : how many replicas you wants?
    You : 5
    k8  : Scaling matrix deployment to 5.

    You : Update deployment or Update matrix deployment
    k8  : which tag you want to use?
    You : 2.0.0
    k8  : updating matrix deployment to tag 2.0.0

```

# Architecture

![Architecture](https://github.com/urvil38/api.ai/blob/master/documentation/images/api.003.jpeg)

# Working
- following are the components involved into architecture
1. Kubernetes Cluster ([minikube](https://kubernetes.io/docs/tasks/tools/install-minikube/) or [docker-for-mac](https://docs.docker.com/docker-for-mac/install/))
2. [Flask web server](http://flask.pocoo.org)
3. [ngrok](https://ngrok.com) (secure tunnel between flask server and dialogflow server)
4. [Dialogflow](https://dialogflow.com)
5. Simulator (Google Assistance)

### Request flow from simulator to kubernetes cluster

![requstflow](https://github.com/urvil38/api.ai/blob/master/documentation/images/api.001.jpeg)

Every time user interact with google assitance with speech, For ex.
```
talk to my test application?
```
It invokes a defualt [intent]() in dialogflow. 

Now all following interaction with google assistance is handled by this test application which is a machine learning model(Agent) trained by dialogflow. 

- Following are the two main elements to create model in dialogflow.
    1. Intents
    2. Entity

    You can learn more about those elements [here](https://dialogflow.com/docs/getting-started).

    #### Following are intents from our app
    ![intents](https://github.com/urvil38/api.ai/blob/master/documentation/images/intent.001.png)

    Every Invoked intent send POST request to webhook. This request contains intent name,metadata and also [action]().Now a python server running on your computer get this request through ngrok secure tunnel. Your server invokes particular function depending on action parameter from request and then this function invokes particular action in kubernetes cluser using kubernetes client.

    ```
    action = req.get('result').get('action')

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
    ```

### Response flow from kubernetes cluster to simulator

![responseflow](https://github.com/urvil38/api.ai/blob/master/documentation/images/api.002.jpeg)



