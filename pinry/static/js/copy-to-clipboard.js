/**
 * Created by user on 2017/6/22.
 */


//usage:
//create an input with id as 'copy-content'
//create a button with onclick as 'copyToClipboard()'

function copyToClipboard() {

var $input = $('#copy-content');
result= $input.val();
$input.val(result);
if (navigator.userAgent.match(/ipad|ipod|iphone/i)) {
  var el = $input.get(0);
  var editable = el.contentEditable;
  var readOnly = el.readOnly;
  el.contentEditable = true;
  el.readOnly = false;
  var range = document.createRange();
  range.selectNodeContents(el);
  var sel = window.getSelection();
  sel.removeAllRanges();
  sel.addRange(range);
  el.setSelectionRange(0, 999999);
  el.contentEditable = editable;
  el.readOnly = readOnly;
} else {
  $input.select();
}
document.execCommand('copy');
$input.blur();
}