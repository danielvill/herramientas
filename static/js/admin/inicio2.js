document.addEventListener("DOMContentLoaded", function() {
    // Función para convertir la fecha de formato español a un objeto Date de JavaScript
    function parseDate(dateString) {
        const months = {
            "enero": 0, "febrero": 1, "marzo": 2, "abril": 3, "mayo": 4, "junio": 5,
            "julio": 6, "agosto": 7, "septiembre": 8, "octubre": 9, "noviembre": 10, "diciembre": 11
        };

        const parts = dateString.split(", ");
        const dateParts = parts[1].split(" de ");
        const timeParts = parts[2].split(":");

        const day = parseInt(dateParts[0]);
        const month = months[dateParts[1]];
        const year = parseInt(dateParts[2]);
        const hours = parseInt(timeParts[0]);
        const minutes = parseInt(timeParts[1]);
        const seconds = parseInt(timeParts[2].split(" ")[0]);

        return new Date(Date.UTC(year, month, day, hours, minutes, seconds));
    }

    // Función para calcular la diferencia en días entre dos fechas
    function calculateDaysDifference(startDate, endDate) {
        const oneDay = 24 * 60 * 60 * 1000; // Milisegundos en un día
        const diffDays = Math.round(Math.abs((endDate - startDate) / oneDay));
        return diffDays;
    }

    // Inicializar DataTable y agregar evento draw
    const table = $('#myTable5').DataTable();

    table.on('draw', function() {
        // Obtener todas las filas de la tabla
        const rows = document.querySelectorAll("#myTable5 tbody tr");

        rows.forEach(row => {
            const pedidoDateStr = row.querySelector(".pedido").textContent.trim();
            const entregadoDateStr = row.querySelector(".entregado").textContent.trim();
            const mostrarCell = row.querySelector(".mostrar");

            const pedidoDate = parseDate(pedidoDateStr);
            const entregadoDate = parseDate(entregadoDateStr);

            const daysDifference = calculateDaysDifference(pedidoDate, entregadoDate);

            mostrarCell.textContent = daysDifference;
        });
    });

    // Forzar el evento draw para procesar las filas iniciales
    table.draw();
});