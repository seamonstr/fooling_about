var myGlobal = "Default vale"

function saySomething() {
	return `twoFunc saying hello with ${myGlobal}`;
}

function setGlobal(val) {
	myGlobal = val;
}
export {saySomething as twoFunc, myGlobal, setGlobal}