$(document).ready(function () {
    $('#myTable').DataTable({
    "language": {
            "url": "/static/js/Spanish.json"
        }
    });
    var table = $('#myTable').DataTable();
    //Cambio de english a spanish
    // Funcionalidad de edición
    table.on('click', '.editar', function () {
        var row = $(this).closest('tr');
        var data = table.row(row).data();
        // Aquí puedes abrir el modal y llenar los campos del formulario con los datos del usuario
        // Por ejemplo:
        $('#id_h').val(data[0]);
        $('#codigo').val(data[1]);
        $('#nombre_h').val(data[2]);
        $('#stock').val(data[3]);
        $('#comentario').val(data[4]);
       // $('#imagen').val(data[5]);
        $('#editForm').attr('action','/edit_pr/'+ data[0]); // Recuerda que en esta parte el 0 es la posicion selectora del codigo que estas usando en este caso es 0 ya que usas la cedula
        $('#editModal').dialog('open');
    });
    // Inicializar el modal
    $('#editModal').dialog({
        autoOpen: false,
        modal: true,
        buttons: [
            {
                text: 'Guardar',
                click: function () {
                    $('#editForm').submit();
                },
                // Agregar una clase al botón
                class: 'guardar'
            },
            {
                text: 'Cancelar',
                click: function () {
                    $(this).dialog('close');
                },
                // Agregar una clase al botón
                class: 'cancelar'
            }
        ]
    });
});
$(".eliminar").click(function (event) {
    event.preventDefault();
    var url = $(this).attr('href'); // Guarda la URL del enlace
    Swal.fire({
        title: '¿Estás seguro?',
        text: "¿Estás seguro de que quieres eliminar?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, eliminar!',
        cancelButtonText: 'No, cancelar!'
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = url; // Navega a la URL del enlace
        }
    });
});