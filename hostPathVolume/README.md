= hostPathVolume

Experiment to run helm and kind to create a pod that mounts a local directory into a volume

* A helm chart that deploys
  * A PersistentVolume with a hostpath volume that mounts /mnt/hostpath from the node
  * A pod with a container that prints the contents of /mnt/mypath to the log on an infinite loop
  * A different pod with the same thing
  * Each of the pods requesting the hostpath PersistentVolume

* A script that creates a kind cluster, and then deploys the helm chart into it.