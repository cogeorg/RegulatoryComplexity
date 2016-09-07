
/* On-Off button (Show and hide div1/div2)*/
    $(document).ready(function () {
        $('.group').hide();
        $('#div1').show();
        $('#selectMe').change(function () {
            $('.group').hide();
            $('#'+$(this).val()).show();
        })
    });
    /* ******************** */

/* Git images while loading*/
  $(document).on({
        ajaxStart: function() { $("body").addClass("loading");    },
        ajaxStop: function() { $("body").removeClass("loading"); }
    });
/* ******************** */
