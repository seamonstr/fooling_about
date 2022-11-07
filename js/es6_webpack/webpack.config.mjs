import * as Url from "node:url";

console.log(import.meta);

export default {
    entry:{
        main: "./test.js",
    },
    output: {
        path: Url.fileURLToPath(new URL('dist', import.meta.url)),
        filename: "[name].js"
    }
}