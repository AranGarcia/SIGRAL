$(function () {
    // AJAX para cuarta consulta
    var form = $('#mdxquery4');
    var res = document.getElementById("resultados");

    $(form).submit(function (event) {
        event.preventDefault();
        var formData = $(form).serialize();
        $.ajax({
            type: 'GET',
            url: $(form).attr('action'),
            data: formData,
            success: function (data, status, jqXHRobj) {
                borrarTabla(res);
                crearTabla(res, data['antiguedades']);
            },
            error: function (jqXHRobj, status, excp) {
                // TODO
            }
        })
    })
});

function borrarTabla(tab) {
    while (tab.firstChild) {
        tab.firstChild.remove();
    }
}

function crearTabla(res, data) {
    var tabla = document.createElement('table');
    tabla.setAttribute('class', 'table table-striped');

    // Cabecera de la tabla
    var cabecera = document.createElement('thead');
    var encabezados = ['Proveedor desde', 'Nombre'];
    var rengCabecera = document.createElement('tr');
    var colEnc;
    var col_texto;
    for (const i of encabezados) {
        colEnc = document.createElement('th');
        col_texto = document.createTextNode(i);
        colEnc.setAttribute('scope', 'col');
        colEnc.appendChild(col_texto);
        rengCabecera.appendChild(colEnc);
    }
    cabecera.appendChild(rengCabecera);
    tabla.appendChild(cabecera);

    // Datos de la tabla
    var cuerpo = document.createElement('tbody');
    var renglon;
    var colFecha;
    var colNombres;
    var textoFecha;
    var textoNombres;
    for (const it of data) {
        renglon = document.createElement('tr');
        colFecha = document.createElement('th');
        colNombres = document.createElement('td');
        colFecha.setAttribute('scope', 'row');

        textoFecha = document.createTextNode(it['fecha']);
        textoNombres = document.createTextNode(it['proveedor']);
        colFecha.appendChild(textoFecha);
        colNombres.appendChild(textoNombres);

        renglon.appendChild(colFecha);
        renglon.appendChild(colNombres);
        cuerpo.appendChild(renglon);
    }

    tabla.appendChild(cuerpo);

    res.appendChild(tabla);
}