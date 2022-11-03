import {oneFunc} from './one.js'
import * as Two from './two.js'


function newText(text) {
	var para = document.createElement("p");
	para.appendChild(document.createTextNode(text));
	return para;
}

document.getElementById("target_div").appendChild(newText("Some text, mofo."));
document.getElementById("target_div").appendChild(newText(oneFunc()));
document.getElementById("target_div").appendChild(newText(Two.twoFunc()));
Two.setGlobal("New value!");
document.getElementById("target_div").appendChild(newText(Two.twoFunc()));
