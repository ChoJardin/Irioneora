module.exports = {
  devServer: {
    proxy: {
      "^/openapi": {
        target: 'http://www.emuseum.go.kr/',
        ws:true,
        changeOrigin: true

      }
    }
  }
}