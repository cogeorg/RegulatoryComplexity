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

    /* Word count function */
    function wordCount() {
          var count = document.getElementById('result').innerText.split(' ').length;
          var spans = document.getElementsByTagName('span')
          spanList = []
          for(var i = 0; i < spans.length; i++) {
            if (spans[i].style.backgroundColor !== 'white'){
                var split = spans[i].innerText.split(' ')
                for(var j = 0; j < split.length; j++) {
                  if (split[j]) {
                    spanList.push(split[j])
                  }
                }
                var spanCount = spanList.length -17     // -17 because categories and counting values are in spans
            }
          }
          var remaining = count - spanCount
          document.getElementById("value1").innerHTML = count.toString();
          document.getElementById("value2").innerHTML = spanCount.toString();
          document.getElementById("value3").innerHTML = remaining.toString();
    }


    /* Right Table double click feature*/
    $(document).on('dblclick', '#words li', function(){
        list_high.push($(this).text() + "_" + "white");
        // does not work with flask
        // Similar to the remove dropdown
        flag = true;
        hltr.setColor("white");
        hltr.find($(this).text(), false);
        hltr.setReady(true);
        // to remove the li item from the frame
        this.parentNode.removeChild(this);
        count=1;
        wordCount()
    });
    /* ******************** */


    /* Load different titles*/
    /* ******************** */
    document.getElementById("mySidenav").style.width = "150px";

    var auxiliar = "";
     $("#mySidenav").click(function(){
            count =-1;
            wordCount()
     });


     $("#mySidenav a").click(function(){
            auxiliar = $(this).attr("id");
            $("#mySidenav a").removeClass('selected');
            $(this).addClass('selected');
            load_html(auxiliar);
            count =-1;
            /*wordCount()*/
     });

    function load_html(line){

      $(document).ready( function() {
        $.get(line, function(res) {
            // load html title
            $("#result").html(res);
            var paramData = {wordList:list_high, user_name:  user_name};
             $.ajax({
                type : "POST",
                url : '/words/_array2python',
                data: JSON.stringify(paramData, null, '\t'),
                contentType: 'application/json;charset=UTF-8',
                success: function(data) {
                        var words = data.words;
                        var colors = data.colors;
                        var i = 0;
                        words.forEach(function(entry) {
                            hltr.setColor(colors[i]);
                            hltr.find(" " + words[i] + " ", false);
                            hltr.find(" " + words[i] + ",", false);
                            hltr.find(" " + words[i] + ";", false);
                            hltr.find(" " + words[i] + ".", false);
                            hltr.find(" " + words[i] + ":", false);
                            hltr.find(" " + words[i] + "-", false);
                            hltr.find(" " + words[i] + ")", false);
                            hltr.find("(" + words[i] + " ", false);
                            hltr.find(" " + words[i] + "\n", false);
                            hltr.find("\n" + words[i] + " ", false);
                            hltr.setReady(true);
                            i +=1;
                            });
                        $("#words").empty();
                        makeUL(words.slice(0,21), colors.slice(0,21));
                        list_high = [];
                        wordCount()
                        }
                });


            });
        });
        };

        // save words when clicking on "Instructions", "Words classified" or "Log out" button
        $(document).on('click', '.nav-tabs ul form button', function(){
            var paramData = {wordList:list_high, user_name:  user_name};
        $.ajax({
            type : "POST",
            url : '/words/_array2python',
            data: JSON.stringify(paramData, null, '\t'),
            contentType: 'application/json;charset=UTF-8',
            success: function(data) {
                var words = data.words;
                var colors = data.colors;
                var i = 0;
                words.forEach(function(entry) {
                    hltr.setColor(colors[i]);
                    hltr.find(" " + words[i] + " ", false);
                    hltr.find(" " + words[i] + ",", false);
                    hltr.find(" " + words[i] + ";", false);
                    hltr.find(" " + words[i] + ".", false);
                    hltr.find(" " + words[i] + ":", false);
                    hltr.find(" " + words[i] + "-", false);
                    hltr.find(" " + words[i] + ")", false);
                    hltr.find("(" + words[i] + " ", false);
                    hltr.find(" " + words[i] + "\n", false);
                    hltr.find("\n" + words[i] + " ", false);
                    hltr.setReady(true);
                    i +=1;
                });
                list_high = [];
            }
        /*$.getJSON('words/_array2python', {
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
                list_high = [];
            });*/
            });
        });

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
                             case "LogicalConnectors":
                             flag = true;
                             hltr.setColor("#8B69F9");
                             hltr.setClick(true);
                             hltr.setReady(true);
                             break;
                         case "RegulatoryOperators":
                             flag = true;
                             hltr.setColor("#C25FF8");
                             hltr.setClick(true);
                             hltr.setReady(true);
                             break;
                         case "EconomicOperands":
                             flag = true;
                             hltr.setColor("#FFFF58");
                             hltr.setClick(true);
                             hltr.setReady(true);
                             break;
                         case "Attributes":
                             flag = true;
                             hltr.setColor("#FFE258");
                             hltr.setClick(true);
                             hltr.setReady(true);
                             break;
                         case "LegalReferences":
                             flag = true;
                             hltr.setColor("#AFAFAF");
                             hltr.setClick(true);
                             hltr.setReady(true);
                             break;
                         case "FunctionWords":
                             flag = true;
                             hltr.setColor("#696969");
                             hltr.setClick(true);
                             hltr.setReady(true);
                             break;
                         case "Other":
                             flag = true;
                             hltr.setColor("#A3A3A3");
                             hltr.setClick(true);
                             hltr.setReady(true);
                         break;
                         case "Update":
                             /* Input to python flask array2python function */
                             var paramData = {wordList:list_high, user_name:  user_name};
                                $.ajax({
                                    type : "POST",
                                    url : '/words/_array2python',
                                    data: JSON.stringify(paramData, null, '\t'),
                                    contentType: 'application/json;charset=UTF-8',
                                    success: function(data) {
                                 /* Output of flask function */
                                        var words = data.new_words;
                                        var colors = data.new_colors;
                                        var remove = data.remove;
                                        var all_words = data.words;
                                        var all_colors = data.colors;
                                        var i = 0;
                                        words.forEach(function(entry) {
                                            hltr.setColor(colors[i]);
                                            hltr.find(" " + words[i] + " ", false);
                                            hltr.find(" " + words[i] + ",", false);
                                            hltr.find(" " + words[i] + ";", false);
                                            hltr.find(" " + words[i] + ".", false);
                                            hltr.find(" " + words[i] + ":", false);
                                            hltr.find(" " + words[i] + "-", false);
                                            hltr.find(" " + words[i] + ")", false);
                                            hltr.find("(" + words[i] + " ", false);
                                            hltr.find(" " + words[i] + "\n", false);
                                            hltr.find("\n" + words[i] + " ", false);
                                            hltr.setReady(true);
                                            i +=1;
                                            });
                                        var i =0;
                                        remove.forEach(function(entry) {
                                            hltr.setColor("white");
                                            hltr.find(" " + entry + " ", false);
                                            hltr.find(" " + entry + ",", false);
                                            hltr.find(" " + entry + ";", false);
                                            hltr.find(" " + entry + ".", false);
                                            hltr.find(" " + entry + ":", false);
                                            hltr.find(" " + entry + "-", false);
                                            hltr.find(" " + entry + ")", false);
                                            hltr.find("(" + entry + " ", false);
                                            hltr.find(" " + words[i] + "\n", false);
                                            hltr.find("\n" + words[i] + " ", false);
                                            hltr.setReady(true);
                                            i +=1;
                                            });
                                 /* Update the word classified frame */
                                        $("#words").empty();
                                 /* Make table */
                                        makeUL(all_words.slice(0, 21), all_colors.slice(0, 21));
                                        // removeUL(remove);
                                        list_high = [];
                                        }
                                     });
                                     var titleName = $("#mySidenav a.selected").attr("id")
                                     load_html(titleName)
                                     /*wordCount()*/
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
