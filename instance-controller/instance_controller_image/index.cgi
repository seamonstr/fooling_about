#!/bin/bash

echo "Content-type: text/html"
echo ""

messages=""

#### Parse phase

# POST?
    # Get content
    read 
    # Split into parms

#### Process phase

# Process add
echo "<pre>"
env | sort
echo "</pre>"

# Process delete


#### Render phase
if [[ -n $messages ]]; then
    echo "<h1>Messages</h1><ul>"

    for msg in $messages; do
        echo "<li>$msg</li>"
    done
    echo "</ul><br>"
fi

echo "<h1>Available charts</h1>"
if [ -d /charts ]; then
    echo "<table>"
    for chart in $(ls /charts); do 
        if [[ -d $chart ]]; then
            echo "<tr><td>$chart</td></tr>"
        fi
    done
    echo "</table>"
    echo "<pre>"
    ls -la /charts 2>&1
    echo "Err: $?"
    echo "</pre>"
else
    echo "No directory at /charts"
fi  