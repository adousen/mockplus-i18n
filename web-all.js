var lang = require('./langs/allapi.json');

var toString = Object.prototype.toString;


function outputAll(obj, prefix) {
  var k;
  for (k in obj) {
    var v = obj[k];
    if (!obj.hasOwnProperty(k)) {
      continue
    }
    if (toString.call(v) === '[object String]') {
      if (prefix) {
        console.log(prefix + '.' + k + ' = "' + obj[k].replace('\n', 'osrpt') + '"');
      } else {
        console.log(k + ' = "' + obj[k].replace('\n', 'osrpt') + '"');
      }
    } else {
      if (prefix) {
        outputAll(v, prefix + '.' + k);
      } else {
        outputAll(v, k);
      }
    }
  }
}

outputAll(lang, '');
