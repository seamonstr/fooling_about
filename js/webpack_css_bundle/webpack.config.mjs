import path from "node:path";
import * as Url from "node:url";

const dirname = Url.fileURLToPath(new URL('.', import.meta.url))
export default {
    mode: 'development',
    devtool: "nosources-source-map",
    entry:{
        style: "./file.css",
        start: "./main.js"
    },
    output: {
        path: path.join(dirname, 'dist'),
        publicPath: '/js/',
        filename: "[name].js"
    },
    module: {
        rules: [
            {
                test: /\.css$/,
                use: ['style-loader', 'css-loader']
            }
        ]
    },
    devServer: {
        static: './public'
    }
}