

From : https://www.kubeflow.org/docs/started/getting-started-multipass/
(You can't "just do it" on Linux- need to create VMs no matter what. )
```bash
snap install multipass --beta --classic
multipass launch bionic -n kubeflow -m 8G -d 40G -c 4
multipass shell kubeflow
# then in the kf shell

git clone https://github.com/canonical-labs/kubernetes-tools
sudo kubernetes-tools/setup-microk8s.sh 
git clone https://github.com/canonical-labs/kubeflow-tools
wget https://github.com/ksonnet/ksonnet/releases/download/v0.13.1/ks_0.13.1_linux_amd64.tar.gz
tar -xzf *gz
rm *gz
sudo cp ks*/ks /usr/local/bin
ks init ks_app
kubeflow-tools/install-kubeflow.sh
```

Jupyter, any login works



## Seldon core

###### install s2i

```bash
wget https://github.com/openshift/source-to-image/releases/download/v1.1.13/source-to-image-v1.1.13-b54d75d3-linux-amd64.tar.gz
tar -xvf *gz
cp ./s2i /usr/local/bin
s2i create foo fooDir 
```

####### create s2i from model

see simplesk


```bash
multipass mount ./simplesk kubeflow
multipass shell kubeflow
cd /home/rawkintrevo/gits/intro-to-ml-with-kubeflow/ch2-simple-example/simplesk
wget https://github.com/openshift/source-to-image/releases/download/v1.1.13/source-to-image-v1.1.13-b54d75d3-linux-amd64.tar.gz
tar -xzf *gz
sudo ./s2i build . seldonio/seldon-core-s2i-python3:0.4 simplesk -U unix:///var/snap/microk8s/current/docker.sock
```

test the served model
```bash
microk8s.docker run -p 5000:5000 simplesk:latest 
```


```bash
#microk8s.docker push localhost:32000/simplesk
```
```bash
# go back to ks_app
# Generate the seldon component and deploy it
ks registry add kubeflow github.com/google/kubeflow/tree/master/kubeflow
ks pkg install kubeflow/seldon
ks generate seldon seldon --namespace
ks apply default -c seldon

ks generate seldon-serve-simple-v1alpha2 simple-sk-model \
  --name=simple-sk \
  --image=simplesk \
  --replicas=2
  --namespace=kubeflow
ks apply default -c simple-sk
```

microk8s.kubectl port-forward $(microk8s.kubectl get pods -n kubeflow -l service=ambassador -o jsonpath='{.items[0].metadata.name}') -n kubeflow 8085:80 &

curl -g http://localhost:8085/predict --data-urlencode 'json={"data": {"names": ["protein", "fat", "carbo", "sugars"], "ndarray": [[5.0, 5.0, 5.0, 5.0]]}}'

curl -H "Content-Type:application/json" \
  -d '{"data": {"names": ["protein", "fat", "carbo", "sugars"], "ndarray": [[5.0, 5.0, 5.0, 5.0]]}}' \
  http://localhost:8085/seldon/simple-sk/api/v0.1/predictions
  
  
### ~~Install analytics dash~~ bridge to far right now.
```bash
sudo snap install helm --classic
helm install seldon-core-analytics --name seldon-core-analytics --set grafana_prom_admin_password=password --set persistence.enabled=false --repo https://storage.googleapis.com/seldon-charts --namespace kubeflow
kubectl -n kube-system create sa tiller
kubectl create clusterrolebinding tiller --clusterrole cluster-admin --serviceaccount=kube-system:tiller
helm init --service-account tiller
kubectl rollout status deploy/tiller-deploy -n kube-system
kubectl create clusterrolebinding my-cluster-admin-binding --clusterrole=cluster-admin --user=$(gcloud info --format="value(config.account)")
kubectl create clusterrolebinding default-admin2 --clusterrole=cluster-admin --serviceaccount=kubeflow:default
helm install seldon-core-analytics --name seldon-core-analytics --set grafana_prom_admin_password=password --set persistence.enabled=false --repo https://storage.googleapis.com/seldon-charts --namespace kubeflow
kubectl port-forward $(kubectl get pods -n kubeflow -l app=grafana-prom-server -o jsonpath='{.items[0].metadata.name}') -n kubeflow 3000:3000

exit
## how to port forward metal to multipass @ port 3000
```


### reset

#### model serve local

```bash
sudo docker run -p 5000:5000 localhost:32000/simplesk:latest
```


