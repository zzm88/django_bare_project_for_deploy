/**
 * Lightbox for Pinry
 * Descrip: A lightbox plugin for pinry so that I don't have to rely on some of
 *          the massive code bases of other lightboxes, this one uses data
 *          fields to acquire the info we need and dynamically loads comments.
 *          It also has a nice parallax view mode where the top scrolls and the
 *          background stays stationary.
 * Authors: Pinry Contributors
 * Updated: Feb 4th, 2016
 * Require: jQuery, Pinry JavaScript Helpers
 */


$(window).load(function() {
    // Start Helper Functions
    function freezeScroll(freeze) {
        freeze = typeof freeze !== 'undefined' ? freeze : true;


        if (freeze) {
            $('body').data('scroll-level', $(window).scrollTop());
            $('#pins').css({
                // 'position': 'fixed',
                // 'margin-top': -$('body').data('scroll-level')
            });
            // $(window).scrollTop(0);
            /* disable the global pin-loading scroll handler so we don't
               load pins when scrolling a selected image */
            $(window).off('scroll');
        } else {
            $('#pins').css({
                // 'position': 'static',
                // 'margin-top': 0
            });
            $(window).scrollTop($('body').data('scroll-level'));
            /* enable the pin-loading scroll handler unless we've already
               loaded all pins from the server (in which case an element
               with id 'the-end' exists */
            var theEnd = document.getElementById('the-end');
            if (!theEnd) {
                $(window).scroll(scrollHandler);
            }
        }
    }
    // End Helper Functions


    // Start View Functions
    function createBox(context) {
        freezeScroll();
        $('body').append(renderTemplate('#lightbox-template', context));
        var box = $('.lightbox-background');
        // box.css('height', $(document).height());
        var height = Math.max($(document).height(), $(window).height());
        box.css('height', height);


        var img_wrapper_height = ((context.image.standard.width >= $(window).width())) ? context.image.standard.height * $(window).width() /context.image.standard.width : context.image.standard.height;
        img_wrapper_height = (img_wrapper_height> 0.8 * $(window).height) ? img_wrapper_height * 0.8 :  img_wrapper_height;

        $('.lightbox-image-wrapper').css('height', img_wrapper_height);
        box.fadeIn(200);
        $('.lightbox-image').load(function() {
            $(this).fadeIn(200);
        });

        var lightbox_wrapper_width = (context.image.standard.width > $(window).width()) ?  $(window).width(): context.image.standard.width ;
        var lightbox_wrapper_top_offset = ($(window).height()- img_wrapper_height)/2;

        $('.lightbox-wrapper').css({
            'width': lightbox_wrapper_width,
            'margin-top':  $(window).scrollTop()+ lightbox_wrapper_top_offset ,
            'margin-bottom': 80,
            'margin-left': -lightbox_wrapper_width/2
        });
        // if ($('.lightbox-wrapper').height()+140 > $(window).height())
        //     $('.lightbox-background').height($('.lightbox-wrapper').height()+160);

        box.click(function(event) {
            // event.stopPropagation();
            if (event.target.className.includes('btn')) {
                return;
            }
            // alert(event.target.id);
            $(this).fadeOut(200);
            setTimeout(function() {
                box.remove();
            }, 200);
            freezeScroll(false);
        });
    }
    // End View Functions


    // Start Global Init Function
    window.lightbox = function() {
        var links = $('body').find('.lightbox');
        if (pinFilter) {
            var promise = getPinData(pinFilter);
            promise.success(function(pin) {
                createBox(pin);
            });
            promise.error(function() {
                message('Problem problem fetching pin data.', 'alert alert-danger');
            });
        }
        return links.each(function() {
            $(this).off('click');
            $(this).click(function(e) {
                e.preventDefault();
                var promise = getPinData($(this).data('id'));
                promise.success(function(pin) {
                    createBox(pin);
                });
                promise.error(function() {
                    message('Problem problem fetching pin data.', 'alert alert-danger');
                });
            });
        });
    }

    // End Global Init Function
});
