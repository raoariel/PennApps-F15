module.exports = function(grunt) {
  require('jit-grunt')(grunt);

  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),

    browserify: {
      options: {
        browserifyOptions: {
          extensions: ['.jsx'],
          paths: ['pennapps/AI_chat/src/js', 'pennapps/AI_chat/src/jsx'],
        },
        transform: [['babelify', { modules: 'commonStrict' }]],
        watch: true,
        keepAlive: true,
      },
      build: {
        src: 'pennapps/AI_chat/src/jsx/main.jsx',
        dest: 'pennapps/AI_chat/static/<%= pkg.name %>.js',
      },
    },
  });

  grunt.registerTask('dev', ['browserify:build']);
  grunt.registerTask('default', ['dev']);
}
