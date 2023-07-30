#!/bin/sh

echo "Content-type: text/html"
echo ""
echo "<h1>File listing</h1>"
if [ -d /host ]; then
    echo "<pre>"
    ls -la /host 2>&1
    echo "Err: $?"
    echo "</pre>"
else
    echo "No directory at /host"
fi  