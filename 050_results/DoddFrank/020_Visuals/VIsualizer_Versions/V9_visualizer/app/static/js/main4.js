

(function () {
    /* First p tag*/
    var user_name = $( "p:first" ).text();
    /* Div (Document) to apply Text High*/
    var sandbox = document.getElementById('dodd_frank');


    /* Load different titles*/
    /* ******************** */
    document.getElementById("mySidenav").style.width = "150px";

    var auxiliar = "";
     $("#mySidenav").click(function(){
            count =-1;
     });


     $("#mySidenav a").click(function(){
            auxiliar = $(this).attr("id");
            $("#mySidenav a").removeClass('selected');
            $(this).addClass('selected');
            load_html(auxiliar);
            count =-1;
     });

    function load_html(line){
        $(document).ready( function() {
            $.get(line, function(res) {
            // load html title
            $("#result").html(res);
            });
        });
    }


})();
