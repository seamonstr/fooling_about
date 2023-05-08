#!/bin/bash

# Define a function to get the parameters from the CGI environment variables
get_params() {
    read -r QUERY_STRING
    last_chunk=$(echo "$QUERY_STRING" | sed -n 's/^.*last_chunk=\([^&]*\).*$/\1/p')
}

# Define a function that takes the "last_chunk" parameter and generates the data array
get_data() {
    last_chunk="$1"

    # Read a list of the files in the data directory
    files=($(ls -1 data/))

    # Determine the file with the lowest index that is larger than last_chunk, and
    # append the next 10 (or however many we have)
    files=()
    for file in "${files[@]}"; do
        index=$(echo "$file" | sed -n 's/^chunk_\([0-9]*\)$/\1/p')
        if [ "$index" -gt "$last_chunk" ]; then
            files+=($(cat $file))
            last_chunk=$index
            if [[ ${#file[@]} -eq 10 ]]; then
                break
            fi
        fi
    done
}


# Define a function that formats the data as a JSON document
format_data() {
    files=$1
    last_chunk=$2

    # Convert each line of data into a JSON object with a "line_number" field and concatenate them into a single JSON array
    json_array=$(printf '%s\n' "${files[@]}" | jq -Rn '[inputs]')

    # Wrap the JSON array in an object with a "data" field and add a "last_line_number" field with the number of lines read
    payload=$( \
        printf '{"data":%s,"last_line_number":%d}\n' \
            "$json_array"  \
            "$((last_chunk + ${#data[@]}))" \
    )
}

# Define a function that writes the JSON document to standard output
write_output() {
    payload=$1
    printf 'Content-Type: application/json\n\n'
    echo $payload
    format_data > /dev/stdout
}

# Call all of the functions appropriately

get_params
get_data $last_chunk
format_data $files $last_chunk
write_output $payload