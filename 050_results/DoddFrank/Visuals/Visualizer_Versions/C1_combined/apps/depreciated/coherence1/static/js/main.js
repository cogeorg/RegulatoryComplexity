/* Load different titles*/
/* ******************** */
(function () {
    /* First p tag*/
    var user_name = $( "p:first" ).text();

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

/* Save function */
/* ******************************************* */
function save() {
    var user_name = $( "p:first" ).text();
    var newFile = document.getElementById("result").innerHTML;
    var newFileString = newFile.toString();

    var titleName = $("#mySidenav a.selected").attr('id');
    console.log(titleName)
    var paramData = {file: newFileString, user_name: user_name, title: titleName};
    $.ajax({
        type : "POST",
        url : '/coherence/_html2python',
        data: JSON.stringify(paramData, null, '\t'),
        contentType: 'application/json;charset=UTF-8',
        success: function(result) {
            //console.log(result);
        }
    });
}

/* Highlight and remove highlight */
/* ******************************************* */

function surroundSelection(type) {
    var selection = window.getSelection().getRangeAt(0);
    var txt = window.getSelection();
    var selectedText = selection.extractContents();
    var parent = selection.commonAncestorContainer.parentNode;
    var span = document.createElement("span");
    span.setAttribute("class",type)
    span.appendChild(selectedText);
    span.oncontextmenu = function (ev) {
        this.parentNode.insertBefore(document.createTextNode(this.innerText), this);
        this.parentNode.removeChild(this);
    }
    selection.insertNode(span);
}

function removeHighlight() {
    var selection = window.getSelection().getRangeAt(0);
    var selectedText = document.createTextNode( selection.toString() );
    selection.deleteContents();
    selection.insertNode(selectedText);
}
