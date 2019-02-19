
https://github.com/kubeflow/examples/tree/0843cdad66a5a3bec06bba1d2a5d120c713d4a8c/demos/yelp_demo

### Install KF on MicroK8s

```bash
# install line for snap (?)
# snap install multipass --beta --classic  # if you haven't installed multipass yet
multipass launch bionic -n kubeflow -m 8G -ad 40G -c 4
multipass exec kubeflow -- sudo snap install microk8s --classic
multipass shell kubeflow
```

##### In `kubeflow` vm shell

```bash
git clone https://github.com/canonical-labs/kubernetes-tools
sudo kubernetes-tools/setup-microk8s.sh 
git clone https://github.com/canonical-labs/kubeflow-tools
wget https://github.com/ksonnet/ksonnet/releases/download/v0.13.1/ks_0.13.1_linux_amd64.tar.gz
tar -xzf *gz
rm *gz
sudo cp ks*/ks /usr/local/bin
```

according to docs...
```bash
ks init kubeflow
cd kubeflow

ks registry add kubeflow github.com/kubeflow/kubeflow/tree/${VERSION}/kubeflow
ks pkg install kubeflow/core@${VERSION}
ks pkg install kubeflow/tf-serving@${VERSION}
ks pkg install kubeflow/tf-job@${VERSION}
ks generate core kubeflow-core --name=kubeflow-core
```

but I like this (sometimes need to run twice?)
```bash
kubeflow-tools/install-kubeflow.sh
```

at the end you should see.
```bash

Ambassador Port: 32591 ==> Access default Kubeflow UIs
JupyterHub Port:  ==> Access JupyerHub directly
```

If you forget later ^^ `kubectl get services -n kubeflow`


I don't think you need to do this...
```bash
export NAMESPACE=kubeflow
cd my_kubeflow/ks_app
ks env add microk8s --namespace=${NAMESPACE}
ks param set --env microk8s kubeflow-core \
  cloud "microk8s"
  
ks apply microk8s -c kubeflow-core
```

```bash
exit
multipass list
rawkintrevo@tower1:~/gits/intro-to-ml-with-kubeflow/ch2-simple-example$ multipass list
Name                    State             IPv4             Release
kubeflow                RUNNING           10.172.2.38      Ubuntu 18.04 LTS

```

browse to `<kubeflowip>:<ambassador_port>`

for me its 10.172.2.38:32591

jupyter hub enter anything for username 

```bash
multipass mount ./reboot/stuff kubeflow
```

install argo
```bash
sudo curl -sSL -o /usr/local/bin/argo https://github.com/argoproj/argo/releases/download/v2.2.1/argo-linux-amd64
sudo chmod +x /usr/local/bin/argo
```

```bash
cd ~/example-seldon/models/sk_mnist/train
docker build . -t simple-sk:latest
docker push simple-sk:latest
```
