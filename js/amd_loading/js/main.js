// scriptPath: function (path, port, options) {
//     return options.getIn(['urls', 'local']) + "what now";
// }

function newText(text) {
	para = document.createElement("p");
	para.appendChild(document.createTextNode(text));
	return para;
}

require(["second"], function(second) {
	document.getElementById("target_div").appendChild(newText("Some text, mofo."));
	document.getElementById("target_div").appendChild(newText(second.saySomething()));
});