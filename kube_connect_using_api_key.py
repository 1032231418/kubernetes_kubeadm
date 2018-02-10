#!/usr/local/bin/python3.6

'''
This is a simple program to demonstrate usage of API-KEY (aka Token) in kube-python
I used the serviceAccount default and did a rbac binding with cluster-admin role. More
details in README.md

This approach should be used only for initial experiments. Later the appropriate usage
would be to create customer roles and users, accounts and appropriate rbac bindings.
ApiToken below is obtained using kubectl:
$ kubectl describe secret $(kubectl get secrets | grep default | cut -f1 -d ' ') \
                        | grep -E '^token' | cut -f2 -d':' | tr -d '\t'
'''

from kubernetes import client, config
from kubernetes.client.rest import ApiException
ApiToken = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImRlZmF1bHQtdG9rZW4tbXF0eG4iLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGVmYXVsdCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjA5NWQ3ZGVhLTA5MDgtMTFlOC04NTFiLTA4MDAyNzk0OGE2OSIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmRlZmF1bHQifQ.DBk6gyh4BFy-Gc94dihasYXLbspMvMEjuzFS-AEyNUwk6pR1zsdYOqxo5J-0t6qHN09JyyNK5Oz75cR6bYOGxir1a7SveQpXly4S2Iu3K3o6n8ys_kdP4lNMgBZy--rE0h4neG9s91ven36XP4nYZMwvWal56w39nCUmkomR2-DfhaD4-_Mqq2bd7lmETNinD2hpzTa9cf46VTTY0kcIwhk8FzxEtPA3kxoZul0AfpZT2QlyzLk9fTBRPjd57XbktBgQmiO2wppa_A1KN1Kg83fk1p40hSfY4Vf7Dr76rmKgAUVae-qkN725FWj-4NqzktjyAqalli5jcHo2leJv0A'
configuration = client.Configuration()
configuration.host = 'https://192.168.0.110:6443'
configuration.verify_ssl=False
configuration.debug = True
configuration.api_key = {"authorization": "Bearer " + ApiToken}
client.Configuration.set_default(configuration)
kubeApi = client.CoreV1Api()

try:
    allPods = kubeApi.list_pod_for_all_namespaces(watch=False)
except ApiException as e:
    print("Exception when calling CoreV1Api->list_pod_for_all_namespaces: %s\n" % e)

print(allPods)
