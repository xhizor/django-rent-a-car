$(function(){
    $('#btn').click(function(){
            $("#modal").fadeOut('slow');
            $("#modal_car").fadeOut('slow');
        });

        $(document).keyup(function(e){
            if (e.which === 27){
                $('#btn').click();
                $('#btn_modal_car').click();
            }
        });

        $('a.delete').click(function(){
            $('article').fadeOut('slow');
        });

});