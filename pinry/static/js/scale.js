/**
 * Created by user on 2017/6/4.
 */
var pageWidth, pageHeight;

var basePage = {
  width: 480,
  height: 600,
  scale: 1,
  scaleX: 1,
  scaleY: 1
};

// var isMobile = window.matchMedia("only screen and (max-width: 760px)");

$(function(){
  if (!isMobile) {
    return;
  }
  var $page = $('.page_content');

  getPageSize();
  scalePages($page, pageWidth, pageHeight);

  //using underscore to delay resize method till finished resizing window
  $(window).resize(_.debounce(function () {
    getPageSize();
    scalePages($page, pageWidth, pageHeight);
  }, 150));


function getPageSize() {
  pageHeight = $('#container').height();
  pageWidth = $('#container').width();
}

function scalePages(page, maxWidth, maxHeight) {

  var scaleX = 1, scaleY = 1;
  scaleX = maxWidth / basePage.width;
  scaleY = maxHeight / basePage.height;
  var k = 1;
  basePage.scaleX = scaleX  ;
  basePage.scaleY = scaleY;
  basePage.scale = (scaleX > scaleY) ? scaleY : scaleX;

  var newLeftPos = Math.abs(Math.floor(((basePage.width * basePage.scale) - maxWidth)/2));
  var newTopPos = Math.abs(Math.floor(((basePage.height * basePage.scale) - maxHeight)/2));

  page.attr('style', '-webkit-transform:scale(' + basePage.scale + ');left:' + newLeftPos + 'px;top:' + newTopPos + 'px;');
}
});