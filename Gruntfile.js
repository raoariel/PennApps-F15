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

    less: {
      build: {
        files: {
          'pennapps/AI_chat/static/<%= pkg.name %>.css': 'pennapps/AI_chat/src/less/app.less',
        },
      },
    },

    watch: {
      options: {
        interrupt: true,
      },
      less: {
        files: 'pennapps/AI_chat/src/less/**/*',
        tasks: 'less:build',
        options: {
          atBegin: true,
        },
      },
    },

    concurrent: {
      dev: {
        tasks: ['browserify:build', 'watch:less'],
        options: { logConcurrentOutput: true },
      },
    },
  });

  grunt.registerTask('dev', ['concurrent:dev']);
  grunt.registerTask('default', ['dev']);
}
