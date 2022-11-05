let lib1 = require("./lib1");

function getLib2Message() {
    return lib1.getMessage() + " & " + getMessage();
}

function getMessage() {
    return "Stuff in Lib2!"
}

exports.getMessage = getLib2Message;