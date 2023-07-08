source "$(dirname "${BASH_SOURCE[0]}")/../common.sh"
source "$(dirname "${BASH_SOURCE[0]}")/../next_batch.sh"

test_get_params() {
    get_params "some/stuff?last_chunk=29"
    assert_true "$( test "$last_chunk" = "29" )" "last_chunk not extracted correctly"

    get_params "some/stuff"
    assert_true "$( test "$last_chunk" = "" )" "last_chunk should be empty: A"

    get_params "some/stuff?last_chunk=wibble"
    assert_true "$( test "$last_chunk" = "" )" "last_chunk should be empty: B"
}

argcount() {
    echo argcount: $#
}

test_get_data() {
    testdir=$(mktemp -d)
    add_exit_trap "rm -rf $testdir"
    echo $'this\nten' >> "$testdir/chunk_10"
    echo $'this\neleven' >> "$testdir/chunk_11"
    echo $'this\ntwelve' >> "$testdir/chunk_12"
    echo $'this\nthirteen' >> "$testdir/chunk_13"

    get_data 11 $testdir
    assert_true "$( test "${batch[*]}" = $'this\ntwelve this\nthirteen' )" \
        "Batch didn't match as expected: happy path"

    # Check missing chunks work
    rm "$testdir/chunk_12"
    echo $'this\nfourteen' >> "$testdir/chunk_14"

    get_data 10 $testdir
    assert_true "$( test "${batch[*]}" = $'this\neleven this\nthirteen this\nfourteen' )" \
        "Batch didn't match as expected: missing chunks"

    echo $'this' >> "$testdir/chunk_15"
    echo $'this' >> "$testdir/chunk_16"
    echo $'this' >> "$testdir/chunk_17"
    echo $'this 18' >> "$testdir/chunk_18"
    echo $'this' >> "$testdir/chunk_19"
    echo $'this' >> "$testdir/chunk_20"
    echo $'this 21' >> "$testdir/chunk_21"
    echo $'this' >> "$testdir/chunk_22"
    echo $'this' >> "$testdir/chunk_23"
    echo $'this' >> "$testdir/chunk_24"
    echo $'this 25' >> "$testdir/chunk_25" 

    get_data 10 $testdir
    assert_true "$( test "${#batch[@]}" -eq 10 )" \
        "Batch didn't match as expected: max 10 chunks"
    assert_true "$( test "${batch[9]}" == $"this 21" )" \
        "Batch didn't match as expected: 10th element"
    assert_true "$( test "${batch[6]}" == $"this 18" )" \
        "Batch didn't match as expected: 7th element"

    get_data 21 $testdir
    assert_true "$( test "${#batch[@]}" -eq 4 )" \
        "Batch didn't match as expected: remaining four chunks"
    assert_true "$( test "${batch[3]}" == $"this 25" )" \
        "Batch didn't match as expected: 4th element"

}

test_format_data() {
    files=(
        "data file 1"
        "data file 2"
        $'data\nwith\nretchars'
        "data file 3"
    )

    format_data 20 "${files[@]}"

    expected_payload='{"data":["data file 1","data file 2","data with retchars","data file 3"],"last_line_number":20}'
    assert_true "$( test "$payload" == "$expected_payload")" \
          "Formatted data not as expected"
}

test_format_data
test_get_params
test_get_data
green All tests passed
