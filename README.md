# Install kubernetes using kubeadm on CentOS 7.4

Bringing up a kubernetes cluster on 4 VMs running CentOS 7.4. Master has 4G memory and all 3 Nodes has 2G memory each.

## Prerequisites

1. Open respective ports as outlined in [this](https://kubernetes.io/docs/setup/independent/install-kubeadm/#check-required-ports) link. Opened 8285 as well here, as we'll be using flannel as our CNI.

#### Master
```
sudo firewall-cmd --permanent --zone=public --add-port=6443/tcp
sudo firewall-cmd --permanent --zone=public --add-port=2379/tcp
sudo firewall-cmd --permanent --zone=public --add-port=2380/tcp
sudo firewall-cmd --permanent --zone=public --add-port=10250/tcp
sudo firewall-cmd --permanent --zone=public --add-port=10251/tcp
sudo firewall-cmd --permanent --zone=public --add-port=10252/tcp
sudo firewall-cmd --permanent --zone=public --add-port=10255/tcp
sudo firewall-cmd --permanent --zone=public --add-port=8285/udp
sudo firewall-cmd --reload
```

#### Nodes
```
sudo firewall-cmd --zone=public --add-port=10250/tcp
sudo firewall-cmd --zone=public --add-port=10255/tcp
sudo firewall-cmd --zone=public --add-port=30000-32767/tcp
sudo firewall-cmd --permanent --zone=public --add-port=8285/udp
sudo firewall-cmd --reload
```

2. Disable swap on all machines to fulfill one of the [requirements](https://kubernetes.io/docs/setup/independent/install-kubeadm/#before-you-begin)
```
sudo swapoff -a
sudo vi /etc/fstab     ; Comment out the line for swap`
sudo mount -a          ; verify if we're still using swap. If so, lets reboot and check again
```

3. Ensure selinux is disabled and update some sysctl parameters as suggested [here](https://kubernetes.io/docs/setup/independent/install-kubeadm/) for CentOS. Following commands were run as root on all machines.
```
setenforce 0
echo "net.bridge.bridge-nf-call-iptables=1" >> /etc/sysctl.conf
echo "net.bridge.bridge-nf-call-ip6tables=1" >> /etc/sysctl.conf
sysctl -p
```

## Lets start installing

1. Install flannel
```
sudo yum install flannel -y
```

2. Install docker 1.12.6 using RPM from [here](https://yum.dockerproject.org/repo/main/centos/7/Packages/docker-engine-1.12.6-1.el7.centos.x86_64.rpm) on all machines
```
yum install docker-engine-1.12.6-1.el7.centos.x86_64.rpm
mkdir -p /etc/docker && touch /etc/docker/daemon.json
cat << EOF > /etc/docker/daemon.json
{
  "exec-opts": ["native.cgroupdriver=systemd"]
}
systemctl enable docker && systemctl start docker
sudo usermod -aG docker $(whoami)    ; as the standard user
```

3. Install kubelet, kubeadm and kubectl on all machines. I ran all the following commands as root.
```
cat <<EOF > /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
EOF

yum install -y kubelet kubeadm kubectl
```

4. Initialize the Master
```
[root@master ~]# kubeadm init --pod-network-cidr=10.244.0.0/16
[init] Using Kubernetes version: v1.9.2
[init] Using Authorization modes: [Node RBAC]
[preflight] Running pre-flight checks.
	[WARNING Hostname]: hostname "master.kube" could not be reached
	[WARNING Hostname]: hostname "master.kube" lookup master.kube on 8.8.8.8:53: no such host
	[WARNING Firewalld]: firewalld is active, please ensure ports [6443 10250] are open or your cluster may not function correctly
	[WARNING FileExisting-crictl]: crictl not found in system path
[certificates] Generated ca certificate and key.
[certificates] Generated apiserver certificate and key.
[certificates] apiserver serving cert is signed for DNS names [master.kube kubernetes kubernetes.default kubernetes.default.svc kubernetes.default.svc.cluster.local] and IPs [10.96.0.1 192.168.0.110]
[certificates] Generated apiserver-kubelet-client certificate and key.
[certificates] Generated sa key and public key.
[certificates] Generated front-proxy-ca certificate and key.
[certificates] Generated front-proxy-client certificate and key.
[certificates] Valid certificates and keys now exist in "/etc/kubernetes/pki"
[kubeconfig] Wrote KubeConfig file to disk: "admin.conf"
[kubeconfig] Wrote KubeConfig file to disk: "kubelet.conf"
[kubeconfig] Wrote KubeConfig file to disk: "controller-manager.conf"
[kubeconfig] Wrote KubeConfig file to disk: "scheduler.conf"
[controlplane] Wrote Static Pod manifest for component kube-apiserver to "/etc/kubernetes/manifests/kube-apiserver.yaml"
[controlplane] Wrote Static Pod manifest for component kube-controller-manager to "/etc/kubernetes/manifests/kube-controller-manager.yaml"
[controlplane] Wrote Static Pod manifest for component kube-scheduler to "/etc/kubernetes/manifests/kube-scheduler.yaml"
[etcd] Wrote Static Pod manifest for a local etcd instance to "/etc/kubernetes/manifests/etcd.yaml"
[init] Waiting for the kubelet to boot up the control plane as Static Pods from directory "/etc/kubernetes/manifests".
[init] This might take a minute or longer if the control plane images have to be pulled.
[apiclient] All control plane components are healthy after 240.514731 seconds
[uploadconfig] Storing the configuration used in ConfigMap "kubeadm-config" in the "kube-system" Namespace
[markmaster] Will mark node master.kube as master by adding a label and a taint
[markmaster] Master master.kube tainted and labelled with key/value: node-role.kubernetes.io/master=""
[bootstraptoken] Using token: a5d8fa.aabd9968ffb836cb
[bootstraptoken] Configured RBAC rules to allow Node Bootstrap tokens to post CSRs in order for nodes to get long term certificate credentials
[bootstraptoken] Configured RBAC rules to allow the csrapprover controller automatically approve CSRs from a Node Bootstrap Token
[bootstraptoken] Configured RBAC rules to allow certificate rotation for all node client certificates in the cluster
[bootstraptoken] Creating the "cluster-info" ConfigMap in the "kube-public" namespace
[addons] Applied essential addon: kube-dns
[addons] Applied essential addon: kube-proxy

Your Kubernetes master has initialized successfully!

To start using your cluster, you need to run the following as a regular user:

  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config

You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  https://kubernetes.io/docs/concepts/cluster-administration/addons/

You can now join any number of machines by running the following on each node
as root:

  kubeadm join --token a5d8fa.aabd9968ffb836cb 192.168.0.110:6443 --discovery-token-ca-cert-hash sha256:b1649a5e2414f57b44bb37b42847473d948bfaa4f0aa2e12b8837356507beaf0
```

5. Run below commands as a standard user. The root cannot run kubectl by default.
```
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

6. Lets join our Nodes to Master. Pasted this command verbatim from output of `kubeadm init`
```
[root@node2 ~]# kubeadm join --token a5d8fa.aabd9968ffb836cb 192.168.0.110:6443 --discovery-token-ca-cert-hash sha256:b1649a5e2414f57b44bb37b42847473d948bfaa4f0aa2e12b8837356507beaf0
```

7. We need the following to complete integration with flanneld
```
kubectl create -f https://raw.githubusercontent.com/coreos/flannel/v0.9.1/Documentation/kube-flannel.yml
kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/v0.9.1/Documentation/kube-flannel.yml
```

8. The kube-dns pod had `crashloopbackoff` errors. This looked like iptables and ip forwarding issues. Ran the following commands as well on Master and all Nodes.
```
echo "net.ipv4.conf.all.forwarding=1" >> /etc/sysctl.conf && sysctl -p   ; on all hosts
sudo iptables -P FORWARD ACCEPT
systemctl stop kubelet
systemctl stop docker
iptables --flush
iptables -tnat --flush
systemctl start kubelet
systemctl start docker
```

9. Final status
```
[papu@master ~]$ kubectl get pods --all-namespaces
NAMESPACE     NAME                                  READY     STATUS    RESTARTS   AGE
kube-system   etcd-master.kube                      1/1       Running   2          14h
kube-system   kube-apiserver-master.kube            1/1       Running   4          14h
kube-system   kube-controller-manager-master.kube   1/1       Running   2          14h
kube-system   kube-dns-6f4fd4bdf-nhs6h              3/3       Running   75         14h
kube-system   kube-flannel-ds-b66nj                 1/1       Running   4          10h
kube-system   kube-flannel-ds-jn48q                 1/1       Running   2          10h
kube-system   kube-flannel-ds-r4gqw                 1/1       Running   2          10h
kube-system   kube-flannel-ds-vqzjv                 1/1       Running   2          10h
kube-system   kube-proxy-4pxsk                      1/1       Running   2          14h
kube-system   kube-proxy-bgfbh                      1/1       Running   2          14h
kube-system   kube-proxy-q7xmk                      1/1       Running   2          14h
kube-system   kube-proxy-qvz58                      1/1       Running   2          14h
kube-system   kube-scheduler-master.kube            1/1       Running   2          14h

[papu@master ~]$ ip address
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP qlen 1000
    link/ether 08:00:27:94:8a:69 brd ff:ff:ff:ff:ff:ff
    inet 192.168.0.110/24 brd 192.168.0.255 scope global dynamic enp0s3
       valid_lft 75517sec preferred_lft 75517sec
    inet6 fe80::aea:9de6:2e82:c29a/64 scope link 
       valid_lft forever preferred_lft forever
3: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN 
    link/ether 02:42:66:7b:67:19 brd ff:ff:ff:ff:ff:ff
    inet 172.17.0.1/16 scope global docker0
       valid_lft forever preferred_lft forever
4: flannel.1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue state UNKNOWN 
    link/ether ae:8c:3e:20:1e:54 brd ff:ff:ff:ff:ff:ff
    inet 10.244.0.0/32 scope global flannel.1
       valid_lft forever preferred_lft forever
    inet6 fe80::ac8c:3eff:fe20:1e54/64 scope link 
       valid_lft forever preferred_lft forever
```
