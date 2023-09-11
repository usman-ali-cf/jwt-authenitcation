$(document).ready(function () {
    $("#register_id").click(function (event) {
        var role_id = 3;
        if($('#role_id').val()=="admin"){
            role_id = 1;
        }
        var formData = {
            name: $('#name_id').val(),
            email: $("#email_id").val(),
            password: $("#password_id").val(),
            gender:  $('#gender_id').val(),
            city:  $('#city_id').val(),
            role:  role_id,
        };
        $.ajax({
            type: "POST",
            url: "http://127.0.0.1:8000/user/register",
            data: formData,
            dataType: "json",
            encode: true,
            success:  function(){
                window.location.replace("http://127.0.0.1:8000/login-user");
            },
            error: function(xhr, status, error) {
                $('#message').text("Invalid Data Entered, Please Try again with correct data!!")
            }
        });
        event.preventDefault();
    });
});
