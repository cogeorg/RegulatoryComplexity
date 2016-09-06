/* Main javascript file*/
/* The highlighter uses texthighlighter plugin https://github.com/mir3z/texthighlighter*/



(function () {
    var sandbox = document.getElementById('dodd_frank');
    var serialized = '';
    var list_high = [];
    var hltr = new TextHighlighter(sandbox, {
        onAfterHighlight: function (range, highlights) {
            /* function which stores the highlighted word in a list*/
             var string = highlights.map(function (h) { return  h.innerText ;}).join('');
             if (string !=""){
             if (list_high[list_high.length - 1] != string + "_" + hltr.getColor()) {
                 list_high.push(string + "_" + hltr.getColor());
             }
                }
        }});

    /* Context menu for the document*/
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


                $(window).click(function() {
                    if ($('.custom-menu').is(":visible")){
                        hltr.setColor("white");
                        hltr.setReady(true);
                    }
                      $(".custom-menu").hide(100);
                    });

                $('.custom-menu').click(function(event){
                     event.stopPropagation();
                });



                 $(".custom-menu li").click(function(){

                     // This is the triggered action name
                     switch($(this).attr("data-action")) {
                         // A case for each action. Your actions here
                         case "GrammaticalOperators":
                             hltr.setColor("#554600");
                             hltr.setReady(true);
                             break;
                         case "LegalOperators":
                             hltr.setColor("#806D15");
                             hltr.setReady(true);
                             break;
                         case "LegalReferences":
                             hltr.setColor("#D4C26A");
                             hltr.setReady(true);
                             break;
                         case "LogicalOperators":
                             hltr.setColor("#FFF0AA");
                             hltr.setReady(true);
                             break;
                         case "RegulationOperators":
                             hltr.setColor("#AA0739");
                             hltr.setReady(true);
                             break;
                         case "Attributes":
                             hltr.setColor("green");
                             hltr.setReady(true);
                             break;
                         case "EconomicOperand":
                             hltr.setColor("yellow");
                             hltr.setReady(true);
                             break;
                         case "Other":
                             hltr.setColor("red");
                             hltr.setReady(true);
                             break;
                         case "Update":
                             $.getJSON('/_array2python', {
                                wordlist: JSON.stringify(list_high)
                                 }, function(data){
                                        var words = data.words;
                                        var colors = data.colors;
                                        var i = 0;
                                        console.log(words);
                                        words.forEach(function(entry) {
                                            console.log(entry);
                                            hltr.setColor(colors[i]);
                                            hltr.find(words[i], false);
                                            hltr.setReady(true);
                                            i +=1;
                                            });
                                        list_high = [];
                                     });
                             break;
                         case "Remove":
                             hltr.setColor("white");
                             hltr.setReady(true);
                             break;
                     }

                     // Hide it AFTER the action was triggered
                     $(".custom-menu").hide(100);
                   });




})();
