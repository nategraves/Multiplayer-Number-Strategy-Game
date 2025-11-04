const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  console.log('Setting up proxy for /api to http://localhost:5000/api');
  app.use(
    '/api',
    createProxyMiddleware({
      target: 'http://localhost:5000/api',
      changeOrigin: true,
      pathRewrite: {
        '^/api': '',  // Remove /api prefix since target already has it
      },
      logLevel: 'debug',
    })
  );
};
