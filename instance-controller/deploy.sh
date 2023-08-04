BASE_PATH=$(readlink -f $(dirname $0))
cluster_name="instance-controller"
instance_controller_ns="instance-controller"
host_path=$BASE_PATH/app-charts
arg_clean=false

log() {
    colour=$1
    shift
    echo -e "\033[0;${colour}m[$(date +%T)]\033[0m $@"
}

info() {
    log "34" $@
}

warn() {
    log "33" $@
}

error() {
    log "31" $@
}

usage() {
    echo "Usage: $(basename $0) [options]"
    echo "Deploy a new instance-controller in a kind cluster"
    echo
    echo "Options:"
    echo "  -h, --help                   Print this usage message"
    echo "  --clean                      Delete and recreate the cluster"
    echo
    echo "If --clean is not specified then any changes to the kind configuration, "
    echo "K8S node image, ingress controller and ingress resource will not take "
    echo "effect."
}

sudo_kind() {
    sudo kind "$@"
    return $?
}

load_kind_image() {
    local image
    image=$1
    kind load docker-image -n $instance_controller_ns $image
}

parse_args() {
    info Parsing command line arguments
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --clean)
                arg_clean=true
                ;;
            -h|--help)
                usage
                exit 0
                ;;
            *)
                echo "Unknown argument: $1"
                usage
                exit 1
                ;;
        esac
        shift
    done
}

clean() {
    info "Cleaning up cluster $cluster_name"
    if sudo_kind get clusters | grep "$cluster_name"; then
        info "Deleting cluster $cluster_name"
        sudo_kind delete cluster -n "$cluster_name"
    fi
}

build_docker_kind_image() {
    info "Building docker image for kind"
    docker build -t swkindest/node:latest -<<EOF
# A default kind node image with some extras to help debugging

FROM kindest/node:v1.27.3

RUN apt-get update && \
    apt-get install -y iputils-ping inetutils-traceroute netcat && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir /charts
RUN chmod 755 /charts
EOF

}

create_cluster() {
    info "Ensuring cluster $cluster_name exists"
    if sudo_kind get clusters | grep "$cluster_name"; then
        info "Cluster $cluster_name already exists; not creating"
        return 0
    fi

    # Sudo to create the cluster; needed for mounts to work. However, write 
    # the kubectl to the current user's config.
    info "Cluster doesn't exist; creating"
    sudo_kind create cluster -n "$cluster_name" \
        --config $cfg_file \
        --kubeconfig ~/.kube/config \
        --image swkindest/node:latest
    sudo chown "$USER" ~/.kube/config
    sudo chmod 600 ~/.kube/config

    # Push the nginx controller image to the control plane container
    # Note you can see the images on the container by using "ctr --namespace k8s.io image ls"
    # from its shell.  "ctr" is the containerd command line. Containerd is namespaced, 
    # and everything for the control plane is in the k8s.io namespace
    info "Pushing nginx controller image to cluster"
    load_kind_image registry.k8s.io/ingress-nginx/controller:v1.8.1
    load_kind_image registry.k8s.io/ingress-nginx/kube-webhook-certgen:v20230407
    info "Installing nginx controller"
    kubectl apply -f \
      https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml

    # Wait for the nginx controller to be ready
    info "Waiting for nginx controller to be ready"
    kubectl wait --namespace ingress-nginx \
      --for=condition=ready pod \
      --selector=app.kubernetes.io/component=controller \
      --timeout=120s
}

generate_cfg() {
    cfg_file=$(mktemp)
    info "Generating cluster config in $cfg_file"
    # Substitute the path to be mounted into the config file
    cp $BASE_PATH/kindcfg.yaml $cfg_file
    sed -i -e "s#__HOST_PATH__#$host_path#g" $cfg_file
}

get_instance_controller_image() {
    local tag
    # MD5 sum all the files, producing an md5sum output for them, and then 
    # md5sum that output, producing a hash of the directory.
    # Only use the first 7 chars; highly unlikely to get a dup, and much 
    # easier to work with.
    tag="$(md5sum $(find $BASE_PATH/instance-controller-image ! -type d) \
        | md5sum \
        | awk '{print substr($1, 1, 7)}')"
    echo instance-controller:1.0.0.$tag
}

build_app_image() {
    info "Building the instance controller docker image"
    docker build -t $(get_instance_controller_image) instance-controller-image/
}

deploy_app() {
    info "Deploying the instance controller"
    load_kind_image $(get_instance_controller_image)

    if helm list | grep instance-controller; then
        info "App already deployed; upgrading"
        helm upgrade --set instance_controller_image=$(get_instance_controller_image) \
            instance-controller instance-controller-helm
    else
        info "App not deployed; installing"
        helm install --set instance_controller_image=$(get_instance_controller_image) \
            instance-controller instance-controller-helm 
        info "Deploying ingress"
        helm install ingress ingress-helm/
    fi
}

set -e

cd $BASE_PATH
parse_args $@
if $arg_clean; then
    clean
    build_docker_kind_image
    generate_cfg
    create_cluster
fi

build_app_image
deploy_app