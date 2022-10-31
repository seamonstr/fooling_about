class Dog {
	Save() { // Not yet sure about best practise for method names; this looks ick
		console.log(`Dog saved: ${this.name} ( colour: ${this.colour} )`);
	}
	constructor(name, colour) {
		console.log("Creating a dog.")
		this.name = name;
		this.colour = colour;
	}

	myfunc(a, b) {
		console.log("myfuncing: " + a + " " + b)
	}
}

class Cockapoo extends Dog {
}

milly = new Cockapoo("Milly", "brown and white");
milly.Save();
milly.myfunc(1)
