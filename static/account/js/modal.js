$('#btn').click(function(){
    $('#modal').fadeOut('slow');
});

$('#btn_modal_order').click(function () {
   $('#modal_order').fadeOut('slow');
});

$('#btn_modal_payment').click(function () {
   $('#modal_payment').fadeOut('slow');
});

$(document).keyup(function(e){
    if (e.which === 27){
        $('#btn').click();
        $('#btn_modal_order').click();
        $('#btn_modal_payment').click();

    }
});

$('a.delete').click(function(){
    $('article').fadeOut('slow');
});

