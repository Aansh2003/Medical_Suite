
$(function () {
    $('.dot1').hover(function () {
        $('.dot2').css('left', '32vw');
        $('.dot2').css('top', '20vw');
        $('.dot2').css('transition-timing-function', 'ease-in-out');
        $('.dot2').css('transition-duration', '0.5s');
        $('.dot3').css('top', '30vw');
        $('.dot3').css('left', '17vw');
        $('.dot3').css('transition-timing-function', 'ease-in-out');
        $('.dot3').css('transition-duration', '0.5s');
    }, function () {
        $('.dot2').css('left', '29vw');
        $('.dot2').css('top', '18vw');
        $('.dot2').css('transition-timing-function', 'linear');
        $('.dot2').css('transition-duration', '0.7s');
        $('.dot3').css('top', '27vw');
        $('.dot3').css('left', '18vw');
        $('.dot3').css('transition-timing-function', 'linear');
        $('.dot3').css('transition-duration', '0.7s');
    });
    $('.dot2').hover(function () {
        $('.dot1').css('left', '14vw');
        $('.dot1').css('top', '11vw');
        $('.dot1').css('transition-timing-function', 'ease-in-out');
        $('.dot1').css('transition-duration', '0.5s');
        $('.dot3').css('top', '30vw');
        $('.dot3').css('left', '14vw');
        $('.dot3').css('transition-timing-function', 'ease-in-out');
        $('.dot3').css('transition-duration', '0.5s');
    }, function () {
        $('.dot1').css('left', '18vw');
        $('.dot1').css('top', '14vw');
        $('.dot1').css('transition-timing-function', 'linear');
        $('.dot1').css('transition-duration', '0.7s');
        $('.dot3').css('top', '27vw');
        $('.dot3').css('left', '18vw');
        $('.dot3').css('transition-timing-function', 'linear');
        $('.dot3').css('transition-duration', '0.7s');
    });

    $('.dot3').hover(function () {
        $('.dot1').css('left', '17vw');
        $('.dot1').css('top', '11vw');
        $('.dot1').css('transition-timing-function', 'ease-in-out');
        $('.dot1').css('transition-duration', '0.5s');
        $('.dot2').css('top', '16vw');
        $('.dot2').css('left', '32vw');
        $('.dot2').css('transition-timing-function', 'ease-in-out');
        $('.dot2').css('transition-duration', '0.5s');
    }, function () {
        $('.dot1').css('left', '18vw');
        $('.dot1').css('top', '14vw');
        $('.dot1').css('transition-timing-function', 'linear');
        $('.dot1').css('transition-duration', '0.7s');
        $('.dot2').css('top', '18vw');
        $('.dot2').css('left', '29vw');
        $('.dot2').css('transition-timing-function', 'linear');
        $('.dot2').css('transition-duration', '0.7s');
    });
});