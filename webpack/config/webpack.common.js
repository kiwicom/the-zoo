const path = require("path")
var glob = require("glob")
const { VueLoaderPlugin } = require("vue-loader")
const MiniCssExtractPlugin = require("mini-css-extract-plugin")
const StyleLintPlugin = require("stylelint-webpack-plugin")

const extractText = new MiniCssExtractPlugin({
  filename: "[name].css",
})

function scanStaticFiles() {
  basePath = path.resolve(__dirname, "..", "source/")
  entryPoints = {}

  filePaths = glob.sync(basePath + '/*/' + 'assets/js/*.js')

  if (filePaths) {
    entryPoints = Object.assign.apply(
      {},
      filePaths.map((filePath) => ({ [path.parse(filePath).name]: filePath }))
    )
  }

  return entryPoints
}

module.exports = {
  entry: scanStaticFiles,
  resolve: {
    extensions: [".js", ".vue", ".less"],
    alias: {
      "../../theme.config$": path.resolve(__dirname, "..", "source/base/assets/theme.config"),
      "zoo:base": path.resolve(__dirname, "..", "source/base/assets"),
      vue: "vue/dist/vue.common.js"
    }
  },
  rules: [{
    test: /\.css$/,
    use: [
      MiniCssExtractPlugin.loader,
      "css-loader",
      "postcss-loader",
    ],
  },
  {
    test: /\.less$/,
    use: [
      MiniCssExtractPlugin.loader,
      "css-loader",
      "postcss-loader",
      "less-loader",
    ]
  },
  {
    test: /\.vue$/,
    loader: "vue-loader",
  },
  {
    test: /\.js$/,
    loader: "babel-loader",
    exclude: /node_modules/
  },
  {
    test: /\.jpe?g$|\.gif$|\.ico$|\.png$|\.svg$/,
    loader: "file-loader",
    options: {
      name: "img/[name].[ext]",
      publicPath: "./"
    }
  },
  {
    test: /\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/,
    loader: "url-loader?mimetype=application/font-woff",
    options: {
      name: "fonts/[name].[ext]"
    }
  },
  {
    test: /\.(ttf|eot|otf)(\?v=[0-9]\.[0-9]\.[0-9])?$/,
    loader: "file-loader",
    options: {
      name: "fonts/[name].[ext]"
    }
  }
  ],
  optimization: {
    splitChunks: {
      chunks: "all",
      cacheGroups: {
        commons: {
          test: /\/node_modules\//,
          name: "vendor",
          chunks: "all",
        },
      },
    },
  },
  plugins: [
    extractText,
    new VueLoaderPlugin(),
    new MiniCssExtractPlugin()
  ]
}
