/**
 * Created by gamedu on 18/04/17.
 */
$(document).ready(function(){

    $("#save").click(function(){
        var logs = $('table > tbody > tr');
        //console.log(logs.length);

        $.each(logs, function() {
            var tdFather = $(this).children('.father');
            var tdChild = $(this).children('.child');
            $.each(tdChild, function() {
                var valueChild = $(this).children('#id_variable_child').val();
                $.each(tdFather, function() {
                    var value = $(this).children('.inputCTP').val();
                    var father = $(this).children('input')[0].id;
                    console.log('father: ' + father + " child: " + valueChild + " value: " + value);
                }, valueChild );
            });
        });

    });
});