function cancel_order(pk) {
    if (confirm('Are you sure you want to cancel the order?')) {
        axios.defaults.headers.common['Authorization'] = 'Token '
            + localStorage.getItem('token');
        const url = 'http://localhost:8000/order/' + pk + '/cancel/';
        axios
            .put(url)
            .then(r => {
                if (r.data.canceled)
                    $('span').text('Canceled');
                    $('a.delete').hide();

            });
    }
}

function get_orders(url, status){
    axios.defaults.headers.common['Authorization'] = 'Token '
            + localStorage.getItem('token');
    axios
            .get(url)
            .then(r => {
                $('a.fillForm').hide();
                $('#order_data').hide();
                $('#rows').html('');
                const orders = r.data;
                let rows = '';
                if (Object.keys(orders).length) {
                    $.each(orders, function (key, val) {
                        rows += '<tr><td>' + val.id + '</td><td>' +
                            val.car.model.name + ' ' + val.car.name + '</td><td>' +
                            val.total_price + '</td><td>' + val.start_date + '</td><td>' +
                            val.end_date + '</td><td>';
                            if (status === 'pending'){
                                rows += '<span class="tag is-danger">Pending</span></td><td><a href="#" class="delete"' +
                                        'onclick="cancel_order(' + val.id + ');">Cancel</a></td>';
                                        $('#th_cancel').show();
                                }
                            else if (status === 'active')
                                rows += '<span class="tag is-link">Active</span></td>';
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

$('#finished_orders').click(function () {
        const url = 'http://localhost:8000/order/get-orders/?finished=True';
        get_orders(url, 'finished');

});

