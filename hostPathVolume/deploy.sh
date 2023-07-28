BASE_PATH=$(readlink -f $(dirname $0))
cluster_name="hostpathmounter"
host_path=$BASE_PATH/mount
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
    echo "Deploy the hostPathVolume helm chart to a kind cluster"
    echo
    echo "Options:"
    echo "  -c, --cluster-name <name>    Name of the cluster to create"
    echo "  -h, --help                   Print this usage message"
}

sudo_kind() {
    sudo kind "$@"
    return $?
}

parse_args() {
    info Parsing command line arguments
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --clean)
                arg_clean=true
                ;;
            -c|--cluster-name)
                cluster_name="$2"
                shift
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

create_cluster() {
    info "Ensuring cluster $cluster_name exists"
    if sudo_kind get clusters | grep "$cluster_name"; then
        info "Cluster $cluster_name already exists; not creating"
        return 0
    fi

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
    kind load docker-image -n hostpathmounter registry.k8s.io/ingress-nginx/controller:v1.8.1
    kind load docker-image -n hostpathmounter registry.k8s.io/ingress-nginx/kube-webhook-certgen:v20230407
    info "Installing nginx controller"
    # Can pull sources locally too; see
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
    info "Generating cluster config in $cfg_file"
    cfg_file=$(mktemp)
    cp $BASE_PATH/kindcfg.yaml $cfg_file
    sed -i -e "s#__HOST_PATH__#$host_path#g" $cfg_file
}

deploy_app() {
    info "Deploying app"
    if helm list | grep hpv; then
        info "App already deployed; upgrading"
        helm upgrade hpv hostPathVolume
    else
        info "App not deployed; installing"
        helm install hpv hostPathVolume
        info "Deploying ingress"
        helm install ingress ingress/
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
EOF

}

set -e

cd $BASE_PATH
parse_args $@
if $arg_clean; then
    clean
fi

build_docker_kind_image
generate_cfg
create_cluster

deploy_app