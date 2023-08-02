#!/bin/bash

set -e

LOGFILE=/var/log/index.cgi.log
log() {
    echo "$(date "+%Y/%m/%d %H:%M:%S") $*" >> $LOGFILE 
}

write_headers() {
    echo "Content-type: text/html"
    echo "Status: $http_status"
    echo ""
}

parse_params() {
    ## Get content
    if [[ $REQUEST_METHOD != "POST" ]]; then
        return 0
    fi

    log Reading parms for POST
    read -n $CONTENT_LENGTH parms
    echo "<h1>Parms</h1>"
    echo "<pre>$parms</pre>"

    local param_array
    IFS=\& read -ra param_array <<<"$(echo $parms)"
    # The param array now contains our values as "key=value", which is conveniently 
    # exactly what declare needs as parameters
    log Got parms: ${param_array[@]} 
    declare -g "${param_array[@]}"
}

process_add() {
    if [[ -z "$chart_name" || -z "$namespace" ]]; then
        log Nothing to do
        return 0
    fi

    log Adding instance $namespace from chart $chart_name

    if kubectl get namespace $namespace; then
        log Instance already exists
        messages+=("Namespace $namespace already exists")
        http_status="400 Bad request"
    fi
    log Helm install
    helm install --set "namespace=$namespace" "$namespace" "/charts/$chart_name" 1>>$LOGFILE 2>&1 
}

process_delete() {
    true
}


# Render phase
render_messages() {
    if [[ -n $messages ]]; then
        echo "<h1>Messages</h1><ul>"

        for msg in $messages; do
            echo "<li>$msg</li>"
        done
        echo "</ul><br>"
    fi
}

render_deployed_namespaces() {
    true
}

render_form() {
    echo "<h1>Create an instance</h1>"
    if [ -d /charts ]; then
        echo "<form method='post'>"
        echo "<p>Chart: "
        echo "<select name='chart_name'>"
        for chart in $(ls /charts); do 
            if [[ -d /charts/$chart ]]; then
                echo "<option value="$chart">$chart</option>"
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

http_status=200

log Parsing params
parse_params

log Processing add
process_add

log Processing delete
process_delete

log Writing headers
write_headers

log Rendering messages
render_messages

log Rendering namespaces
render_deployed_namespaces

log Rendering form
render_form

log Done