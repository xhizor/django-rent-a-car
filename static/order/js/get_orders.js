function cancel_order(pk) {
    if (confirm('Are you sure you want to cancel the order?')) {
        axios.defaults.headers.common['Authorization'] = 'Token '
            + localStorage.getItem('token');
        const url = 'http://localhost:8000/order/' + pk + '/cancel/';
        axios
            .put(url)
            .then(r => {
                location.reload();
            });
    }
}


function get_orders(url, status){
    axios.defaults.headers.common['Authorization'] = 'Token '
            + localStorage.getItem('token');
    axios
            .get(url)
            .then(r => {
                $('#not_found').hide();
                $('a.fillForm').hide();
                $('#order_data').hide();
                $('#rows').html('');
                const orders = r.data;
                let rows = '';
                if (Object.keys(orders).length) {
                    $.each(orders, function (key, val) {
                        rows += '<tr><td>' + val.id + '</td><td>' +
                            val.car.model.name + ' ' + val.car.name + '</td><td>$<span id="total_price">' +
                            val.total_price + '</span></td><td>' + val.start_date + '</td><td>' +
                            val.end_date + '</td><td>';
                            if (status === 'pending'){
                                rows += '<span class="tag is-danger">Pending</span></td><td><a href="#" class="delete"' +
                                        'onclick="cancel_order(' + val.id + ');">Cancel</a></td>';
                                        $('#th_cancel').show();
                                }
                            else if (status === 'active') {
                                if (val.approved && val.paid) {
                                    $('#th_payment').hide();
                                    rows += '<span class="tag is-success"> Paid </span>';
                                }
                                else {
                                    $('#order_pk').val(val.id);
                                    $('#th_payment').show();
                                    rows += '<span class="tag is-link" id="td_active">Active</span></td><td><a href="#" ' +
                                        'onclick="$(\'#modal_payment\').show(\'slow\');" id="td_payment">' +
                                        '<span class="tag is-success">Pay via Card</span></a></td>';
                                }
                            }
                            else if (status === 'canceled')
                                rows += '<span class="tag is-danger">Canceled</span></td>';
                            else
                                rows += '<span class="tag is-success">Finished</span></td>';
                        rows += '</tr>';

                    });

                    $('#order_data').show();
                    $('#rows').append(rows);
                }
                else
                    $('#not_found').show();
            });

}

$('#pending_orders').click(function () {
        const url = 'http://localhost:8000/order/get-orders/';
        get_orders(url, 'pending');

});

$('#active_orders').click(function () {
        const url = 'http://localhost:8000/order/get-orders/?active=True';
        get_orders(url, 'active');

});

$('#canceled_orders').click(function () {
        const url = 'http://localhost:8000/order/get-orders/?canceled=True';
        get_orders(url, 'canceled');

});

$('#finished_orders').click(function () {
        const url = 'http://localhost:8000/order/get-orders/?finished=True';
        get_orders(url, 'finished');

});


$('#checkout').click(function () {
    $('#payment_error').hide();
    const card = {
        name: $('#card_name').val(),
        number: $('#card_number').val(),
        exp_month: $('#expiry_month').val(),
        exp_year: $('#expiry_year').val(),
        cvc: $('#cvv').val()
    };

    Stripe.createToken(card, function(status, r){
        if (status === 200){
            const pk = $('#order_pk').val();
            const url = 'http://localhost:8000/order/' + pk + '/payment/';
            const data = {
                'stripe_id': r.id,
                'total_price': $('#total_price').text()
            };
            axios
                .post(url, data)
                .then(r => {
                    $('#modal_payment').hide();
                    $('#modal_order_complete').show();
                })
        }
        else
            $('#payment_error').show('slow');
    });

});
