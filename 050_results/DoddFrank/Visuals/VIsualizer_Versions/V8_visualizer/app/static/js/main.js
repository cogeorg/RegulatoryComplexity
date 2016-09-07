/* Main javascript file*/
/* The highlighter uses texthighlighter plugin https://github.com/mir3z/texthighlighter*/
(function () {
    var user_name = $( "p:first" ).text();
    var sandbox = document.getElementById('dodd_frank');
    var list_high = [];
    var count = 1;
    var flag = true;
    var hltr = new TextHighlighter(sandbox, {
        onAfterHighlight: function (range, highlights) {
            /* function which stores the highlighted word in a list*/
             var string = highlights.map(function (h) { return  h.innerText ;}).join(' ');
             if (string !=""){
                 if (flag){
                     list_high.push(string + "_" + hltr.getColor());
                     flag = false;
                 }else{
                     flag = true;
                 }

             }
        }});


    /* Right Table double click feature*/
    $(document).on('dblclick', '#words li', function(){
        list_high.push($(this).text() + "_" + "white");
        flag = true;
        hltr.setColor("white");
        hltr.find($(this).text(), false);
        hltr.setReady(true);
        this.parentNode.removeChild(this);
        count=1;
    });
    /* ******************** */


    /* Load different titles*/
    /* ******************** */
    document.getElementById("mySidenav").style.width = "150px";

    var auxiliar = "";
     $("#mySidenav").click(function(){
            count =-1;
     });


     $("#mySidenav a").click(function(){
            auxiliar = $(this).attr("id");
            load_html(auxiliar);
            count =-1;
     });

      function load_html(line){
      $(document).ready( function() {
        $.get(line, function(res) {
            $("#result").html(res);
            var paramData = {wordList:list_high, user_name:  user_name};
                             $.getJSON('/_array2python', {
                                params: JSON.stringify(paramData)
                                 }, function(data){
                                        var words = data.words;
                                        var colors = data.colors;
                                        var i = 0;
                                        words.forEach(function(entry) {
                                            hltr.setColor(colors[i]);
                                            hltr.find(words[i], false);
                                            hltr.setReady(true);
                                            i +=1;
                                            });
                                        $("#words").empty();
                                        makeUL(words.slice(0,21), colors.slice(0,21));
                                        list_high = [];
                                     });


        });
        });
        };

        /* ******************** */



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


                $(document).click(function() {
                    if ($('.custom-menu').is(":visible")){
                        hltr.setClick(false);
                        hltr.setReady(true);
                        $(".custom-menu").hide(100);
                        count =1;
                    }else {
                        var text = window.getSelection().toString()
                        if (count == 1 && text!="") {
                            count += 1;
                        }
                        else  {
                             hltr.setClick(false);
                             hltr.setReady(true);
                             count =1;
                        }
                    }
                });

                $('.custom-menu').click(function(event){
                     event.stopPropagation();
                });


            /*

            /* Put the proper classification names and colors
             # case "Name":
             # hltr.setColor(Color);
             # Be sure to have the same number of cases and Names
             */

                 $(".custom-menu li").click(function(){

                     // This is the triggered action name
                     switch($(this).attr("data-action")) {
                         // A case for each action. Your actions here
                         case "GrammaticalOperators":
                             flag = true;
                             hltr.setColor("#554600");
                             hltr.setClick(true);
                             hltr.setReady(true);
                             break;
                         case "LegalOperators":
                             flag = true;
                             hltr.setColor("#806D15");
                             hltr.setClick(true);
                             hltr.setReady(true);
                             break;
                         case "LegalReferences":
                             flag = true;
                             hltr.setColor("#D4C26A");
                             hltr.setClick(true);
                             hltr.setReady(true);
                             break;
                         case "LogicalOperators":
                             flag = true;
                             hltr.setColor("#FFF0AA");
                             hltr.setClick(true);
                             hltr.setReady(true);
                             break;
                         case "RegulationOperators":
                             flag = true;
                             hltr.setColor("#AA0739");
                             hltr.setClick(true);
                             hltr.setReady(true);
                             break;
                         case "Attributes":
                             flag = true;
                             hltr.setColor("green");
                             hltr.setClick(true);
                             hltr.setReady(true);
                             break;
                         case "EconomicOperand":
                             flag = true;
                             hltr.setColor("yellow");
                             hltr.setClick(true);
                             hltr.setReady(true);
                             break;
                         case "Other":
                             flag = true;
                             hltr.setColor("red");
                             hltr.setClick(true);
                             hltr.setReady(true);
                         break;
                         case "Update":
                             var paramData = {wordList:list_high, user_name:  user_name};
                             $.getJSON('/_array2python', {
                                params: JSON.stringify(paramData)
                                 }, function(data){
                                        var words = data.new_words;
                                        var colors = data.new_colors;
                                        var remove = data.remove;
                                        var all_words = data.words;
                                        var all_colors = data.colors;
                                        var i = 0;
                                        words.forEach(function(entry) {
                                            hltr.setColor(colors[i]);
                                            hltr.find(words[i], false);
                                            hltr.setReady(true);
                                            i +=1;
                                            });
                                        var i =0;
                                        remove.forEach(function(entry) {
                                            hltr.setColor("white");
                                            hltr.find(entry, false);
                                            hltr.setReady(true);
                                            i +=1;
                                            });
                                        $("#words").empty();
                                        makeUL(all_words.slice(0, 21), all_colors.slice(0, 21));
                                        // removeUL(remove);
                                        list_high = [];
                                     });
                             break;
                         case "Remove":
                             flag = true;
                             hltr.setColor("white");
                             hltr.setClick(true);
                             hltr.setReady(true);
                             break;
                     }
                    count =1;
                     // Hide it AFTER the action was triggered
                     $(".custom-menu").hide(100);
                   });




})();
