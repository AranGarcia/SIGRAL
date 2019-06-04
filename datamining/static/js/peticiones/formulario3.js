$(function () {
    // AJAX para primera consulta
    var form = $('#mdxquery3');
    $(form).submit(function (event) {
        event.preventDefault();
        var formData = $(form).serialize();
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