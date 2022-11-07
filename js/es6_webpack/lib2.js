import * as lib1 from "./lib1"; 

function getLib2Message() {
    return lib1.getMessage() + " & " + getMessage();
}

function getMessage() {
    return "Stuff in Lib2!"
}

export {getLib2Message as getMessage};
