var gulp = require('gulp');
var sass = require('gulp-sass');
var cleanCSS = require('gulp-clean-css');
var rename = require("gulp-rename");
var uglify = require('gulp-uglify');
var eslint = require('gulp-eslint')
var nodemon = require('gulp-nodemon');
var run = require('gulp-run');
var browserSync = require('browser-sync');

//Config for development purposes
const port = 5000;
const node_env = 'development';

const jsFiles = ['*.js', '**/*.js', '!node_modules/**', '!public/vendor/**'];
const nodemonFiles = ['*.js', '**/*.js', 'views/*.handlebars', '!node_modules/**', '!public/vendor/**'];

//Check for linting issues that developer might have missed
gulp.task('lint', function(){
    return gulp.src(jsFiles)
        .pipe(eslint({"config": ".eslintrc.json"}))
        .pipe(eslint.format())
        .pipe(eslint.failAfterError());
});

//Serve the application & restart it when javascript files get changed
gulp.task('nodemon', ['lint'], function(){

    var options = {
        script: 'bin/www',
        delayTime: 1,
        env: {
            'PORT': port,
            'NODE_ENV': node_env
        },
        watch: nodemonFiles
    };

    return nodemon(options)
        .on('restart', function(ev){
            console.log('Restarting...');
            browserSync.reload;
            console.log(ev);
        });
});

// Static files: Compiles SCSS files from /scss into /css
gulp.task('sass', function() {
    return gulp.src('./public/scss/beverageRandomizer.scss')
      .pipe(sass())
      .pipe(gulp.dest('./public/css'))
      .pipe(browserSync.reload({
        stream: true
      }));
  });

// Minify compiled CSS
gulp.task('minify-css', ['sass'], function() {
    return gulp.src('./public/css/beverageRandomizer.css')
      .pipe(cleanCSS({
        compatibility: 'ie8'
      }))
      .pipe(rename({
        suffix: '.min'
      }))
      .pipe(gulp.dest('./public/css'))
      .pipe(browserSync.reload({
        stream: true
      }))
  });

// Minify custom JS
gulp.task('minify-js', function() {
    return gulp.src('./public/js/beverageRandomizer.js')
      .pipe(uglify())
    .pipe(rename({
      suffix: '.min'
    }))
    .pipe(gulp.dest('./public/js'))
    .pipe(browserSync.reload({
        stream: true
    }));
});


//Start a browser-sync proxy so that development changes can be seen in browser
gulp.task('browser-sync', ['nodemon'], function(){
    browserSync.init({
        proxy: 'http://localhost:' + port,
    });
});

gulp.task('serve', ['browser-sync'], function(){
    gulp.watch('./public/scss/*.scss', ['sass']);
    gulp.watch('./public/css/*.css', ['minify-css']);
    gulp.watch('./public/js/*.js', ['minify-js']);
    // Reloading browserSync whenever the hbs or js files change
    gulp.watch(['./views/*.hbs', './public/js/*.js'], browserSync.reload);
});