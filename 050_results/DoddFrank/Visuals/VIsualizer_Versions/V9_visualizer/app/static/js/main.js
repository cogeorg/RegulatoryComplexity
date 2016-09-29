/* Main javascript file*/
/* The highlighter uses texthighlighter plugin https://github.com/mir3z/texthighlighter*/
(function () {
    /* First p tag*/
    var user_name = $( "p:first" ).text();
    /* Div (Document) to apply Text High*/
    var sandbox = document.getElementById('dodd_frank');
    /* List to store Highlighted words*/
    var list_high = [];
    /* Variable to show/hide dropdown menu*/
    var count = 1;
    /* needs to be there because we click on word twice (highlight and rightclick)*/
    /* Necessary to store the words*/
    var flag = true;

    /* Object highlighter (document and OnAfterHighlight), saves word and color in list_high */
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
        // does not work with flask
        // Similar to the remove dropdown
        //flag = true;
        //hltr.setColor("white");
        //hltr.find($(this).text(), false);
        //hltr.setReady(true);
        // to remove the li item from the frame
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
/*            var paramData = {wordList:list_high, user_name:  user_name};
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
                                        makeUL(words.slice(0,10), colors.slice(0,10));
                                        list_high = [];
                                     }); */


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


                /* Click inside highlight is ok, click outside deletes highlight*/

                $(document).click(function() {
                    if ($('.custom-menu').is(":visible")){
                         /* Remove highlight range*/
                        hltr.setClick(false);
                        /* Finish the highlight process (without hihglight)*/
                        hltr.setReady(true);
                        $(".custom-menu").hide(100);
                        count =1;
                    }else {
                        var text = window.getSelection().toString()
                        if (count == 1 && text!="") {
                            count += 1;
                        }
                        else  {
                            /* When count is two clear the range*/
                             hltr.setClick(false);
                             hltr.setReady(true);
                             count =1;
                        }
                    }
                });

                $('.custom-menu').click(function(event){
                     event.stopPropagation();
                });


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
                             case "A-Antecedent":
                             flag = true;

                            $("div").click("mouseup",function() {
                            selection = getSelectedText();
                            if(selection.length >= 3) {
                            var spn = ("<span class='A-Antecedent'>" + selection + "</span>");
                            var html = $(this).html().replace(selection,spn);
                            $(this).html(html);
                            }
                            });


                             /*hltr.setColor("#81fd81");*/
                             hltr.setClick(true);
                             hltr.setReady(true);
                             break;
                         case "C-Consequent":
                             flag = true;
                             hltr.setColor("#cc99ff");
                             hltr.setClick(true);
                             hltr.setReady(true);
                             break;
                         case "T1-Topic":
                             flag = true;
                             hltr.setColor("#ffff99");
                             hltr.setClick(true);
                             hltr.setReady(true);
                             break;
                         case "T2-Topic":
                             flag = true;
                             hltr.setColor("#ffff00");
                             hltr.setClick(true);
                             hltr.setReady(true);
                             break;
                         case "T3-Topic":
                             flag = true;
                             hltr.setColor("#ffcc00");
                             hltr.setClick(true);
                             hltr.setReady(true);
                             break;
                         case "EL-LeftEquivalent":
                             flag = true;
                             hltr.setColor("#d3d3d3");
                             hltr.setClick(true);
                             hltr.setReady(true);
                             break;
                         case "ER-RightEquivalent":
                             flag = true;
                             hltr.setColor("#bababa");
                             hltr.setClick(true);
                             hltr.setReady(true);
                         break;
                         case "Update":
                            var newFile = document.getElementById("result").innerHTML;
                            var newFileString = newFile.toString();
                            var titleName = $("#mySidenav a").attr("id");
                            var paramData = {file: newFileString, user_name: user_name, title: titleName};
                            $.getJSON('/_html2python', {
                                params: JSON.stringify(paramData)
                                 });
                             /* Input to python flask array2python function */
/*                             var paramData = {wordList:list_high, user_name:  user_name};
                             $.getJSON('/_array2python', {
                                params: JSON.stringify(paramData)
                                 }, function(data){
                                 /* Output of flask function */
/*                                        var words = data.new_words;
                                        var colors = data.new_colors;
                                        var remove = data.remove;
                                        var all_words = data.words;
                                        var all_colors = data.colors;
                                        var i = 0;
                                        words.forEach(function(entry) {
                                            hltr.setColor(colors[i]);
                                            hltr.find(words[i], true);
                                            hltr.setReady(true);
                                            i +=1;
                                            });
                                        var i =0;
                                        remove.forEach(function(entry) {
                                            hltr.setColor("white");
                                            hltr.find(entry, true);
                                            hltr.setReady(true);
                                            i +=1;
                                            });
                                 /* Update the word classified frame */
/*                                        $("#words").empty();
                                 /* Make table */
/*                                        makeUL(all_words.slice(0, 10), all_colors.slice(0, 10));
                                        // removeUL(remove);
                                        list_high = [];
                                     });
                             break; */
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
