$(function() {
  $('span').addClass("white-cell");
    $('span').click(function() {
      var span= $(this);
      if (span.hasClass("white-cell")) {
        span.toggleClass("white-cell red-cell");
      } else if (span.hasClass("red-cell")) {
        span.toggleClass("red-cell blue-cell");
      } else if (span.hasClass("blue-cell")) {
        span.toggleClass("blue-cell yellow-cell");
      }  else if (span.hasClass("yellow-cell")) {
        span.toggleClass("yellow-cell white-cell");
      }
    });
  });
