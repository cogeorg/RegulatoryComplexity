// Function to create the graphs (tables)
function graphs(){
    var html = document.getElementById('result').innerHTML
    // extract title name
    var title = /(TITLE\s.*?)<div/g.exec(html)[1]
    $("#graph").html('<div class = "ex1">' + title + '</div>')
    // extract sections and corresponding paragraphs
    var pattern = /(SEC\.\s[0-9].+?\.\s[A-Z].*?\.) | (class="ex5")/g
    pattern.lastIndex = 0;
    id = 0
    while (section = pattern.exec(html)){
        // paste section name
        if (String(section[1]).startsWith('SEC.') == true){
            $("#graph").append('<div class = "ex4">' + section[1] + '</div>')
        }
        // generate placeholder for paragraphs
        else {
            $("#graph").append('<div class = "table" id="'+ id + '"></div>')
            id += 1
        }
    }
    // extract paragraphs
    var paragraphs = document.getElementsByClassName('ex5')
    for(var i = 0; i < paragraphs.length; i++) {
        // extract HTML
        var parHtml = paragraphs[i].innerHTML
        // extract spans
        var regex = /<sp.*?<\/span>/g
        if (regex.test(parHtml) == true){
            var spans = parHtml.match(regex)
            for(var j = 0; j < spans.length; j++) {
                // create table
                $("#" + String(i)).append(spans[j])
            }
        }
    }
}

(function () {
    /* First p tag*/
    var user_name = $( "p:first" ).text();

    /* Load different titles*/
    /* ******************** */
    /*document.getElementById("mySidenav").style.width = "120px";*/

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
            graphs()
            });
        });
    }


})();
