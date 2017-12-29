'use strict';
var fs = require('fs');
var lang = require('./langs/web.json');
var toString = Object.prototype.toString;

function read_all_not_in_use(cb) {
  fs.readFile('./temp/not_in_use.log', {
    encoding: 'utf8',
    flag: 'r'
  }, function (err, content) {
    if (err) {
      return cb(err);
    }
    var lines = content.split('\n');
    cb(null, lines);
  })
}

function walk(obj, prefix, notInUse) {
  var k;
  var key_in_str = '';
  for (k in obj) {
    var v = obj[k];
    if (!obj.hasOwnProperty(k)) {
      continue
    }
    if (toString.call(v) === '[object String]') {
      if (prefix) {
        key_in_str = prefix + '.' + k;
      } else {
        key_in_str = k;
      }
      if (notInUse.indexOf(key_in_str) > -1) {
        delete obj[k]
      }
    } else {
      if (prefix) {
        walk(v, prefix + '.' + k, notInUse);
      } else {
        walk(v, k, notInUse);
      }
    }
  }
}

function clear() {

}

read_all_not_in_use(function (err, notInUse) {
  if (err) {
    console.error(err);
    process.exit(1);
  }
  walk(lang, '', notInUse)
  console.log(JSON.stringify(lang, null, 2));
});
