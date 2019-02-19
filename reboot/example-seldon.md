
(after kf is installed)

```bash
multipass launch bionic -n kubeflow -m 8G -d 40G -c 4
multipass exec kubeflow -- sudo snap install microk8s --classic
multipass shell kubeflow
microk8s.enable registry
microk8s.enable dns dashboard # turns o FORAWARD ACCEPT
sudo iptables -P FORWARD ACCEPT
sudo snap alias microk8s.docker docker
sudo snap alias microk8s.kubectl kubectl

git clone https://github.com/canonical-labs/kubernetes-tools
sudo kubernetes-tools/setup-microk8s.sh 
git clone https://github.com/canonical-labs/kubeflow-tools
wget https://github.com/ksonnet/ksonnet/releases/download/v0.13.1/ks_0.13.1_linux_amd64.tar.gz
tar -xzf *gz
rm *gz
sudo cp ks*/ks /usr/local/bin
```

install argo
```bash
sudo curl -sSL -o /usr/local/bin/argo https://github.com/argoproj/argo/releases/download/v2.2.1/argo-linux-amd64
sudo chmod +x /usr/local/bin/argo
kubectl apply -f https://raw.githubusercontent.com/argoproj/argo/v2.2.1/manifests/install.yaml
#kubectl create rolebinding default-admin --clusterrole=admin --serviceaccount=default:default
```

```bash
kubeflow-tools/install-kubeflow.sh


```

https://github.com/kubeflow/example-seldon

In VM
```bash
#git clone https://github.com/kubeflow/example-seldon
cd my_kubeflow/ks_app
ks pkg install kubeflow/seldon
ks pkg install kubeflow/argo

ks generate seldon seldon 
ks generate argo kubeflow-argo

ks apply default -c seldon
ks apply default -c kubeflow-argo

# Switch context for the rest of the example
#kubectl config set-context $(kubectl config current-context) --namespace=${NAMESPACE}
```

```bash
sudo snap install helm --classic
kubectl -n kube-system create sa tiller
kubectl create clusterrolebinding tiller --clusterrole cluster-admin --serviceaccount=kube-system:tiller
helm init --service-account tiller
kubectl rollout status deploy/tiller-deploy -n kube-system
```



```bash
kubectl create clusterrolebinding my-cluster-admin-binding --clusterrole=cluster-admin 
kubectl create clusterrolebinding default-admin2 --clusterrole=cluster-admin --serviceaccount=kubeflow:default
```

```bash
helm install seldon-core-analytics --name seldon-core-analytics --set grafana_prom_admin_password=password --set persistence.enabled=false --repo https://storage.googleapis.com/seldon-charts --namespace kubeflow
```

```bash
kubectl port-forward $(kubectl get pods -n kubeflow -l app=grafana-prom-server -o jsonpath='{.items[0].metadata.name}') -n kubeflow 3000:3000
```
^^ Not sure we need that.

```bash
kubectl get services -n kubeflow  | grep grafana-prom

grafana-prom                             NodePort    10.152.183.174   <none>        80:31747/TCP        17m

```
 so i surf to <vm-ip>:31747

http://10.53.148.125:3000/dashboard/db/prediction-analytics?refresh=5s&orgId=1
only will go over localhost-- need to figure out how to push that through VM and expose to outside owrld

https://github.com/SeldonIO/seldon-core/issues/209
username admin- password password

cd ~
sudo curl -sSL -o /usr/local/bin/argo https://github.com/argoproj/argo/releases/download/v2.2.1/argo-linux-amd64
sudo chmod +x /usr/local/bin/argo


wget https://raw.githubusercontent.com/kubeflow/example-seldon/master/workflows/training-sk-mnist-workflow.yaml

export DOCKER_HOST="unix:///var/snap/microk8s/current/docker.sock"

kubectl config set-context $(kubectl config current-context) --namespace=kubeflow

### Create links to spoof docker (microk8s only)    
sudo ln -s /var/snap/microk8s/current/docker.sock /var/run/docker.sock
sudo ln -s /var/snap/microk8s/common/var/lib/docker /var/lib/docker

cd ~/example-seldon/models/sk_mnist/train

docker build . -t localhost:32000/skmnistclassifier_trainer:latest
docker push localhost:32000/skmnistclassifier_trainer:latest


#### nfs volume
The example at https://github.com/kubeflow/example-seldon/ calls for using Google Cloud to make an NFS Persistent Volume 
Claim.  But Nah. 

Read here to understand why I am doing: https://kubernetes.io/docs/tasks/configure-pod-container/configure-persistent-volume-storage/

In shell in multipass:

```bash
kubectl create -f https://k8s.io/examples/pods/storage/pv-volume.yaml -n kubeflow
kubectl create -f https://k8s.io/examples/pods/storage/pv-claim.yaml -n kubeflow
```

need to delete `storageClass` from pv-claim.yaml to work on local disk (same for pv-volume.yaml. need to download and edit botht then create from local files)
https://stackoverflow.com/questions/52668938/pod-has-unbound-persistentvolumeclaims


Change last line of example-seldon/workflows/training-sk-mnist-workflow.yaml

`"nfs-1"` to `task-pv-claim` (yes remove quotes)


```bash
cd ~/example-seldon/workflows
argo submit training-sk-mnist-workflow.yaml -n kubeflow
```
 

watch progress here  (obvi adjust to your vm ip / ambassador port)
http://10.53.148.125:36993/argo/

drop thsi
edit ~/example-seldon/workflows/runtime-sk*
`"nfs-1"` to `task-pv-claim` (yes remove quotes) ... towards the end


wget https://raw.githubusercontent.com/kubeflow/example-seldon/master/notebooks/create-protos.sh
chmod +x create-protos.sh
./create-protos.sh

wget https://raw.githubusercontent.com/SeldonIO/seldon-core/master/proto/k8s/create-k8s-protos.sh
chmod +x create-k8s-protos.sh
./create-k8s-protos.sh


### Serving

```bash
sudo apt install make
sudo snap install go --classic
wget https://github.com/openshift/source-to-image/releases/download/v1.1.13/source-to-image-v1.1.13-b54d75d3-linux-amd64.tar.gz
tar -xzf source-to-image-v1.1.13-b54d75d3-linux-amd64.tar.gz
sudo cp ~/s2i /usr/local/bin
cd example-seldon/models/sk_mnist/runtime
```


update `~/example-seldon/models/sk_mnist/Makefile` change `seldonio` -> `localhost:32000`

```bash
sudo make seldon_build_image_local
docker push localhost:32000/skmnistclassifier_runtime:0.2
```

edit first line from `apiVersion: argoproj.io/v1alpha1` to `apiVersion: argoproj.io/v1alpha2`
https://github.com/SeldonIO/seldon-core/blob/master/docs/v1alpha2_update.md
also update componentSpec to componentSpecs
occurs mid file (not first line!)

```bash
argo submit serving-sk-mnist-workflow.yaml -n kubeflow -p deploy-model=true
```



get port 
kubectl get services -n kubeflow | grep grafana

https://github.com/SeldonIO/seldon-core/issues/209
username admin- password password

curl -v 0.0.0.0:30882/seldon/mnist-classifier/api/v0.1/predictions -d '{"data":{"names":["a","b"],"tensor":{"shape":[2,2],"values":[0,0,1,1]}}}' -H "Content-Type: application/json"