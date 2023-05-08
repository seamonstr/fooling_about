#!/bin/bash

set -e

# Source  the file "common.sh" in the same directory as this script
# shellcheck source-path=SCRIPTDIR
source "$(dirname "${BASH_SOURCE[0]}")/common.sh"

test_initialise() {
    DOWNLOAD_DIR=$(mktemp -d)
    export DOWNLOAD_DIR
    add_exit_trap "rm -rf ${DOWNLOAD_DIR}"

    # Create a subshell to call the function, echo some stuff and exit
    # Check that the stuff is where we expected
    # Check that the named pipe was cleaned up when the subshell exited
    (
        # shellcheck source-path=SCRIPTDIR
        source "$(dirname "${BASH_SOURCE[0]}")/stdout.sh"


        initialise

        assert_true "$( test -p "${stdout_pipe}" )" "Named pipe should exist"
        assert_true "$( test -d "${DOWNLOAD_DIR}" )" "Download dir should exist"
        echo "Hello World"
    
        exit 0
    )

    assert_true "$( test "$(cat "${DOWNLOAD_DIR}/WORKING_CHUNK.txt")" = "Hello World" )" \
        "Output should be in the working chunk"

    assert_true "$( test ! -p "${stdout_pipe}" )" "Named pipe should no longer exist"
}

test_roll() {
    rm -rf /var/tmp/stdout.txt

    DOWNLOAD_DIR=$(mktemp -d)
    export DOWNLOAD_DIR

    add_exit_trap "rm -rf ${DOWNLOAD_DIR}"

    # Write enough to roll the chunk; check that it rolls where we expect
    (
        # shellcheck source-path=SCRIPTDIR
        source "$(dirname "${BASH_SOURCE[0]}")/stdout.sh"

        initialise
        echo "one"
        echo "two"
        echo "three"
        echo "four"
        echo "five"
        echo "six"
        echo "seven"
        echo "eight"
        echo "nine"
        echo "ten"
        echo "eleven"
        exit 0
    )

    # wait for the reader subshell to exit
    sleep 1
    assert_true "$( test "-f ${DOWNLOAD_DIR}/0_chunk.txt" )" \
        "Chunk 0 should exist"

    assert_true "$( test "$(cat "${DOWNLOAD_DIR}/WORKING_CHUNK.txt")" = "eleven" )" \
        "working chunk should contain the last line"

}

test_initialise
test_roll

green "All tests passed"
