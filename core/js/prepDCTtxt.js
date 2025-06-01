 function prepDCTtxt(txt) {
  txt = txt.replaceAll(/(?:\r\n|\r|\n)+/gi, '\n\n');
  txt = txt.replaceAll(/dct:([a-zA-Z][a-zA-Z0-9_]*)/gi, "<a href='/$1'>$1</a>");
  txt = marked.parse(txt);
  return txt;
}