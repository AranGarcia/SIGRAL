$(function () {
    // AJAX para primera consulta
    var form = $('#mdxquery2');
    $(form).submit(function (event) {
        event.preventDefault();

        $.ajax({
            type: 'GET',
            url: $(form).attr('action'),
            success: function (data, status, jqXHRobj) {
                $('#mdxplot').attr('src', 'data:image/gif;base64,' + data);
            },
            error: function (jqXHRobj, status, excp) {
                // TODO
            }
        })
    })
});