require.config({
    baseUrl: 'js',
    deps: ['main'],
    paths: {
    //'jquery' : 'libs/jquery'// if loading from local directory
        // 'second': 'second',
        // 'third': 'third',
        // 'jquery': "https://code.jquery.com/jquery-1.12.3.min" // loading from CDN
    },
    shim: {
        // "person2": {
        //     "exports": "person2"
        //         // use this alias in the global scope and pass it to modules as dependency
        // },
        // "person3": {
        //     deps: ['person4'],
        //     // none AMD module, depending on another non AMD module
        //     "exports": "person3"
        // }
    }
});