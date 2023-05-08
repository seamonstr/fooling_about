#!/bin/bash

# Common functions for all scripts

red () {
    echo -e "\033[0;31m$*\033[0m"
}

green () {
    echo -e "\033[0;32m$*\033[0m"
}

# For tests. Asserts that the return value of the input function was 0. 
# Use like:
# assert_true "$(echo "Hello")" "Should be true"
assert_true() {
    # shellcheck disable=SC2181
    input_status=$?

    if [[ $# != 2 ]]; then
        echo "Usage: assert_true <output> <message>"
        exit 1
    fi

    if [[ $input_status != 0 ]]; then
        red "Assertion failed: $2, output: $1"
        exit 1
    fi
}

# appends a command to the existing exit trap
#
# - 1st arg:  code to add
# - remaining args:  names of traps to modify
#
add_exit_trap() {
    trap_add_cmd=$1; shift || fatal "trap_add usage error"
    trap -- "$(
        # helper fn to get existing trap command from output
        # of trap -p
        # shellcheck disable=SC2317
        extract_trap_cmd() { printf '%s\n' "$3"; }
        # print existing trap command with newline
        eval "extract_trap_cmd $(trap -p EXIT)"
        # print the new trap command
        printf '%s\n' "${trap_add_cmd}"
    )" EXIT \
        || fatal "unable to add to trap for EXIT"
}
