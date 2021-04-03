
$(function () {
    $('#demo1').on('shown.bs.collapse', function (e) {
            $('html,body').animate({
                scrollTop: $('#demo1').offset().top -145
            }, 1000); 
    }); 
});

