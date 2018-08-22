$('#rent-a-car').click(function () {
   $('#modal').show();
   $('#price, #total_price').text($('#car_price').text());

});

$('#end_date').blur(function () {
    $(this).css('border-color', '');
    const price_per_hour = parseInt($('#price').text());
    const end_date = new Date($(this).val());
    const now = new Date();
    let diff = Math.round(end_date.getTime() - now.getTime()) / 1000;
    diff /= 60 * 60;
    const total_hours = Math.abs(Math.round(diff));
    const total_price = price_per_hour * total_hours;
    $('#total_price').text((!total_price || total_price === undefined) ? price_per_hour : total_price);
});

$('#proceed_order').click(function () {
    const end_date = $('#end_date');
    if (confirm('Are you sure you want to rent this car?')){
         if (!end_date.val()) {
            end_date.css('border-color', 'red');
            return false;
        }
        axios.defaults.headers.common['Authorization'] = 'Token '
                    + localStorage.getItem('token');
        const pk = window.location.pathname.split('/')[2];

        const data = {'end_date': end_date.val().toString(),
                      'total_price': $('#total_price').text(),
                      'pk': pk};
        const url = 'http://localhost:8000/order/create/';
        axios
            .post(url, data)
            .then(r => window.location.href = 'http://localhost:8000/account/dashboard/')
            .catch(r => {
                $('#modal').hide();
                $('#modal_error').show();
            });
}
});