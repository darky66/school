$(document).ready(function(){
    
    // --- РЕГИСТРАЦИЯ ---
    $('#67').on('submit',function(e){
        e.preventDefault();
        
        if ($('#fullname').val().trim() === '' || $('#password').val().trim() === '' || $('#password').val().trim() != $('#confirm_password').val().trim()){
            alert('Заполните все поля и убедитесь, что пароли совпадают!');
            return; 
        }
        
        $.ajax({
            url: '/user_register',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                name: $('#fullname').val(),
                password: $('#password').val(),
                email: $('#email').val()
            }),
            success: function(response) {
                alert(response.message);
                if(response.success) {
                    window.location.href = '/login'; 
                }
            },
            error: function(xhr) {
                let msg = xhr.responseJSON ? xhr.responseJSON.message : 'Неизвестная ошибка';
                alert('Ошибка: ' + msg);
            }
        });
    });

    // --- АВТОРИЗАЦИЯ ---
    $('#52').on('submit',function(e){
        e.preventDefault();
        $.ajax({
            url: '/user_login',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                password: $('#password').val(),
                email: $('#username').val()
            }),
            success: function(response) {
                if(response.success) {
                    window.location.href = '/profile'; 
                }
            },
            error: function(xhr) {
                let msg = xhr.responseJSON ? xhr.responseJSON.message : 'Неизвестная ошибка';
                alert('Ошибка входа: ' + msg);
            }
        });
    });

});