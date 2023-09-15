function validateForm() {
    var isValid = true;
    $('.form').each(function() {
      if ( $(this).val() === '' )
          isValid = false;
    });
    return isValid;
  }

$(function () {
    $('.submit').click(function () {
        var isValid = true;
        isValid = validateForm();
       if(isValid == true){
            $('.main-container').css('visibility', 'hidden');
            $('.loader').css('visibility', 'visible');
       }
    });
});