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

![Architecture](https://drive.google.com/open?id=1YLsQRnvSaOPi-KNosoQRRFxCjfLfTe6P)

