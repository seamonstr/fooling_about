import {secondFunction as sayHello2} from "./second";

interface MyInterface {
    MyMethod(x: string, y: number): string;
    MyMethod2(): number;
}

function myFunction(obj1: MyInterface, obj2: MyInterface) {
    let a = obj1.MyMethod("stuff", 12);
    let b = obj1.MyMethod2();
    let c = obj2.MyMethod("more stuff", 5);
    let d = obj2.MyMethod2();
}

class MyClass<T> {
    _thing: T;

    constructor(thing: T) {
        this._thing = thing;
    }

    getThing(): T {
        return this._thing;
    }
}

let a: number = 10;
let myObj = new MyClass(a);

export default MyClass;

const enum MyStuff {
    apple = 1,
    orange = 2
}

function getThings(o: MyStuff): number {
    if (o == MyStuff.apple) {
        return MyStuff.apple
    } else {
        return MyStuff.orange
    }
}

console.log(`Hello: ${sayHello2()}`)