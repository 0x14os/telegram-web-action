module.exports = {
  entry: 'src/index.js',
  publicPath: './',
  proxy: {
    '/**': {
      enable: true,
      target: 'http://127.0.0.1:8091',
    },
  },
  plugins: [
    ['ice-plugin-fusion', {
      themePackage: '@icedesign/theme',
      themeConfig: {
        primaryColor: '#447eff',
      },
    }],
    ['ice-plugin-moment-locales', {
      locales: ['zh-cn'],
    }],
  ],
};
