BASE_PATH=$(readlink -f $(dirname $0))
cluster_name="hostpathmounter"
host_path=$BASE_PATH/mount
arg_clean=false

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
    if sudo_kind get clusters | grep "$cluster_name"; then
        sudo_kind delete cluster -n "$cluster_name"
    fi
}

create_cluster() {
    sudo_kind create cluster -n "$cluster_name" \
        --config $cfg_file \
        --kubeconfig ~/.kube/config
    sudo chown "$USER" ~/.kube/config
    sudo chmod 600 ~/.kube/config
}

generate_cfg() {
    cfg_file=$(mktemp)
    cp $BASE_PATH/kindcfg.yaml $cfg_file
    sed -i -e "s#__HOST_PATH__#$host_path#g" $cfg_file
}

deploy_app() {
    helm install hpv hostPathVolume
}

set -e

cd $BASE_PATH
parse_args "$*"

if $arg_clean; then
    clean
fi

generate_cfg
create_cluster
deploy_app