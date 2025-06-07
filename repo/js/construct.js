document.addEventListener("DOMContentLoaded", () => {
  
  var urlParams = new URLSearchParams(window.location.search);
  var ucid = urlParams.get('ucid');
  
  document.getElementById(ucid+"_view").style.display = "block";
  
  // var htmlCollection_Def = document.getElementsByClassName('construct-definition-box');
  // var htmlCollection_mDev = document.getElementsByClassName('measure-dev-box');
  // var htmlCollection_mCode = document.getElementsByClassName('measure-code-box');
  // var htmlCollection_aDev = document.getElementsByClassName('aspect-dev-box');
  // var htmlCollection_aCode = document.getElementsByClassName('aspect-code-box');
  // 
  // for (let i = 0; i < htmlCollection_Def.length; i++) {
  //   htmlCollection_Def[i].innerHTML =
  //     htmlCollection_Def[i].innerHTML.replace(/dct:([a-zA-Z][a-zA-Z0-9_]*)/i, "<a href='https://psycore.one/$1'>$1</a>");
  // }
  //
  // for (let i = 0; i < htmlCollection_mDev.length; i++) {
  //   htmlCollection_mDev[i].innerHTML =
  //     htmlCollection_mDev[i].innerHTML.replace(/dct:([a-zA-Z][a-zA-Z0-9_]*)/i, "<a href='https://psycore.one/$1'>$1</a>");
  // }
  //
  // for (let i = 0; i < htmlCollection_mCode.length; i++) {
  //   htmlCollection_mCode[i].innerHTML =
  //     htmlCollection_mCode[i].innerHTML.replace(/dct:([a-zA-Z][a-zA-Z0-9_]*)/i, "<a href='https://psycore.one/$1'>$1</a>");
  // }
  //
  // for (let i = 0; i < htmlCollection_aDev.length; i++) {
  //   htmlCollection_aDev[i].innerHTML =
  //     htmlCollection_aDev[i].innerHTML.replace(/dct:([a-zA-Z][a-zA-Z0-9_]*)/i, "<a href='https://psycore.one/$1'>$1</a>");
  // }
  //
  // for (let i = 0; i < htmlCollection_aCode.length; i++) {
  //   htmlCollection_aCode[i].innerHTML =
  //     htmlCollection_aCode[i].innerHTML.replace(/dct:([a-zA-Z][a-zA-Z0-9_]*)/i, "<a href='https://psycore.one/$1'>$1</a>");
  // }
  //

});
