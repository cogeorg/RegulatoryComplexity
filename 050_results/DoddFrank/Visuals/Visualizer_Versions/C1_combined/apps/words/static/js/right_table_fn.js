function removeUL(array){
    for(var i = 0; i < array.length; i++) {
        $('#words li').filter(function () {
            // Get the li element with the text of the array[i] (to remove)
            return $.text([this]) === array[i];
        }).remove();
    }
}

function makeUL(array, array2) {
// Create the list element:
    var list = document.getElementById('words');
    var first = document.createElement('li');
    // Create header Words Classfied
    first.className= "li_words";
    first.appendChild(document.createTextNode("Words Classified:"));
    // Append to the UL
    list.appendChild(first);

    for(var i = 0; i < array.length; i++) {
    // Create the list item:
        var item = document.createElement('li');
        // Put the backgroud color
        item.style.backgroundColor = array2[i];
	item.className= "li_words";
        // Set its contents:
        text = array[i];
        item.appendChild(document.createTextNode(text));

     // Add it to the list Ul:
         list.appendChild(item);
}
    return list;
}


