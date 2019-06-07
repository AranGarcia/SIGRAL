$(function () {

    var form = $('#mdxquery5');
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
                crearTabla(res, data);
            },
            error: function (jqXHRobj, status, excp) {
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
    var encabezados = ['#', 'Nombre Producto', 'Cantidad Pedida'];
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
    var colNumero;
    var colNombre;
    var colCantidad;
    var textoNumero;
    var textoNombre;
    var textoCantidad;

    for (const it in data) {
        renglon = document.createElement('tr');
        colNumero = document.createElement('th');
        colNombre = document.createElement('td');
        colCantidad = document.createElement('td');
        colNumero.setAttribute('scope', 'row');

        textoNumero = document.createTextNode(it)
        textoNombre = document.createTextNode(data[it][0]);
        textoCantidad = document.createTextNode(data[it][1]);
        colNumero.appendChild(textoNumero);
        colNombre.appendChild(textoNombre);
        colCantidad.appendChild(textoCantidad);

        renglon.appendChild(colNumero);
        renglon.appendChild(colNombre);
        renglon.appendChild(colCantidad);
        cuerpo.appendChild(renglon);
    }

    tabla.appendChild(cuerpo);

    res.appendChild(tabla);
}