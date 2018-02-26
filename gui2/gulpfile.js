var gulp   = require('gulp'),
    sass   = require('gulp-sass');

gulp.task('build-css', function() {
  return gulp.src('src/scss/**/*.scss')
    .pipe(sass())
    .pipe(gulp.dest('public/css'));
});

gulp.task('watch', function() {
  gulp.watch('src/scss/**/*.scss', ['build-css']);
});
