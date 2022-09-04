$(document).ready(function(){

    function ajax_login(){
        httpRequest = new XMLHttpRequest();
        $.ajax({
            url:'http://127.0.0.1:5000/login', data: $('form').serialize(), type : 'POST', success: function(responseText){
                console.log(responseText)           
                document.getElementById("response").innerHTML = responseText;
            },
            error: function(error){
            console.log(error);
            }
        });
    }
    $("#login-form").submit(function(event){
        event.preventDefault();
        ajax_login();
    });
});

