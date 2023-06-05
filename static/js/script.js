// Load the header
const headerPlaceholder = document.getElementById("header-placeholder");
const headerURL = "header.html";
fetch(headerURL)
    .then(response => response.text())
    .then(data => {
        headerPlaceholder.innerHTML = data;
    });

let mensajeSWA = (message, icon) => {
    Swal.fire({
        html: `<h3>${message}</h3>`,
        icon: icon,
        confirmButtonText: "Aceptar",
        confirmButtonColor: "green"
    })
}




    // Create Account
function createAccount() {
    const name = document.getElementById('nameInput').value;
    const lastname = document.getElementById('lastNameInput').value;
    const documentId = document.getElementById('documentInput').value;
    const address = document.getElementById('addressInput').value;
    const phone = document.getElementById('phoneInput').value;
    const email = document.getElementById('emailInput').value;
    const date = document.getElementById('dateInput').value;
    const nationality = document.getElementById('nationalityInput').value;
    const employmentSituation = document.getElementById('employmentSituationLst').value;
    const income = parseFloat(document.getElementById('incomeInput').value);
    const initialValue = parseFloat(document.getElementById('initialValueInput').value);
    const password = document.getElementById('passwordInput').value;
    const passwordConfirmation = document.getElementById('passwordConfirmationInput').value;

    if (name == "" || lastname == "" || documentId == "" || address == "" || phone == "" || email == "" || date == "" || employmentSituation == "" || income == "" || password == "" || passwordConfirmation == ""){
        mensajeSWA("Introduzca todos los campos!", "warning")
        return false
    }
    if (password != passwordConfirmation){
        mensajeSWA("las contraseñas no coinciden", "error")
        return false
    }
    Swal.fire({
        html: `<h3>Esta seguro de crear cuenta de ${name + lastname}</h3>`,
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: 'green',
        confirmButtonText: "Si estoy seguro",
        cancelButtonText: "Cancelar",
    }).then((result) => {
        if (result.value) {
            let body = JSON.stringify({
                name,
                lastname,
                documentId,
                address,
                phone,
                email,
                date,
                nationality,
                employmentSituation,
                income,
                initialValue,
                password
        
            })
            fetch('/accounts', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body,
            })
            .then(response => response.json())
            .then(data => {
                Swal.fire({
                    html: `<h3>Cuenta creada satisfactoriamente</h3>`,
                    icon: "success",
                    confirmButtonText: "Aceptar",
                    confirmButtonColor: "green"
                }).then((result) => {
                    if(result.value){
                        location.reload();
                    }
                });
                
            })
            .catch(error => {
                console.log(error);
            });
        }
    })
}

function consultAccount(s){
    const accountNumber = document.getElementById('accountNumber'+s).value;

    if (accountNumber == ""){
        mensajeSWA("Introduzca todos los campos!", "warning")
        return false
    }else{
        let body = JSON.stringify({
            accountNumber
        })
        fetch('/consultAccount', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body,
        })
        .then(response => response.json())
        .then(data => {
            if (data.message == "error"){
                mensajeSWA(data.data, "error")
                return false
            }
            if (data.message == "success"){
                document.getElementById('div1'+s).style.display = 'block';
                document.getElementById('name'+s).value = data.data.nombre + ' ' + data.data.apellido;
                document.getElementById('document'+s).value = data.data.documento;
                document.getElementById('typeAccount'+s).value = data.data.tipoCuenta;
                document.getElementById('stateAccount'+s).value = data.data.estadoCuenta;
                if (data.data.estadoCuenta == "Activa"){
                    document.getElementById('div2'+s).style.display = 'block';
                }
            }
        })
        .catch(error => {
            console.log(error);
        });
    }
}
// Consign
function consign() {
    const name = document.getElementById('depositorNameConsignar').value;
    const documentId = document.getElementById('depositorDocumentConsignar').value;
    const valueConsign = parseFloat(document.getElementById('valueConsignar').value);
    const accountNumber = document.getElementById('accountNumberConsignar').value;

    if (name == "" || documentId == "" || valueConsign == ""){
        mensajeSWA("Introduzca todos los campos!", "warning")
        return false
    }
    if (valueConsign <= 0){
        mensajeSWA("Valor invalido para consignar", "error")
        return false
    }else{
        let body = JSON.stringify({
            name,
            documentId,
            valueConsign,
            accountNumber
        })
        fetch('/consign', {  
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body,
        })
        .then(response => response.json())
        .then(data => {
            if (data.message == "error"){
                mensajeSWA(data.data, "error")
                return false
            }
            if (data.message == "success"){
                Swal.fire({
                    html: `<h3>Consignacion realizada satisfactoriamente</h3>`,
                    icon: "success",
                    confirmButtonText: "Aceptar",
                    confirmButtonColor: "green"
                }).then((result) => {
                    if(result.value){
                        location.reload();
                    }
                });
            }

        })
        .catch(error => {
            console.log(error);
        });

    }

}

// Withdraw
function withdraw() {
    const valueRetirar = parseFloat(document.getElementById('valueRetirar').value);
    const accountNumber = document.getElementById('accountNumberRetirar').value;

    if (valueRetirar == ""){
        mensajeSWA("Introduzca todos los campos!", "warning")
        return false
    }
    if (valueRetirar <= 0){
        mensajeSWA("Valor invalido para retirar", "error")
        return false
    }else{
        let body = JSON.stringify({
            valueRetirar,
            accountNumber
        })
        fetch('/withdraw', {  
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body,
        })
        .then(response => response.json())
        .then(data => {
            if (data.message == "error"){
                mensajeSWA(data.data, "error")
                return false
            }
            if (data.message == "success"){
                Swal.fire({
                    html: `<h3>Retiro realizado satisfactoriamente</h3>`,
                    icon: "success",
                    confirmButtonText: "Aceptar",
                    confirmButtonColor: "green"
                }).then((result) => {
                    if(result.value){
                        location.reload();
                    }
                });
            }

        })
        .catch(error => {
            console.log(error);
        });

    }
}

// Check Balance
function checkBalance() {
    const accountNumber = document.getElementById('accountNumberConsultar').value;

    let body = JSON.stringify({
        accountNumber
    })
    fetch('/balance', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body,
    })
    .then(response => response.json())
    .then(data => {
        if (data.message == "error"){
            mensajeSWA(data.data, "error")
            return false
        }
        if (data.message == "success"){
            document.getElementById('valueConsultar').value = data.data
        }

    })
    .catch(error => {
        console.log(error);
    });
}
