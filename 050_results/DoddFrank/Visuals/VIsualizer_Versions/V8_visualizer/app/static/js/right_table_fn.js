
function removeUL(array){
    for(var i = 0; i < array.length; i++) {
        $('#words li').filter(function () {
            return $.text([this]) === array[i];
        }).remove();
    }
}

function makeUL(array, array2) {
// Create the list element:
    var list = document.getElementById('words');
    var first = document.createElement('li');
    first.className= "li_words";
    first.appendChild(document.createTextNode("Words Classified"));
    list.appendChild(first);

    for(var i = 0; i < array.length; i++) {
    // Create the list item:
        var item = document.createElement('li');
        item.style.backgroundColor = array2[i];
        // Set its contents:
        text = array[i];
        item.appendChild(document.createTextNode(text));

     // Add it to the list:
         list.appendChild(item);
}
    return list;
}


