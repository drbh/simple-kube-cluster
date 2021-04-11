# A basic kubernetes example

First, we'll want to deploy a new Kubernetes cluster on our local machine. The most common ways of creating a local cluster are with the tools `kind` and `minikube`.

In this example we'll be using `kind` since it allow for multiple nodes and it has a clean/simple api.

We can use the following command to create a new cluster with a specific name. This cluster has a few special features that can be seen in the config file. For instance we'll use `kubeadmConfigPatches` and `extraPortMappings` to allow ingress traffic
```bash
kind create cluster --config './cluster-config.yaml' --name mycluster
```

Next we'll want to set our `kubectl` context to our kind cluster. This may not be required if the kind setup preselects the context for you.
```bash
kind export kubeconfig --name mycluster
# kubectl config get-contexts
# kubectl config use-context kind-testcluster
```


```bash
kubectl cluster-info --context kind-mycluster
```

```bash
cd python-app

docker build -t tiny-docker-python:latest .
kind load docker-image tiny-docker-python:latest --name mycluster
```


Create a namespace - and populate it with objects.
```bash
kubectl create namespace space
kubectl apply -f application/secret.yaml -n space
kubectl apply -f application/database.yaml -n space
kubectl apply -f application/server.yaml -n space
kubectl apply -f application/ingress.yaml -n space
```

remove all objects
```bash
kubectl delete -f application/ingress.yaml -n space
kubectl delete -f application/server.yaml -n space
kubectl delete -f application/database.yaml -n space
kubectl delete -f application/secret.yaml -n space
kubectl delete namespace space

```


```bash
kubectl get all -n space
# watch -n 5 kubectl get all -n space

# NAME                                       READY   STATUS    RESTARTS   AGE
# pod/flask-app-8494744687-7p8t6             1/1     Running   0          5m42s
# pod/postgres-deployment-6464f5b7d6-wfvdn   1/1     Running   0          5m42s

# NAME                       TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)    AGE
# service/flask-service      ClusterIP   10.96.228.65   <none>        8081/TCP   5m42s
# service/postgres-service   ClusterIP   10.96.17.150   <none>        5432/TCP   5m42s

# NAME                                  READY   UP-TO-DATE   AVAILABLE   AGE
# deployment.apps/flask-app             1/1     1            1           5m42s
# deployment.apps/postgres-deployment   1/1     1            1           5m42s

# NAME                                             DESIRED   CURRENT   READY   AGE
# replicaset.apps/flask-app-8494744687             1         1         1       5m42s
# replicaset.apps/postgres-deployment-6464f5b7d6   1         1         1       5m42s
```

Allowing incoming traffic
```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/static/provider/kind/deploy.yaml

kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=90s
```

tail logs
```bash
kubectl logs -f pod/flask-app-8494744687-bk498 -n space
```

```bash
# kubectl delete deployment flask-app -n space
# docker exec -ti mycluster-control-plane crictl images
```# simple-kube-cluster
