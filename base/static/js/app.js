$(document).ready(
function() {

    // textfile field click
    $('#textfile').on('click', function() {
    $('#file').click();
    return false; });


    // file field to textfile field
    $('#file').on('change', function() {
            var vl = $('#file').val()
            if (vl == "")
                {
                    $("#textfile").val("");
                }
            else
                {
                    var ts = vl.split('\\');
                    $("#textfile").val(ts[ts.length-1]);
                }
        });
    //////////////////////////////////


    // textfile field to file field
    $('#textfile').on('change', function() {
            var vl = $('#textfile').val()
            if (vl == "")
                {
                    $("#file").val("");
                }
            else
                {
                    var ts = vl.split('\\');
                    $("#file").val(ts[ts.length-1]);
                }
        });
    //////////////////////////////////


//    // AJAX
//
//    function getCookie(c_name)
//    {
//        if (document.cookie.length > 0)
//        {
//            c_start = document.cookie.indexOf(c_name + "=");
//            if (c_start != -1)
//            {
//                c_start = c_start + c_name.length + 1;
//                c_end = document.cookie.indexOf(";", c_start);
//                if (c_end == -1) c_end = document.cookie.length;
//                return unescape(document.cookie.substring(c_start,c_end));
//            }
//        }
//        return "";
//     }
//
//
//    $('#form_addtable').on('submit', function(e) {
//        e.preventDefault();
//        var dataform = $(this).serialize();
//        console.log(dataform);
//
//        $.ajax({
//          headers: { "X-CSRFToken": getCookie("csrftoken") },
//          type: "POST",
//          contentType: 'application/json; charset=utf-8',
//          url: "/base/add_supply",
//          data: {'dform': dataform},
//          success:function(res){console.log(res)},
//          error:function(res){console.log(res)}
//        });
//        return false;
//    });



});