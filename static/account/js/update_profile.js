$("#update").click(function(){
    const data = {
        'username': $('#id_username').val(),
        'email': $('#id_email').val(),
        'password': $('#id_password').val(),
        'first_name': $('#id_first_name').val(),
        'last_name': $('#id_last_name').val(),
        'user_profile.birth_date': $('#birth_date').val(),
        'user_profile.address': $('#address').val(),
        'user_profile.photo': $('#photo').val()
    };
    axios.defaults.headers.common['Authorization'] = 'Token '
        + localStorage.getItem('token');
    axios
        .patch('http://localhost:8000/account/dashboard/update/', data)
        .then(r => location.reload())
        .catch (r => alert(r));
});
