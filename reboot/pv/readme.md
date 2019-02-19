The example at https://github.com/kubeflow/example-seldon/ calls for using Google Cloud to make an NFS Persistent Volume 
Claim.  But Nah. 

Read here to understand why I am doing: https://kubernetes.io/docs/tasks/configure-pod-container/configure-persistent-volume-storage/

In shell in multipass:

```bash
kubectl create -f https://k8s.io/examples/pods/storage/pv-volume.yaml
kubectl create -f https://k8s.io/examples/pods/storage/pv-claim.yaml
```

Change last line of example-seldon/workflows/training-sk-mnist-workflow.yaml

`"nfs-1"` to `task-pv-storage` (yes remove quotes)


{"apiVersion": "batch/v1",
"kind": "Job",
"metadata": {"creationTimestamp": "2019-02-15T12:35:22Z",
"labels":
 {"controller-uid": "29b08ba9-311e-11e9-bdbb-5254003c1de6","job-name": "sk-train"},"name": "sk-train","namespace": "kubeflow","ownerReferences": [{"apiVersion": "argoproj.io/v1alpha1","controller": true,"kind": "Workflow","name": "kubeflow-train","uid": "1e6c3934-311e-11e9-bdbb-5254003c1de6"}],"resourceVersion": "118550","selfLink": "/apis/batch/v1/namespaces/kubeflow/jobs/sk-train","uid": "29b08ba9-311e-11e9-bdbb-5254003c1de6"},"spec": {"backoffLimit": 6,"completions": 1,"parallelism": 1,"selector": {"matchLabels": {"controller-uid": "29b08ba9-311e-11e9-bdbb-5254003c1de6"}},"template": {"metadata": {"creationTimestamp": null,"labels": {"controller-uid": "29b08ba9-311e-11e9-bdbb-5254003c1de6","job-name": "sk-train"},"name": "sk-train"},"spec": {"containers": [{"image": "seldonio/skmnistclassifier_trainer:0.2","imagePullPolicy": "Always","name": "sk-train","resources": {},"terminationMessagePath": "/dev/termination-log","terminationMessagePolicy": "File","volumeMounts": [{"mountPath": "/data","name": "persistent-storage"}]}],"dnsPolicy": "ClusterFirst","restartPolicy": "Never","schedulerName": "default-scheduler","securityContext": {},"terminationGracePeriodSeconds": 30,"volumes": [{"name": "persistent-storage","persistentVolumeClaim": {"claimName": "task-pv-storage"}}]}}},"status": {"active": 1,"startTime": "2019-02-15T12:35:23Z"}}
