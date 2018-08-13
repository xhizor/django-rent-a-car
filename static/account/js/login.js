$('input').keyup(function(e){
     if (e.keyCode === 13)
         $('#btnLogin').click();
});

$('#btnLogin').click(function() {
    $("#errorMessage").hide();

    const username = $('input:text');
    const password = $('input:password');

    if (!username.val()) {
        username.css({'border-color': 'red'});
        return false;
    }
    else username.css({'border-color': ''});

    if (!password.val()) {
        password.css({'border-color': 'red'});
        return false;
    }
    else password.css({'border-color': ''});

    const payload = {'username': username.val(),
                     'password': password.val()};
    const baseUrl = 'http://localhost:8000/account/';

    axios
        .post(baseUrl + 'auth/token/', payload)
        .then(r => {
            localStorage.setItem('token', r.data.token);
            axios.defaults.headers.common['Authorization'] = 'Token '
                + localStorage.getItem('token');
            axios
                .get(baseUrl + 'dashboard/')
                .then(r => r.data);
                window.location.href = baseUrl + 'dashboard/';
        })
        .catch(r => $("#errorMessage").show())
});

