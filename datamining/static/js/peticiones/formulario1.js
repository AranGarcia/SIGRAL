$(function () {
    $('.alert').alert();
    // AJAX para primera consulta
    var form = $('#mdxquery1');
    $(form).submit(function (event) {
        event.preventDefault();

        var formData = $(form).serialize();

        var lanio = parseInt(document.getElementById('lanio').value);
        var ranio = parseInt(document.getElementById('ranio').value);
        if (lanio > ranio) {
            $('#alert_placeholder').html(
                '<div class="alert alert-danger alert-dismissible" role="alert">\
                    Rango de a&ntilde;os inv&aacute;lidos.\
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">\
                        <span aria-hidden="true">&times;</span>\
                    </button>\
                </div>')
            return;
        }

        $.ajax({
            type: 'GET',
            url: $(form).attr('action'),
            data: formData,
            success: function (data, status, jqXHRobj) {
                $('#mdxplot').attr('src', 'data:image/gif;base64,' + data);
            },
            error: function (jqXHRobj, status, excp) {
                // TODO
            }
        })
    })
});