if ($("#phonenum").html()) {
    console.log("true");
    
}



if (response.responseText.includes('msg')) {
    $('#validcode').html(response.responseJSON['msg']);
    $('#btn_getsms').attr('disabled',false); 


  } else {
    $('#validcode').html("try again");

  }

  function functionNAME() {
          $.ajax({
              url:'url/address', //+ some_argument,
              beforeSend: function() {
                  $("#tagid").html('infomation');
              },
              complete: function (response) {
                  $("#tagid").html('infomation');
                  //response.responseText
                  //response.responseJSON
                 //or 
                  //response.responseJSON['key'] 
              },
              error: function () {
                  $('#tagid').html('infomation');
              },
          });
          return false;
      }
  
  
  <button onclick="return functionNAME();" type="button" class="btn btn-success">get_ajax_data</button>
  <span id="tagid" class="badge badge-default">to be rendered</span>
  