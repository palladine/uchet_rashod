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


    // Datalist change values
    const els = document.querySelectorAll('.datalist');
    for (let i = 0; i < els.length; i++){
        els[i].addEventListener('change', function(e){
            var id = e.target.id;
            var form_id = e.target.form.id;
            var list = e.target.getAttribute('list');
            var new_val = document.querySelector("#" + list + " option[value='" + e.target.value + "']").dataset.value;
            var new_input = document.createElement('input');
            new_input.setAttribute('type', 'hidden');
            new_input.setAttribute('name', 'new_'+e.target.name)
            new_input.setAttribute('value', new_val);
            document.getElementById(form_id).appendChild(new_input);
	    });
	}

});