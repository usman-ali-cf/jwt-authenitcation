function ValidateEmail(input) {

  var validRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
  if (input.value.match(validRegex)) {
    $("#user_email_id").focus();
    $('#user_email_id').focus(function(){
        $(this).css('border-color','red');
    });
    return true;
  }
  else {
    $("user_email_id").focus();
    $('#user_email_id').focus(function(){
        $(this).css('border-color','green');
    });
    return false;
  }
}
