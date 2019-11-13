const path = require("path");
const webpack = require("webpack");

const common = require("./config/webpack.common.js");

module.exports = {
  entry: common.entry,
  output: {
    path: path.resolve(__dirname, "source/base/static"),
    publicPath: "/",
    filename: "[name].js",
  },
  resolve: common.resolve,
  module: {
    rules: common.rules,
  },
  optimization: common.optimization,
  plugins: common.plugins,
  mode: 'development',
  watchOptions: {
    poll: true
  },
};
