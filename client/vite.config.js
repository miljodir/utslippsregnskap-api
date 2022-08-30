module.exports = {
  base: '/static/',
  build: {
    outDir: './static',
    sourcemap: true,
  },
  server: {
    proxy: {
      '/utslipp': 'http://localhost:5000',
      '/login': 'http://localhost:5000',
      '/logout': 'http://localhost:5000',
    },
  },
};
