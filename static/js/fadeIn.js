$(document).ready(function(){
    $('p').fadeTo(1000,1);
    /*    
    $('.navOption').mouseenter(function(){
        $(this).fadeTo('slow',0.5);
    });
    $('.navOption').mouseleave(function(){
        $(this).fadeTo('slow',1);
    });
    */
    var $n = $('.navOption');
    $n.click(function(){
        $(this).effect('shake',{direction: 'up', times:1, distance: 4});
    });
});
