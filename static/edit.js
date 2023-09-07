
$(document).ready(function () {
    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:8000/users/"+ localStorage.getItem('id')+ "/",
        headers: {
            "Authorization": "Bearer " + localStorage.getItem('token')
        },
        dataType: "json",
        encode: true,
        success:  function(data){
            console.log(data['name']);
            $("#data").text(data['name']);
            $("#username_id").val(data['name']);
            $("#user_city_id").val(data['city']);
            $("#user_email_id").val(data['email']);
        }
    });
    event.preventDefault();
});

$('#edit_btn_id').click(()=>{
    var formData = {
        name: $("#username_id").val(),
        city: $("#user_city_id").val(),
        email: $("#user_email_id").val(),
        password: $("#user_password_id").val()
    };
    $.ajax({
        type: "PATCH",
        url: "http://127.0.0.1:8000/users/" + localStorage.getItem('id') + "/",
        data: formData,
        dataType: "json",
        encode: true,
        headers: {
            "Authorization": "Bearer " + localStorage.getItem('token')
        },
        success: () => {
            window.location.replace("http://127.0.0.1:8000");
        },
        error: function(xhr, status, error) {
            console.log(xhr.responseText);
        }
    });
});
