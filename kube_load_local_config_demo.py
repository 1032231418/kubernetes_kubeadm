#!/usr/local/bin/python3.6

'''
This a simple script to demonstrate loading ~/.kube/config in python
and how to use it.
'''

from kubernetes import client, config, watch
config.load_kube_config()               # Loading config from ~/.kube/config
kubeApi = client.CoreV1Api()            # Starting the client

# Lets see all command options now available for this client.
# There are quite-a-few
for cmd in dir(kubeApi):
    print(cmd)

# Now we'll use this client to fetch various info
podList = kubeApi.list_pod_for_all_namespaces(watch=False)
nodeList = kubeApi.list_node()
nodeListhttp = kubeApi.list_node_with_http_info()
thisApiResources = kubeApi.get_api_resources_with_http_info()

# Lets check what types they are
print("podList is type {}".format(type(podList)))
print("nodeList is type {}".format(type(nodeList)))
print("nodeListhttp is type {}".format(type(nodeListhttp)))
print("thisApiResources is type {}".format(type(thisApiResources)))

# Finally lets print them to get a hang of the volume of info
# floating around this cluster
def space():
    print("\n\n")

space()
print(podList)
space()
print(nodeList)
space()
print(nodeListhttp)
space()
print(thisApiResources)
space()

print("That was quite a lot!!\n")
