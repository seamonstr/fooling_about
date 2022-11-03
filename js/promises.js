failOne = false
failTwo = false
failThree = true


function doOne() {
	return new Promise((success, fail) => {
		if (failOne) 
			fail("fail one");
		else
			success("one");
	})
}

function doTwo(arg) {
	return new Promise((success, fail) => {
		console.log(`In two with ${arg}`)
		if (failTwo)
			throw new Error("fail two");
		success("two")
	})
}

function doThree(arg) {
	console.log(`In three with ${arg}`)
	return new Promise((success, fail) => {
		if (failThree)
			fail("fail three");
		else
			success("three");
	})
}

doOne()
	.then((result) => doTwo(result))
	.then((result) => doThree(result))
	.catch((fail) => console.log(`fail: ${fail}`));