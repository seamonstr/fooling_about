define ([], 
function() {
    function getLib1Message() {
        return getMessage();
    }
    
    function getMessage() {
        return "Do stuff in Lib1!";
    }
    
    return {getMessage: getLib1Message}       
})