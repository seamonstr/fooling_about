define([], function() {
	myPrivateData = "a private message from third.js!"
	return {

		saySomething() {return myPrivateData;}
	}
});