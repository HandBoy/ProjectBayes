/**
 * Created by gamedu on 23/02/17.
 */


//var linha = document.getElementById("myTable").rows[0].cells.namedItem("inicio");


$(document).ready(function(){

    /*$('#inicio:first-child').each(function() {
        var td = $(this).children('td:eq(3)');
        console.log(td.text());
    });*/
    var filhos = $('#inicio:first-child')
    //console.log(filhos.children('td:eq(3)').text())
    var valores = filhos.children('td:eq(3)').text();
    var valor = valores.split(";");
    for (var i=0;i<valor.length;i++){
        console.log(valor[i]);
        $("#numero"+valor[i]).text(valor[i]);
    }

});