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


        /* Load different titles*/
        /* ******************** */

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
                    var paramData = {wordList:list_high, user_name:  user_name};
                    $.ajax({
                        type : "POST",
                        url : '/coherence/_array2python',
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
                                hltr.find("(" + words[i] + ")", false);
                                hltr.find('"' + words[i] + '"', false);
                                hltr.find(" " + words[i] + "\n", false);
                                hltr.find("\n" + words[i] + " ", false);
                                hltr.setReady(true);
                                i +=1;
                            });
                            $("#words").empty();
                            list_high = [];
                        }
                    });


                });
            });
        };

        // save words when clicking on "Instructions", "Words classified" or "Log out" button
        $(document).on('click', '.nav-tabs form button', function(){
            var paramData = {wordList:list_high, user_name:  user_name};
            $.ajax({
                type : "POST",
                url : '/coherence/_array2python',
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
                        hltr.find("(" + words[i] + ")", false);
                        hltr.find('"' + words[i] + '"', false);
                        hltr.find(" " + words[i] + "\n", false);
                        hltr.find("\n" + words[i] + " ", false);
                        hltr.setReady(true);
                        i +=1;
                    });
                    list_high = [];
                }
            });
        });

        /* ******************** */



        /* Coloring */
        /* ******************** */

        $(".buttons form input").click(function(){
            // This is the triggered action name
            switch($(this).attr("id")) {
                // A case for each action. Your actions here
                case "R":
                flag = true;
                hltr.setColor("#6495ed");
                hltr.setClick(true);
                hltr.setReady(true);
                break;
                case "B":
                flag = true;
                hltr.setColor("#00ff00");
                hltr.setClick(true);
                hltr.setReady(true);
                break;
                case "D":
                flag = true;
                hltr.setColor("#ffff00");
                hltr.setClick(true);
                hltr.setReady(true);
                break;
                case "L":
                flag = true;
                hltr.setColor("#a2a2a2");
                hltr.setClick(true);
                hltr.setReady(true);
                break;
            }
            count =1;
        });


        /* Update & Remove */
        /* ******************** */
        $(".save form input").click(function(){
            // This is the triggered action name
            switch($(this).attr("id")) {
                case "Update":
                /* Input to python flask array2python function */
                var paramData = {wordList:list_high, user_name:  user_name};
                $.ajax({
                    type : "POST",
                    url : '/coherence/_array2python',
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
                            hltr.find("(" + words[i] + ")", false);
                            hltr.find('"' + words[i] + '"', false);
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
                            hltr.find("(" + words[i] + ")", false);
                            hltr.find('"' + words[i] + '"', false);
                            hltr.find(" " + words[i] + "\n", false);
                            hltr.find("\n" + words[i] + " ", false);
                            hltr.setReady(true);
                            i +=1;
                        });
                        /* Update the word classified frame */
                        $("#words").empty();
                        /* Make table */
                        // removeUL(remove);
                        list_high = [];
                    }
                });
                var titleName = $("#mySidenav a.selected").attr("id")
                load_html(titleName)
                break;
                case "Remove":
                flag = true;
                hltr.setColor("white");
                hltr.setClick(true);
                hltr.setReady(true);
                break;
            }
            count =1;
        });

        /* Remove on rightclick */
        /* ******************** */
        $("#result").on('contextmenu', 'span', function(){
            term = $(this).text().replace(/,|;|\.|:|\(|\)|"|\\n/gi, '').toLowerCase()
            if (term !=""){
                if (term in list_high){
                    var index = list_high.indexOf(term);
                    list_high.splice(index, 1);
                }else{
                    list_high.push(term + "_" + "white");
                }
            }
            $(this).css("background-color","white");
        })


    })();
