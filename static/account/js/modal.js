$(function(){
    $('#btn').click(function(){
            $("#modal #modal_error").fadeOut('slow');
        });

        $(document).keyup(function(e){
            if (e.which === 27)
                $('#btn').click();
        });

        $('a.delete').click(function(){
            $('article').fadeOut('slow');
        });

});