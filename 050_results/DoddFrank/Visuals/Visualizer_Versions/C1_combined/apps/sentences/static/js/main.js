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
            graphs()
            loadCheckbox()
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

    var titleName = $("#mySidenav a.selected").attr("id");
    var paramData = {file: newFileString, user_name: user_name, title: titleName};
    $.ajax({
        type : "POST",
        url : '/sentenceparts/_html2python',
        data: JSON.stringify(paramData, null, '\t'),
        contentType: 'application/json;charset=UTF-8',
        success: function(result) {
            //console.log(result);
        }
    });
    saveCheckbox()
}

/* Highlight and remove highlight */
/* ******************************************* */

function surroundSelection(type) {
    var selection = window.getSelection().getRangeAt(0);
    var selectedText = selection.extractContents();
    var span = document.createElement("span");
    span.setAttribute("class",type)
    span.appendChild(selectedText);
    span.oncontextmenu = function (ev) {
        this.parentNode.insertBefore(document.createTextNode(this.innerText), this);
        this.parentNode.removeChild(this);
        graphs();
        loadCheckbox();
    }
    selection.insertNode(span);
    graphs();
    loadCheckbox();

}

function removeHighlight() {
    var selection = window.getSelection().getRangeAt(0);
    var selectedText = document.createTextNode( selection.toString() );
    selection.deleteContents();
    selection.insertNode(selectedText);
    graphs( function(){
        loadCheckbox(function(){
            saveCheckbox();
        });
    });
}

/* Function to create the graphs (tables)*/
/* ******************************************* */
function graphs(callback){
    var html = document.getElementById('result').innerHTML
    // extract title name
    var title = /(TITLE\s.*?\.)/g.exec(html)[1]
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
    // extract paragraphs and build table
    var paragraphs = document.getElementsByClassName('ex5')
    for(var i = 0; i < paragraphs.length; i++) {
        // extract HTML
        var parHtml = paragraphs[i].innerHTML
        var el = document.createElement('html');
        el.innerHTML = parHtml
        // extract spans
        var regex = /<sp.*?<\/span>/g
        if (regex.test(parHtml) == true){
            // build table
            $("#" + String(i)).append('<div id="myDynamicTable' + String(i) + '"></div>');
            var myTableDiv = document.getElementById("myDynamicTable" + String(i));
            var table = document.createElement('TABLE');
            table.border='1';
            var tableBody = document.createElement('TBODY');
            table.appendChild(tableBody);
            // find all spans
            var allSpans = el.getElementsByTagName('span');
            // find all clean spans
            spans = []
            for(var j = 0; j < allSpans.length; j++) {
                var spanClass = allSpans[j].className
                var spanText = allSpans[j].innerText
                // no headlines an no empty spans allowed
                if (spanClass != 'H' && spanText != ""){
                    spans.push(allSpans[j])
                }
            }
            // counter for ID
            var a = 0;
            // loop over all spans to build table
            for(var j = 0; j < spans.length; j++) {
                var spanClass = spans[j].className
                var spanText = spans[j].innerText
                // build table
                var tr = document.createElement('TR');
                tableBody.appendChild(tr);
                // first row with parts of sentences
                var k = 0
                var td = document.createElement('TD');
                td.appendChild(document.createTextNode(spanText));
                td.setAttribute('class', spanClass)
                tr.appendChild(td);
                // second row with ID
                var k = 1
                var td = document.createElement('TD');
                td.appendChild(document.createTextNode(a+1));
                tr.appendChild(td);
                var a = a + 1
                // remaining rows with checkboxes
                for (var k = 2; k < spans.length+2; k++){
                    var td = document.createElement('TD');
                    if (k < a+1) {
                        var checkbox = document.createElement('input');
                        checkbox.setAttribute('id', 'check-' + i + '-' + String(j) + '-' + String(k-2))
                        checkbox.type = "checkbox";
                        td.appendChild(checkbox);
                        tr.appendChild(td);
                    }
                    else{
                        td.appendChild(document.createTextNode(''));
                        tr.appendChild(td);
                    }
                }
            }
            // create table header
            var header = table.createTHead();
            var row = header.insertRow(0);
            var cell1 = row.insertCell(0);
            cell1.innerHTML = "Part";
            var cell2 = row.insertCell(1);
            cell2.innerHTML = "ID";
            for (l = 0; l < a; l++){
                var cell = row.insertCell(2+l)
                cell.innerHTML = l+1
            }
            myTableDiv.appendChild(table);
        }
    }
    // set checkboxes to "checked"
    $("input").on("change", function(){
        if (this.checked) {
            this.setAttribute("checked", "checked");
        } else {
            this.removeAttribute("checked");
        }
    });

    if (callback) {
        callback();
    }
}

/* Save checkboxes */
/* ******************************************* */

function saveCheckbox () {
    var userName = $( "p:first" ).text();
    var titleName = $("#mySidenav a.selected").attr("id");
    // find all inputs
    inputs = document.getElementsByTagName('input');
    inputIds = [];
    checks = [];
    // find all inputs with id "check" and save their "checked" attribute
    for(var i = 0; i < inputs.length; i++) {
        var inputId = inputs[i].getAttribute('id')
        if (inputId != null && inputId.startsWith('check')){
            var inputCheck = inputs[i].getAttribute('checked')
            if (inputCheck == 'checked'){
                var check = 1
            }
            else{
                var check = 0
            }
            inputIds.push(inputId)
            checks.push(check)
        }
    }
    // save data to txt file
    var paramData = {userName:  userName, titleName: titleName, inputIds: inputIds, checks: checks};
    $.ajax({
        type : "POST",
        url : '/sentenceparts/_array2python',
        data: JSON.stringify(paramData, null, '\t'),
        contentType: 'application/json;charset=UTF-8',
        success: function(data) {

        }
    });
}

/* Load checkboxes */
/* ******************************************* */
function loadCheckbox (callback){
    var userName = $( "p:first" ).text();
    var titleName = $("#mySidenav a.selected").attr("id");
    var paramData = {userName:  userName, titleName: titleName}
    $.ajax({
        type : "POST",
        url : '/sentenceparts/_array2javascript',
        data: JSON.stringify(paramData, null, '\t'),
        contentType: 'application/json;charset=UTF-8',
        success: function(data) {
            var inputIds = data.inputIds
            var checks = data.checks
            for (var i=0; i < inputIds.length; i++) {
                if (checks[i] == 1){
                    var checkbox = document.getElementById(inputIds[i])
                    try {
                        checkbox.setAttribute("checked", "checked");
                    } catch (e) {};
                }
            }
            if (callback) {
                callback();
            }
        }
    });
}
