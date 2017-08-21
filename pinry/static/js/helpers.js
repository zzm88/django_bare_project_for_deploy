/**
 * Helpers for Pinry
 * Descrip: A hodgepodge of useful things to help clean up Pinry's JavaScript.
 * Authors: Pinry Contributors
 * Updated: Feb 26th, 2013
 * Require: jQuery
 */


function renderTemplate(templateId, context) {
    var template = Handlebars.compile($(templateId).html());
    return template(context);
}


function cleanTags(tags) {
    if (typeof tags === 'string' && tags.length > 0) {
        tags = tags.split(/[\s,]+/);
        for (var i in tags) {
            tags[i] = tags[i].trim();
        }
    } else {
        return [];
    }
    return tags;
}


function getImageData(imageId) {
    var apiUrl = '/api/v1/image/'+imageId+'/?format=json';
    return $.get(apiUrl);
}


function getPinData(pinId) {
    var apiUrl = '/api/v1/pin/'+pinId+'/?format=json';
    return $.get(apiUrl);
}


function deletePinData(pinId) {
    var apiUrl = '/api/v1/pin/'+pinId+'/?format=json';
    return $.ajax(apiUrl, {
        type: 'DELETE'
    });
}

function postPinData(data) {
    return $.ajax({
        type: "post",
        url: "/api/v1/pin/",
        contentType: 'application/json',
        data: JSON.stringify(data)
    });
}


function getUrlParameter(name) {
    return decodeURIComponent((new RegExp('[?|&]' + name + '=' + '([^&;]+?)(&|#|;|$)').exec(location.search)||[,""])[1].replace(/\+/g, '%20'))||null;
}


Handlebars.registerHelper('niceLinks', (function () {
    var reNL = /\r?\n/g,
        reURL = /https?:[/][/](?:www[.])?([^/]+)(?:[/]([.]?[^\s,.])+)?/g;
    return function (text) {
        var t = Handlebars.Utils.escapeExpression(text);
        t = t.replace(reURL, '<a href="$&" target="_blank">$1</a>');
        t = t.replace(reNL, '<br>');
        return new Handlebars.SafeString(t);
    };
})());

//writing my own helper
// $(document).ready(function() {
//
Handlebars.registerHelper('isWechat', function(val, options) {
    var fnTrue = options.fn,
        fnFalse = options.inverse;

    return (navigator.userAgent.toLowerCase().includes('micromessenger'))? fnTrue(this) : fnFalse(this);
});
    // Handlebars.registerHelper('isWeixin', function(block) {
    //     // var is_weixin = (navigator.userAgent.includes('MicroMessenger')) ? true :  false;
    //         if (navigator.userAgent.includes('MicroMessenger')) {
    //             return block(this);
    //         } else {
    //             return block.inverse(this);
    //         }
    // });
// });
// Handlebars.registerHelper('user_agent', function() {
//     var ua_str = navigator.userAgent.toLowerCase();
//     return ua_str; //just return global variable value
// });
//
// //end of writing my own writer




function postTbkURL(data) {
    var tbk_url = $('#pin-form-purchase-link').val();
    var description = $('#pin-form-description').val();
    return $.ajax({
        url: "/gettkl/",
        type: "post", //send it through get method
        data: {
            'tbk_url': tbk_url,
            'description':description
        },
        success: function(response) {
            $('#pin-form-tao-kouling').val(response.model);
        },


    });
}

function showImages(){
    var img_urls = $(event.target).attr('data-images');
    $.ajax({
      url: "/view_images/",
      type: "post", //send it through get method
      data: {
        'img_urls':img_urls
      },
      success: function(response) {
          img_urls =response.img_urls;
          $('.other-images').html('');
          for (var key in img_urls ) {
            $('.other-images').append("<img style='width:50%' src=" + img_urls[key] + ">");

          }
          $('#modal-container-848864').modal('show');
          console.log(response);


      },

    });

}



