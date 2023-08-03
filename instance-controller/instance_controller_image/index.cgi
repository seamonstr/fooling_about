#!/bin/bash

set -e

LOGFILE=/var/log/index.cgi.log
POST_POST_REDIRECT=postpostredirect

log() {
    echo "$(date "+%Y/%m/%d %H:%M:%S") $*" >> $LOGFILE 
}

write_headers() {
    echo "Status: $http_status"
    echo "Content-type: text/html"
    echo ""
}

write_redirect_headers() {
    echo "Status: 303 Redirect after POST"
    echo "Location: ./"
    echo "Content-type: text/html"
    echo ""
}

parse_params() {
    ## Get content
    if [[ $REQUEST_METHOD != "POST" ]]; then
        return 0
    fi

    log Reading parms for POST
    read -rn "$CONTENT_LENGTH" parms

    local param_array
    IFS=\& read -ra param_array <<<"$parms"
    # The param array now contains our values as "key=value", which is conveniently 
    # exactly what declare needs as parameters
    log Got parms: "${param_array[@]}" 
    declare -g "${param_array[@]}"
}

get_current_state() {
    local exclude_list ns
    exclude_list=( ingress instance-controller )

    for ns in $(helm list -q 2>>$LOGFILE); do
        # shellcheck disable=SC2076
        if [[ "${exclude_list[*]}" =~ "${ns}" ]]; then
            continue
        fi
        deployed_namespaces+=( "$ns" )
    done
}

process_add() {
    if [[ -z "$chart_name" || -z "$namespace" ]]; then
        log "Nothing to do"
        return 0
    fi

    log "Adding instance $namespace from chart $chart_name"

    if kubectl get namespace "$namespace"; then
        log Instance already exists
        messages+=("Namespace $namespace already exists")
        http_status="400 Bad request"
        return 0
    fi

    log Helm install
    helm install --set "namespace=$namespace" "$namespace" "/charts/$chart_name" 1>>$LOGFILE 2>&1 
    http_status=$POST_POST_REDIRECT
}

process_delete() {
    if [[ -z "$delete" ]]; then
        log "Delete: nothing to do"
        return 0
    fi

    if ! kubectl get namespace "$delete"; then
        log "Cannot delete $delete; no such instance"
        messages+=("Cannot delete $delete; no such instance")
        http_status="400 Bad request"
        return 0
    fi

    log Helm delete
    if ! helm delete "$delete" 1>>$LOGFILE 2>&1; then 
        log helm delete returned non-zero
    fi
    http_status=$POST_POST_REDIRECT
}


# Render phase
render_messages() {
    if [[ ${#messages[@]} -gt 0 ]]; then
        echo "<h1>Messages</h1>"

        echo "<ul>"
        for msg in "${messages[@]}"; do
            echo "<li>$msg</li>"
        done
        echo "</ul>"
    fi
}

render_deployed_namespaces() {
    echo "<h1>Deployed instances</h1>"
    local ns
    if [[ ${#deployed_namespaces[@]} -gt 0 ]]; then 
        echo "<form method='POST'><table>"
        for ns in "${deployed_namespaces[@]}"; do
            echo "<tr><td>$ns</td><td><button name='delete' value='$ns'>delete</button></td></tr>"
        done
        echo "</table></form>"
    else
        echo "<p>No deployed namespaces</p>"
    fi
}

render_form() {
    echo "<h1>Create an instance</h1>"
    if [ -d /charts ]; then
        echo "<form method='post'>"
        echo "<p>Chart: "
        echo "<select name='chart_name'>"
        for chart in /charts/*; do 
            if [[ -d $chart ]]; then
                chart=$(basename "$chart")
                echo "<option value='$chart'>$chart</option>"
            fi
        done
        echo "</select></p>"
        echo "<p>Namespace: <input name='namespace'/></p>"
        echo "<p><button>Create</button></p>"
        echo "</form>"

        echo "<pre>"
        ls -la /charts 2>&1
        echo "Err: $?"
        echo "</pre>"
    else
        echo "No directory at /charts"
    fi  

    echo "<h1>Env</h1>"
    echo "<pre>"
    env | sort
    echo "</pre>"
}

http_status="200 OK"
messages=()
deployed_namespaces=()

log Parsing params
parse_params

log Processing add
process_add

log Processing delete
process_delete

if [[ "$http_status" == "$POST_POST_REDIRECT" ]]; then
  write_redirect_headers
  return 0
fi

log Getting current state for rendering
get_current_state

log Writing headers
write_headers

log Rendering messages
render_messages

log Rendering namespaces
render_deployed_namespaces

log Rendering form
render_form

log Done