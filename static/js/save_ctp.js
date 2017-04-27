/**
 * Created by gamedu on 18/04/17.
 */
$(document).ready(function(){
    $("#save").click(function(){
        var logs = $('table > tbody > tr');

        $.each(logs, function() {
            var tdFather = $(this).children('.father');
            var tdChild = $(this).children('.child');
            $.each(tdChild, function() {
                var valueChild = $(this).children('#id_variable_child').val();
                var line = $(this).children('.line').text();
                $.each(tdFather, function() {
                    var id = $('#net').text();
                    var competency_father = $('#competency_father').text();
                    var value = $(this).children('.inputCTP').val();
                    var father = $(this).children('input')[0].id;
                    //console.log('father: ' + father + " child: " + valueChild + " value: " + value);
                    var csrf_token = $('input[name*=csrfmiddlewaretoken]').val();
                    var sendInfo = {
                        csrfmiddlewaretoken: csrf_token,
                        "value": value,
                        "baysianet": id,
                        "competency_father": competency_father,
                        "variable_father": father,
                        "variable_child": valueChild,
                        "line": line
                    };

                    $.ajax({
                       type: "POST",
                       url: "/api/ctp/",
                       dataType: "json",
                       success: function () {
                           console.log("foi")
                       },
                       data: sendInfo
                   });
                }, valueChild, line );
            });
        });
    });
});