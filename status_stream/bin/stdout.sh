#!/bin/bash

# shellcheck source-path=SCRIPTDIR
source "$(dirname "${BASH_SOURCE[0]}")/common.sh"

stdout_pipe="/var/tmp/${$}_stdout.pipe"

# Initialise the stdout mechanism with a callback command specified in $1.

# Location to write chunk files to
if [[ -z "${DOWNLOAD_DIR}" ]]; then
    DOWNLOAD_DIR=/var/tmp/chunk_output
fi

# Number of lines to write to each chunk file
if [[ -z "${CHUNK_LINES}" ]]; then
    CHUNK_LINES=10
fi


# After intialisation, stdout and stderr will be redirected to a named pipe.  A
# background subshell will read from the pipe and call the callback function with each
# line of output.
initialise() {
    echo Initialising
    add_exit_trap "red initialise exit traps running"

    if [[ ! -d "${DOWNLOAD_DIR}" ]]; then
        mkdir -p "${DOWNLOAD_DIR}"
    fi

    # Remove the lock file if it exists; in case the previous run crashed
    rm -f "${DOWNLOAD_DIR}/roll_lock"

    echo writing to "${DOWNLOAD_DIR}"
    echo Making pipe
    add_exit_trap "rm -f $stdout_pipe" EXIT
    # Create a named pipe
    mkfifo "${stdout_pipe}"

    # Kick off these two subshells before we redirect stdout
    start_pipe_reader
    EXIT_FILE=$(mktemp)
    add_exit_trap "rm -f $EXIT_FILE" EXIT
    start_dead_chunk_watcher "$EXIT_FILE"

    add_exit_trap "red initialise exit traps completed"
    echo Initialised: traps are: $(trap -p)
    # Redirect stdout to the pipe
    exec 1>"${stdout_pipe}" 2>&1

}

# Add subshell to watch the current chunk and roll it if it's got some lines in it
# but hasn't been touched in a while - this is to handle the case where the
# main process has died or hung (and so has stopped writing to the chunk), and we 
# need to roll the chunk to get the last bit of data out.
start_dead_chunk_watcher() {
    EXIT_FILE=$1
    (   
        echo dead_chunk_watcher started
        # If the working chunk hasn't been updated in the last minute, roll it
        while [[ -f "$EXIT_FILE" ]]; do
            if [[ $(find "${DOWNLOAD_DIR}/WORKING_CHUNK.txt" -mmin +1) ]]; then
                roll_chunk
            fi
            sleep 10
        done        
        echo dead_chunk_watcher exiting
    ) &

}

start_pipe_reader() {
    # The moment we set the pipe as our stdout and write to it, we will block until the
    # pipe gets a reader (which, given it's us creating the reader, will never happen).
    # So we need to create a background subshell to read from the pipe before we
    # redirect stdout to it.
    
    # Also, because we're kicking off the subshell before
    # redirecting stdout, the subshell will inherit the original stdout - which is what
    # we want.  We can redirect the subshell's stdout to the original stdout.
    (        
        echo Subshell started
        while read -r line; do
            echo "Line to stdout: ${line}"
            chunk_output "${line}"
        done <${stdout_pipe}
    ) &
}

next_chunk=0

roll_chunk() {
    local linecount
    # Loop until we get the lock "set -C" will force the redirection to fail if the 
    # file exists, so it acts like an atomic create-if-not-exist function
    while ! { set -C; true 2>/dev/null >"${DOWNLOAD_DIR}/roll_lock"; }; do
        sleep 1
    done

    echo Got lock for chunk roll
    # Double-check that the working chunk is large enough to roll.  It's possible 
    # that another process has rolled it while we were waiting for the lock.
    linecount=$(wc -l < "${DOWNLOAD_DIR}/WORKING_CHUNK.txt")
    if _=$(( linecount % CHUNK_LINES == 0 )); then
        echo Rolling chunk to ${next_chunk}_chunk.txt
        fn=$(printf "chunk_%010d" ${next_chunk})
        mv "${DOWNLOAD_DIR}/WORKING_CHUNK.txt" \
            "${DOWNLOAD_DIR}/${fn}"
        next_chunk=$((next_chunk+1))
    fi

    rm -f "${DOWNLOAD_DIR}/roll_lock"
}

# Callback function to output the lines to chunk files
chunk_output() {
    local line=$1

    echo "${line}" >> "${DOWNLOAD_DIR}/WORKING_CHUNK.txt"
    
    if [[ $(wc -l < "${DOWNLOAD_DIR}/WORKING_CHUNK.txt") -ge ${CHUNK_LINES} ]]; then
        echo Calling roll_chunk
        roll_chunk
    fi
}