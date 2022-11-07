function getLib1Message() {
    return getMessage();
}

function getMessage() {
    return "Do stuff in Lib1!";
}

export {getLib1Message as getMessage}