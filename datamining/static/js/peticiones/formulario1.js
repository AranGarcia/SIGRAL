$(function () {
    var form = $('#mdxquery1');

    $(form).submit(function (event) {
        event.preventDefault();

        var formData = $(form).serialize();

        $.ajax({
            type: 'GET',
            url: $(form).attr('action'),
            data: formData,
            success: function (data, status, jqXHRobj) {
                // TODO
            },
            error: function(jqXHRobj, status, excp){
                // TODO
            }
        })
    })
});