// Función para convertir la fecha a un formato manejable y calcular los días de demora
function calcularDiasDemora(fechaPrestamo) {
    // Convertir la fecha de prestamo a un objeto Date
    let fecha = new Date(fechaPrestamo);

    // Verificar si la fecha es válida
    if (isNaN(fecha)) {
        return "Fecha inválida";
    }

    // Obtener la fecha actual
    let fechaActual = new Date();

    // Calcular la diferencia en milisegundos
    let diferenciaMilisegundos = fechaActual - fecha;

    // Convertir la diferencia de milisegundos a días
    let diasDemora = Math.floor(diferenciaMilisegundos / (1000 * 60 * 60 * 24));

    return diasDemora;
}
// Esta es para convertir la fecha y obtener los dias con la fecha actual
function convertirFecha(fechaTexto) {
    // Extraer los componentes de la fecha, incluyendo días con caracteres especiales
    let partes = fechaTexto.match(/(\w+), (\d{1,2}) de (\w+) de (\d{4}), (\d{1,2}:\d{2}:\d{2})/u);
    console.log("Partes extraídas:", partes); // <-- Añadir aquí

    if (!partes) return "Fecha inválida";

    let dia = partes[2].padStart(2, '0');
    let mes = partes[3];
    let año = partes[4];
    let hora = partes[5];

    // Convertir el nombre del mes a número
    const meses = {
        "enero": "01",
        "febrero": "02",
        "marzo": "03",
        "abril": "04",
        "mayo": "05",
        "junio": "06",
        "julio": "07",
        "agosto": "08",
        "septiembre": "09",
        "octubre": "10",
        "noviembre": "11",
        "diciembre": "12"
    };

    let mesNumero = meses[mes.toLowerCase()];
    console.log("Mes convertido a número:", mesNumero); // <-- Añadir aquí

    if (!mesNumero) return "Fecha inválida";

    // Formatear la fecha a ISO
    let fechaISO = `${año}-${mesNumero}-${dia}T${hora}Z`;
    console.log("Fecha en formato ISO:", fechaISO); // <-- Añadir aquí

    return fechaISO;
}

// Esta es para convertir la fecha de Miercoles 
function convertimiercoles(fechaTexto) {
    // Extraer los componentes de la fecha, incluyendo días con caracteres especiales
    let partes = fechaTexto.match(/(miércoles), (\d{1,2}) de (\w+) de (\d{4}), (\d{1,2}:\d{2}:\d{2})/u);
    console.log("Partes extraídas (miércoles):", partes); // <-- Añadir aquí

    if (!partes) return "Fecha inválida";

    let dia = partes[2].padStart(2, '0');
    let mes = partes[3];
    let año = partes[4];
    let hora = partes[5];

    // Convertir el nombre del mes a número
    const meses = {
        "enero": "01",
        "febrero": "02",
        "marzo": "03",
        "abril": "04",
        "mayo": "05",
        "junio": "06",
        "julio": "07",
        "agosto": "08",
        "septiembre": "09",
        "octubre": "10",
        "noviembre": "11",
        "diciembre": "12"
    };

    let mesNumero = meses[mes.toLowerCase()];
    console.log("Mes convertido a número (miércoles):", mesNumero); // <-- Añadir aquí

    if (!mesNumero) return "Fecha inválida";

    // Formatear la fecha a ISO
    let fechaISO = `${año}-${mesNumero}-${dia}T${hora}Z`;
    console.log("Fecha en formato ISO (miércoles):", fechaISO); // <-- Añadir aquí

    return fechaISO;
}

function actualizarTabla() {
    // Obtener la tabla con el id myTable3
    let tabla = document.getElementById("myTable3");

    // Obtener todas las filas de la tabla
    let filas = tabla.querySelectorAll("tbody tr");

    // Recorrer cada fila
    filas.forEach(fila => {
        // Obtener la fecha de prestamo
        let fechaPrestamoTexto = fila.querySelector(".prestamo_1").textContent.trim();
        console.log("Fecha de préstamo (texto):", fechaPrestamoTexto); // <-- Añadir aquí
        
        // Verificar si la fecha contiene "miércoles"
        let fechaPrestamoISO;
        if (fechaPrestamoTexto.includes("miércoles")) {
            fechaPrestamoISO = convertimiercoles(fechaPrestamoTexto);
        } else {
            fechaPrestamoISO = convertirFecha(fechaPrestamoTexto);
        }
        console.log("Fecha de préstamo (ISO):", fechaPrestamoISO); // <-- Añadir aquí
        
        // Verificar si la fecha es válida
        if (fechaPrestamoISO !== "Fecha inválida") {
            // Calcular los días de demora
            let diasDemora = calcularDiasDemora(fechaPrestamoISO);
            console.log("Días de demora:", diasDemora); // <-- Añadir aquí
            // Mostrar los días de demora en la columna correspondiente
            fila.querySelector(".respuesta").textContent = diasDemora;
        } else {
            fila.querySelector(".respuesta").textContent = "Fecha inválida";
        }
    });
}

// Inicializar DataTables y escuchar el evento draw
$(document).ready(function() {
    let table = $('#myTable3').DataTable();

    // Llamar a la función para actualizar la tabla al cargar la página
    actualizarTabla();

    // Escuchar el evento draw de DataTables
    table.on('draw', function() {
        actualizarTabla();
    });
});
