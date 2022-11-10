define(["require", "exports", "./second"], function (require, exports, second_1) {
    "use strict";
    exports.__esModule = true;
    function myFunction(obj1, obj2) {
        var a = obj1.MyMethod("stuff", 12);
        var b = obj1.MyMethod2();
        var c = obj2.MyMethod("more stuff", 5);
        var d = obj2.MyMethod2();
    }
    var MyClass = /** @class */ (function () {
        function MyClass(thing) {
            this._thing = thing;
        }
        MyClass.prototype.getThing = function () {
            return this._thing;
        };
        return MyClass;
    }());
    var a = 10;
    var myObj = new MyClass(a);
    exports["default"] = MyClass;
    function getThings(o) {
        if (o == 1 /* MyStuff.apple */) {
            return 1 /* MyStuff.apple */;
        }
        else {
            return 2 /* MyStuff.orange */;
        }
    }
    console.log("Hello: ".concat((0, second_1.secondFunction)()));
});
