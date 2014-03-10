$(document).ready(function(){
    $('p').fadeTo(1000,1);
    var node = '';
    if (document.URL.indexOf('about') !== -1)
        node = '#nav1';
    if (document.URL.indexOf('family') !== -1)
        node = '#nav2';
    if (document.URL.indexOf('projects') !== -1)
        node = '#nav3';
    var $n = $(node);
    $($n).effect('shake',{ times:2, distance: 5});
});
