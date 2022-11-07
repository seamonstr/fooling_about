
define(["./lib1.js"], function (lib1) {
function getLib2Message() {
    return lib1.getMessage() + " & " + getMessage();
}

function getMessage() {
    return "Stuff in Lib2!"
}
return {getMessage: getLib2Message}
})