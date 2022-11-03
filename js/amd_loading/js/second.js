define(['third'], function (third) {
	privateFunction = function () {
		return `Private function in second, with a call: ${third.saySomething()}`
	}

	return {
		saySomething: function() {
			return "Second saying something: " + privateFunction();
		}
	};
});