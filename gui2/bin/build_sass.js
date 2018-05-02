const colors = require('colors/safe');
const fs = require('fs');
const getDirName = require('path').dirname;
const mkdirp = require('mkdirp');
const sass = require('node-sass');
const watch = require('node-watch');

const mode = process.argv[2];

const files = [
  {
    src: 'src/scss/styles.scss',
    dest: 'public/css/styles.css',
  },
];

function printCompiling(fileName) {
  console.log(`Compiling ${fileName}...`);
}

function printCompiled(fileName) {
  console.log(colors.green(fileName));
  console.log(colors.green('Done!'));
  console.log('');
}

function printError(fileName, err) {
  console.log(colors.red(fileName));
  console.error(colors.red('Build error:'));
  console.error(err);
  console.log('');
  if (mode === 'build') {
    process.exit(1);
  }
}

function buildSass() {
  function writeFile(css, options) {
    mkdirp(getDirName(options.dest), () => {
      fs.writeFile(options.dest, css, (err) => {
        if (err) {
          printError(options.dest, err);
        } else {
          printCompiled(options.dest);
        }
      });
    });
  }

  function compileSass(paramOptions = {}) {
    const options = Object.assign({
      style: 'expanded',
    }, paramOptions);

    printCompiling(options.src);
    sass.render({
      file: options.src,
      outputStyle: options.style,
    }, (err, result) => {
      if (err) {
        printError(options.src, err);
      } else {
        writeFile(result.css, options);
      }
    });
  }

  files
    .filter(file => file.src.includes('.scss'))
    .forEach(compileSass);

  if (mode === 'watch') {
    watch('src', {
      recursive: true,
    }, (evt, name) => {
      if (name.includes('.scss')) {
        files
          .filter(file => file.src.includes('.scss'))
          .forEach(compileSass);
      }
    });
  }
}

buildSass();
