module.exports = {
  base: '/static/',
  build: {
    outDir: './static',
  },
  server: {
    proxy: {
      '/utslipp': 'http://localhost:5000',
    },
  },
};
