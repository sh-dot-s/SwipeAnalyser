var webpack = require('webpack');
var path = require('path');

var library = 'animateJs';
var outputFolder = 'dist';
var outputFile = 'animate-js.js';

var config = {
    entry: __dirname + '/src/index.js',
    devtool: 'source-map',
    output: {
        path: path.join(__dirname, outputFolder),
        filename: outputFile,
        library: library,
        libraryTarget: 'umd',
        umdNamedDefine: true
    },
    module: {
    loaders: [
        {
            loader: 'babel-loader',
            test: /\.js$/,
            exclude: /(node_modules|bower_components)/,

            query: {
                presets: ['es2015']
            }
        }    ]
    },
    resolve: {
        root: path.resolve('./src'),
        extensions: ['', '.js']
    }
};

module.exports = config;
