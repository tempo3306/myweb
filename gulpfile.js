var gulp        = require('gulp');
var browserSync = require('browser-sync');
var reload      = browserSync.reload;

gulp.task('default', function() {
    browserSync.init({
        notify: false,
        proxy: "localhost:8000"
    });
    gulp.watch(['./**/*.{scss,css,html,py,js}'], reload);
});
