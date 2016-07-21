(function () {
    var removeBtn = document.getElementById('remove'),
        serializeBtn  = document.getElementById('serialize'),
        deserializeBtn  = document.getElementById('deserialize');
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

    serializeBtn.addEventListener('click', function () {
        serialized = hltr.serializeHighlights();
        console.log(serialized);
        hltr.removeHighlights();
    });

    deserializeBtn.addEventListener('click', function () {
        hltr.removeHighlights();
        hltr.deserializeHighlights(serialized);
    });


})();
