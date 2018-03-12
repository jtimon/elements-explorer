const gulp = require('gulp');
const sass = require('gulp-sass');

gulp.task('build-css', () => (
  gulp.src('src/scss/**/*.scss')
    .pipe(sass())
    .pipe(gulp.dest('public/css'))
));

gulp.task('watch', () => (
  gulp.watch('src/scss/**/*.scss', ['build-css'])
));
