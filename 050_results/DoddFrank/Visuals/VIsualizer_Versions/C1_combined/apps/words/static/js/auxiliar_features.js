
/* On-Off button (Show and hide div1/div2)*/
    $(document).ready(function () {
        /* Default view preclass titles (div1)*/
        $('.group').hide();
        $('#div1').show();
        $('#selectMe').change(function () {
            $('.group').hide();
            /* Change div*/
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
