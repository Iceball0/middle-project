$(document).ready(function(){

    if (get_cookie('page')) {
        if (get_cookie('page') == 'info') {
            $('#info').css('display', 'block');
            $('#specialties').css('display', 'none');
            $('#universities').css('display', 'none');
            $('#news').css('display', 'none');
            $('#reviews').css('display', 'none');
            $('#location').css('display', 'none');

        } else if (get_cookie('page') == 'specialties') {
            $('#info').css('display', 'none');
            $('#specialties').css('display', 'block');
            $('#news').css('display', 'none');
            $('#reviews').css('display', 'none');
            $('#location').css('display', 'none');

        } else if (get_cookie('page') == 'news') {
            $('#info').css('display', 'none');
            $('#specialties').css('display', 'none');
            $('#news').css('display', 'block');
            $('#reviews').css('display', 'none');
            $('#location').css('display', 'none');

        } else if (get_cookie('page') == 'reviews') {
            $('#info').css('display', 'none');
            $('#specialties').css('display', 'none');
            $('#news').css('display', 'none');
            $('#reviews').css('display', 'block');
            $('#location').css('display', 'none');

        } else if (get_cookie('page') == 'location') {
            $('#info').css('display', 'none');
            $('#specialties').css('display', 'none');
            $('#news').css('display', 'none');
            $('#reviews').css('display', 'block');
            $('#location').css('display', 'none');
        };
    }

    // обрабатываем нажатия на кнопки меню, отображаем нужный блок и прячем остальные
    $(document.getElementsByName('info')[0]).click(function(){
        $('#info').css('display', 'block');
        $('#specialties').css('display', 'none');
        $('#universities').css('display', 'none');
        $('#news').css('display', 'none');
        $('#reviews').css('display', 'none');
        $('#location').css('display', 'none');

        var cookie_date = new Date();
        cookie_date.setHours(cookie_date.getHours() + 1);
        document.cookie = "page=info;expires=" + cookie_date.toUTCString()
    });
    $(document.getElementsByName('specialties')[0]).click(function(){
        $('#info').css('display', 'none');
        $('#specialties').css('display', 'block');
        $('#news').css('display', 'none');
        $('#reviews').css('display', 'none');
        $('#location').css('display', 'none');

        var cookie_date = new Date();
        cookie_date.setHours(cookie_date.getHours() + 1);
        document.cookie = "page=specialties;expires=" + cookie_date.toUTCString()
    });
    $(document.getElementsByName('universities')[0]).click(function(){
        $('#info').css('display', 'none');
        $('#universities').css('display', 'block');
    });
    $(document.getElementsByName('news')[0]).click(function(){
        $('#info').css('display', 'none');
        $('#specialties').css('display', 'none');
        $('#news').css('display', 'block');
        $('#reviews').css('display', 'none');
        $('#location').css('display', 'none');

        var cookie_date = new Date();
        cookie_date.setHours(cookie_date.getHours() + 1);
        document.cookie = "page=news;expires=" + cookie_date.toUTCString()
    });
    $(document.getElementsByName('reviews')[0]).click(function(){
        $('#info').css('display', 'none');
        $('#specialties').css('display', 'none');
        $('#news').css('display', 'none');
        $('#reviews').css('display', 'block');
        $('#location').css('display', 'none');

        var cookie_date = new Date();
        cookie_date.setHours(cookie_date.getHours() + 1);
        document.cookie = "page=reviews;expires=" + cookie_date.toUTCString()
    });
    $(document.getElementsByName('location')[0]).click(function(){
        $('#info').css('display', 'none');
        $('#specialties').css('display', 'none');
        $('#news').css('display', 'none');
        $('#reviews').css('display', 'block');
        $('#location').css('display', 'none');

        var cookie_date = new Date();
        cookie_date.setHours(cookie_date.getHours() + 1);
        document.cookie = "page=location;expires=" + cookie_date.toUTCString()
    });
    $(document.getElementsByName('back')[0]).click(function(){
        window.location.href = '/';
    });

    // функция получения куки

    function get_cookie ( cookie_name )
    {
        var results = document.cookie.match ( '(^|;) ?' + cookie_name + '=([^;]*)(;|$)' );
    
        if ( results )
            return ( unescape ( results[2] ) );
        else
            return null;
    }
});