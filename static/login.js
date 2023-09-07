$(document).ready(function () {
    $("#login_id").click(function (event) {
        var formData = {
            email: $("#email_id").val(),
            password: $("#password_id").val(),
        };
        $.ajax({
            type: "POST",
            url: "http://127.0.0.1:8000/user/login/",
            data: formData,
            dataType: "json",
            encode: true,
            success:  function(data){
                $.ajax({
                    type: "GET",
                    url: "http://127.0.0.1:8000/users/",
                    dataType: "json",
                    encode: true,
                    headers: {
                        "Authorization": "Bearer " + data['access']
                    },
                    success: (user_list)=>{
                        user_list.forEach(setID);
                        function setID(value, index, array) {
                            if(value['email']==formData['email']){
                                localStorage.setItem("id", value['id']);
                            }
                        }
                    }
                });
                localStorage.setItem("token", data['access']);
                window.location.replace("http://127.0.0.1:8000");
            }
        });
        event.preventDefault();
    });
});
