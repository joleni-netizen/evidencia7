async function registrarUsuario() {
    const url = "http://127.0.0.1:8000/registro"; // URL del endpoint

    const datos = {
        id:0,
        nombre_completo: document.getElementById("nombre").value,
        correo: document.getElementById("correo").value,
        clave: document.getElementById("clave").value
    };

    try {
        const respuesta = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(datos)
        });

        if (!respuesta.ok) {
            alert(`Error: ${respuesta.status} - ${respuesta.statusText}`)
            throw new Error(`Error: ${respuesta.status} - ${respuesta.statusText}`);
        }

        const resultado = await respuesta.json();
        alert("Usuario registrado con éxito:", resultado);
        return resultado;
    } catch (error) {
        alert("Error en el registro:", error);
        return null;
    }
}


async function iniciarSesionUsuario() {
    const url = "http://127.0.0.1:8000/login"; // URL del endpoint

    const datos = {
        correo: document.getElementById("correo").value,
        clave: document.getElementById("clave").value
    };

    try {
        const respuesta = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(datos)
        });

        if (!respuesta.ok) {
            alert(`Error: ${respuesta.status} - ${respuesta.statusText}`)
            throw new Error(`Error: ${respuesta.status} - ${respuesta.statusText}`);
        }

        const resultado = await respuesta.json();
        alert("Usuario ingresado con éxito:", resultado);
        return resultado;
    } catch (error) {
        alert("Error en el registro:", error);
        return null;
    }
}