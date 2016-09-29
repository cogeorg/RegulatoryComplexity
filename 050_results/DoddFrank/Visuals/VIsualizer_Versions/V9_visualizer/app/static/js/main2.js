

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
    };

    /* Context menu for the document*/
    /* ******************** */

    $(document).bind("contextmenu", function (event) {
        // Avoid the real one
        event.preventDefault();
        // Show contextmenu
        $(".custom-menu").finish().toggle(100).
        // In the right position (the mouse)
        css({
            top: event.pageY + "px",
            left: event.pageX + "px"
        });
    });

    $('body:not("contextmenu")').click(function(){
        $("#menu").css({ 'top' : '-1000px', 'left' : '-1000px' });
    });


    // Classification
    //Grab selected text
    function getSelectedText(){
        if(window.getSelection){
            return window.getSelection().toString();
        }
        else if(document.getSelection){
            return document.getSelection();
        }
        else if(document.selection){
            return document.selection.createRange().text;
        }
    }

    $("div").click("mouseup",function() {
        selection = getSelectedText();
        if(selection.length >= 3) {
        var spn = ("<span id='aux'>" + selection + "</span>");
        var html = $(this).html().replace(selection,spn);
        $(this).html(html);
        }
    });

    $(".custom-menu li").click(function(){
    // This is the triggered action name
        switch($(this).attr("data-action")) {
            // A case for each action. Your actions here
            case "A-Antecedent":
                document.getElementById("aux").className = "A-Antecedent";
                document.getElementById("aux").removeAttribute("id");
                break;
            case "C-Consequent":
                document.getElementById("aux").className = "C-Consequent";
                document.getElementById("aux").removeAttribute("id");
                break;
            case "T1-Topic":
                document.getElementById("aux").className = "T1-Topic";
                document.getElementById("aux").removeAttribute("id");
                break;
            case "T2-Topic":
                document.getElementById("aux").className = "T2-Topic";
                document.getElementById("aux").removeAttribute("id");
                break;
            case "T3-Topic":
                document.getElementById("aux").className = "T3-Topic";
                document.getElementById("aux").removeAttribute("id");
                break;
            case "EL-LeftEquivalent":
                document.getElementById("aux").className = "EL-LeftEquivalent";
                document.getElementById("aux").removeAttribute("id");
                break;
            case "ER-RightEquivalent":
                document.getElementById("aux").className = "EL-LeftEquivalent";
                document.getElementById("aux").removeAttribute("id");
                break; 
            case "Update":
                var newFile = document.getElementById("result").innerHTML;
                var newFileString = newFile.toString();
                var titleName = $("#mySidenav a").attr("id");
                var paramData = {file: newFileString, user_name: user_name, title: titleName};
                $.getJSON('/_html2python', {
                    params: JSON.stringify(paramData)
                     });
                break; 
            case "Remove":

                break;
        }
             // Hide it AFTER the action was triggered
             $(".custom-menu").hide(100);
    });




})();
