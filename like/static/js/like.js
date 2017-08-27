/**
 * Created by user on 2017/5/6.
 */

$('body').on('click', '.like-Unlike', function(e) {
    e.preventDefault(); //don't use return false; has nothing to do with the issue though
    if (is_authenticated){
        console.log('yes! logged in ')
    }
    else{
        console.log('no ! logged out ')

        $('[data-toggle="tooltip"]').tooltip('show');
        // window.open("/login/","_self");
        return;

    }

    var elm = $(this); //cache the element

    id = elm.closest('.pin').attr('data-id')


    heart = elm.children()

    if (heart.hasClass('like')) {
        $.get("/pins/unlike/"+id , function(data){
        json = data;
        console.log(json);
        });
    }

    if (heart.hasClass('unlike')) {
        $.get("/pins/like/"+id , function(data){
        json = data;
        console.log(json);
        });
    }
    heart.toggleClass('like');
    heart.toggleClass('unlike');
});

/*
this helper is for rendering "like" buttons as "unlike" when page is loaded
*/



Handlebars.registerHelper("is_it_in_list", function(id){
    // data = getVotedPin();
    if (typeof data !== 'undefined') {
    }
    else{
        data = getVotedPin();
    }


    if( data.voted_pins.indexOf(id) == -1 ){
        return new Handlebars.SafeString("<span class='unlike'></span>");
    }
    else {
        return new Handlebars.SafeString("<span class='like'></span>");
    }

});

/*
getVotedPin returns current user's voted pins as an object.
it's a helper to previous function.
*/
function getVotedPin(  )
{
     var result = null;
     var apiUrl = "/pins/voted_pins";
     $.ajax({
        url: apiUrl,
        type: 'get',
        dataType: 'html',
        async: false,
        success: function(data) {
            result = JSON.parse(data);
        }
     });
     return result;
}

