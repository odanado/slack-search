const resolve = require('path').resolve

module.exports = {
  root: true,
  env: {
    browser: true,
    node: true
  },
  parserOptions: {
    parser: 'babel-eslint'
  },
  extends: [
    'plugin:vue/strongly-recommended',
    'airbnb-base'
  ],
  // required to lint *.vue files
  plugins: [
    'vue'
  ],
  // add your custom rules here
  rules: {
    'no-param-reassign': [2, { 'props': false }],
    'import/prefer-default-export': 0,
  },
  settings: {
    'import/resolver': {
      webpack: {
        config: {
          resolve: {
            alias: {
              '~': __dirname,
              'static': resolve(__dirname, 'static'),
              '~static': resolve(__dirname, 'static'),
              'assets': resolve(__dirname, 'assets'),
              '~assets': resolve(__dirname, 'assets'),
              '~plugins': resolve(__dirname, 'plugins'),
              '~store': resolve(__dirname, 'store'),
              '~pages': resolve(__dirname, 'pages'),
              '~components': resolve(__dirname, 'components'),
              '~layouts': resolve(__dirname, 'layouts')
            }
          }
        }
      }
    }
  }
}
