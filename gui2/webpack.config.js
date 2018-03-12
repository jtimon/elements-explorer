const path = require('path');

const BUILD_DIR = path.resolve(__dirname, 'public/js');
const APP_DIR = path.resolve(__dirname, 'src');

const config = {
  entry: `${APP_DIR}/index.jsx`,
  output: {
    path: BUILD_DIR,
    filename: 'bundle.js',
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /(node_modules|bower_components)/,
        resolve: {
          extensions: ['.js', '.jsx'],
        },
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['es2015'],
          },
        },
      },
    ],
  },
};

module.exports = config;
