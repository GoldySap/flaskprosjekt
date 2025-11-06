$(document).ready(function() {
        $('#products').on("click", function() {
            $.get('/products', function(){
                products(); 
            });
        });
        $('#test').on("click", function() {
            $.get('/users', function(){
                users();
            });
        });
    });