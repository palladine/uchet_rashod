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


});