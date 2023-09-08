$(document).ready(function () {
    if (localStorage.getItem("id") === null) {
        window.location.replace("http://127.0.0.1:8000/login-user");
    }
    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:8000/users/"+ localStorage.getItem('id')+ "/",
        headers: {
            "Authorization": "Bearer " + localStorage.getItem('token')
        },
        dataType: "json",
        encode: true,
        success:  function(data){
            $("#username_id").text(data['name']);
            $("#user_city_id").text(data['city']);
            $("#user_email_id").text(data['email']);
        },
    });
    event.preventDefault();
});

$('#edit_btn_id').click(()=>{
    window.location.replace("http://127.0.0.1:8000/edit-user");
});

$('#logout-btn').click(()=> {
    localStorage.clear();
    window.location.replace("http://127.0.0.1:8000/login-user");




});
