(function () {
    var removeBtn = document.getElementById('remove'),
        serializeBtn  = document.getElementById('serialize'),
        deserializeBtn  = document.getElementById('deserialize'),
        updateBtn = document.getElementById('update');
    var sandbox = document.getElementById('sandbox');
    var colors = new ColorPicker(document.querySelector('.color-picker'));
    var hltr = new TextHighlighter(sandbox);
    var serialized = '';



    colors.onColorChange(function (color) {
        hltr.setColor(color);
    });

    removeBtn.addEventListener('click', function () {
        hltr.removeHighlights();
    });

    updateBtn.addEventListener('click', function () {
        var serialized = hltr.serializeHighlights();
        $.getJSON('/_array2python', {
            wordlist: JSON.stringify(serialized)
        }, function(data){
                    var words = data.words;
                    var colors = data.colors;
                    var i = 0;
                    words.forEach(function(entry) {
                        hltr.setColor(colors[i]);
                        hltr.find(words[i]);
                        i +=1;
                        });
                 });


    });



})();
