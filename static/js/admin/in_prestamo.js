$('#myTable').DataTable({
    "language": {
        "url": "/static/js/Spanish.json"
    }
});
$('#myTable2').DataTable({
    "language": {
        "url": "/static/js/Spanish.json"
    }
});
$(document).ready(function () {
    // Para el primer botón
    $('.but1').click(function () {
        $('.mosempleado').dialog({
            title: "Seleccionar Empleado",
            width: 500,
            modal: true
        });
    });

    // Para el segundo botón
    $('.but2').click(function () {
        $('.mosherra').dialog({
            title: "Seleccionar Herramienta",
            width: 500,
            modal: true
        });
    });
});


// Copia los datos de una celda para otra
$(document).ready(function () {
    $('#myTable tbody').on('click', 'button', function () {
        var row = $(this).closest('tr');
        var empleado = $.trim(row.find('.valor1').text());
        var cedula = $.trim(row.find('.valor2').text());

        $('.empleado').val(empleado);
        $('.cedula').val(cedula);
    });
});
// Copia los datos de la segunda celda
$(document).ready(function () {
    $('#myTable2 tbody').on('click', 'button', function () {
        var row = $(this).closest('tr');
        var codigo = $.trim(row.find('.var1').text());
        var nombre = $.trim(row.find('.var2').text());
        var cantidad = $.trim(row.find('.var3').text());
        var id_h = $.trim(row.find('.var4').text());

        $('.codigo').val(codigo);
        $('.nombre').val(nombre);
        $('.cantidad').val(cantidad);
        $('.id_h').val(id_h);
    });
});


// Valor de cantidad no se enviará si está en cero
document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form"); // Asumiendo que solo hay un formulario
    form.addEventListener("submit", function (event) {
        const inputCantidad = document.querySelector(".cantidad");
        const cantidad = inputCantidad.value;
        if (cantidad === "0") {
            event.preventDefault(); // Evita que el formulario se envíe
            inputCantidad.style.backgroundColor = "red"; // Cambia el fondo a rojo
            inputCantidad.style.color = "white"; // Cambia el fondo a rojo
            
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'No se puede enviar un valor que se encuentra en cero'
            });
        } else {
            inputCantidad.style.backgroundColor = ""; // Restablece el fondo si no es cero
        }
    });
});

