$('#car_rate').click(function () {
    axios.defaults.headers.common['Authorization'] = 'Token '
        + localStorage.getItem('token');
    const pk = $('#order_rate_id').val();
    const data = {'rate': $('#rate').val()};
    const url = 'http://localhost:8000/order/' + pk + '/rate-car/';
    axios
        .put(url, data)
        .then(r => {
            if(r.data.rated)
                alert('You rated the car successfully!');
                location.reload();
        });
});