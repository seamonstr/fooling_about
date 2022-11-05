// Lib1.js

function getLib1Message() {
    return getMessage();
}

function getMessage() {
    return "Do stuff in Lib1!";
}

exports.getMessage = getLib1Message;