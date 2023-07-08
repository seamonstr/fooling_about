#!/bin/bash


# Define a function to get the parameters from the CGI environment variables
get_params() {
    qry_string=$1
    last_chunk=""
    if [[ $qry_string =~ ^.*last_chunk=([^&]*).*$ ]]; then
        last_chunk=${BASH_REMATCH[1]}
        if [[ ! "$last_chunk" =~ ^[0-9]+$ ]]; then
            last_chunk=""
        fi
    fi
    [[ "$last_chunk" != "" ]]
}

# Define a function that takes the "last_chunk" parameter and generates the data array
get_data() {
    last_chunk="$1"
    data_dir="$2"

    # Read a list of the files in the data directory
    files=($(ls -1 $data_dir/))

    # Determine the file with the lowest index that is larger than last_chunk, and
    # append the next 10 (or however many we have)
    batch=()
    for file in "${files[@]}"; do
        index=$(echo "$file" | sed -n 's/^chunk_\([0-9]*\)$/\1/p')
        if [ "$index" -gt "$last_chunk" ]; then
            batch+=("$(cat $data_dir/$file)")
            last_chunk=$index
            if [[ ${#batch[@]} -eq 10 ]]; then
                break
            fi
        fi
    done
}


# Define a function that formats the data as a JSON document
format_data() {
    last_chunk=$1
    shift
    batch=("$@")

    local json_str
    local delim

    # Convert each line of data into a JSON object with a "line_number" field and concatenate them into a single JSON array
    json_str="["
    delim=""
    for f in "${files[@]}"; do
        f=$(echo $f | sed s/\"/\\\"/g)
        json_str+="$delim\"$f\""
        delim=","
    done
    json_str+="]"

    # Wrap the JSON array in an object with a "data" field and add a "last_line_number" field with the number of lines read
    payload=$(
        printf '{"data":%s,"last_line_number":%d}' "$json_str" "$last_chunk"
    )
}

# Define a function that writes the JSON document to standard output
write_output() {
    payload=$1
    echo 'Content-Type: application/json\n\n'
    echo "$payload"
}

# Only do the next bit if we've been executed as a script, not just sourced from another script
(return 0 2>/dev/null) && sourced=1 || sourced=0
if [[ $sourced == 0 ]]; then
    # Call all of the functions appropriately
    get_params $QUERY_STRING
    get_data $last_chunk $CHUNK_DIR
    format_data $batch $last_chunk
    write_output $payload
fi