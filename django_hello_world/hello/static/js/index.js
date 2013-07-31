$(document).ready(function() {
    var options = {
        target: '#ajaxwrapper',
        beforeSubmit: pre_submit,
        success: post_submit
    };
    $('#contactform').ajaxForm(options)

    $('#id_photo').change(function(){
        $('#photo_preview').attr('src', $('#id_photo').val())
    });
});

function pre_submit(formData, jqForm, options) {
    $('#formstatus').html('Sending form...');
    $('#btnsubmit').attr('disabled', true);
    $('#btncancel').attr('disabled', true);
    return true;
}

function post_submit(responseText, statusText, xhr, $form)  {
    $('#btnsubmit').attr('disabled', false);
    $('#btncancel').attr('disabled', false);
}