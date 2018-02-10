## We'll look at the usage of Python Kubernetes client
#### The correspoding Wiki enumerates the steps followed to install kubernetes using kubeadm on CentOS 7.4

Verify versions:
```
$ pip3.6 freeze
asn1crypto==0.23.0
bcrypt==3.1.3
cachetools==2.0.1
certifi==2018.1.18
cffi==1.11.2
chardet==3.0.4
cryptography==2.0.3
google-auth==1.3.0
idna==2.6
ipaddress==1.0.19
kafka==1.3.5
kafka-python==1.3.5
kubernetes==4.0.0
numpy==1.13.3
oauthlib==2.0.6
pandas==0.21.0
paramiko==2.3.1
pyasn1==0.4.2
pyasn1-modules==0.2.1
pycparser==2.18
pymongo==3.6.0
PyNaCl==1.1.2
PyQt5==5.9.2
python-dateutil==2.6.1
pytz==2017.3
PyYAML==3.12
requests==2.18.4
requests-oauthlib==0.8.0
rsa==3.4.2
sip==4.19.6
six==1.11.0
urllib3==1.22
websocket-client==0.40.0
```
## Lets look into the python client and validate usage of both kube_config and api keys.

#### kube_load_local_config_demo.py
This script demonstrates usage of `config.load_kube_config()`. We can use such scripts on
machines where we can run kubectl from. `config.load_kube_config()` loads ~/.kube/config and 
no API keys are required.

#### kube_connect_using_api_key.py
This script demonstrates usage of API_KEY in python. Following bash one liners can be used to fetch the TOKEN from Apiserver(aka master). I've used serviceAccount default secret token. We'll need kubectl for this bit of information.
```
APISERVER=$(kubectl config view | grep server | cut -f 2- -d ":" | tr -d " ")
TOKEN=$(kubectl describe secret $(kubectl get secrets | grep default | cut -f1 -d ' ') | grep -E '^token' | cut -f2 -d':' | tr -d '\t')
```
A rbac clusterRole binding was necessary. Without this, i was stuck with a `HTTP/1.1 403 Forbidden` message on the python client.
For sake of experimenting, created a binding between `serviceAccount default` and `cluster-admin` role.
```
$ cat service-default-admin.yaml
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRoleBinding
metadata:
  name: service-default-experimental
subjects:
  - kind: ServiceAccount
    name: default
    namespace: default
roleRef:
  kind: ClusterRole
  name: cluster-admin
  apiGroup: rbac.authorization.k8s.io


$ kubectl apply -f service-default-admin.yaml
clusterrolebinding "service-default-experimental" created
```
#### More rbac examples will follow.


