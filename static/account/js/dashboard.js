$('#dashboard, .menu_dashboard a').click(function(){
    window.location.href = 'http://localhost:8000/account/dashboard/'
});


$('a.fillForm').click(function(){
    axios.defaults.headers.common['Authorization'] = 'Token ' + localStorage.getItem('token');
    axios.get('http://localhost:8000/account/auth-user/').then(r => {
         const user = r.data;
         $(this).off('click');
         $('div.box').show();
         $('#id_username').val(user.username);
         $('#id_password').attr('type', 'text').val('Please confirm your password');
         $('#id_email').val(user.email);
         $('#id_first_name').val(user.first_name);
         $('#id_last_name').val(user.last_name);
     })
        .catch(r => alert("Your profile can't be updated!"));

     axios.get('http://localhost:8000/account/auth-user-profile/').then(r => {
         const user_profile = r.data[0];
         $('#birth_date').val(user_profile.birth_date);
         $('#address').val(user_profile.address);
         if (user_profile.photo)
            $('img.photo').attr('src', user_profile.photo);
         else
             $('img.photo').attr('src', '/static/account/img/no-photo.png')
                           .css({ 'height': '85px', 'width': '85px' })
     });

});

$('#id_password').keyup(function(){
   $(this).attr('type', 'password');
});