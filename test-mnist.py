import python.util

mnist = python.util.download_mnist()
python.util.predict_rest_mnist(mnist)

batch_xs, batch_ys = mnist.train.next_batch(1)
chosen=0
python.util.gen_image(batch_xs[chosen]).show()
data = batch_xs[chosen].reshape((1,784))
features = ["X"+str(i+1) for i in range (0,784)]
request = {"data":{"names":features,"ndarray":data.tolist()}}
print('requesting data')
predictions = python.util.rest_request("mnist-classifier",request)

import requests

deploymentName = "mnist-classifier"
AMBASSADOR_API_IP="10.53.148.125:30882"

# update endpoint: https://github.com/SeldonIO/seldon-core/blob/master/notebooks/seldon_utils.py#L102
response = requests.post(
    "http://"+AMBASSADOR_API_IP+"/seldon/"+deploymentName+"/api/v0.1/predictions",
    json=request)

print(response.status_code)
