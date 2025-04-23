document.onreadystatechange = function () {
    if (document.readyState === 'complete') {
        var today = new Date();
        var dd = today.getDate();
        var mm = today.getMonth() + 1; //January is 0!
        var yyyy = today.getFullYear();

        if (dd < 10) {
          dd = '0' + dd;
        }

        if (mm < 10) {
          mm = '0' + mm;
        }

        today = yyyy + '-' + mm + '-' + dd;
        document.getElementById("fechaEntregado").setAttribute("max", today); 
        document.getElementById("fechaEntregado").value=today;

        const stepButtons = document.querySelectorAll('.step-button');
        const progress = document.querySelector('#progress');

        Array.from(stepButtons).forEach((button,index) => {
            button.addEventListener('click', () => {
                progress.setAttribute('value', index * 100 /(stepButtons.length - 1) );//there are 3 buttons. 2 spaces.

                stepButtons.forEach((item, secindex)=>{
                    if(index > secindex){
                        item.classList.add('done');
                    }
                    if(index < secindex){
                        item.classList.remove('done');
                    }
                })
            })
        });

        let prod=document.getElementById("productor");
        let finca=document.getElementById("finca");
        let lote=document.getElementById("lote");

        prod.addEventListener("change", function(e){
            let idProd=e.target.value;
            const request = new XMLHttpRequest();
            request.open('GET', '/getajax/get_finca/'+idProd);
            request.onload = ()=>{
                const template = Handlebars.compile("<option default value=\"\">Seleccione la Finca</option>");
                optiondef = template();   
                finca.innerHTML="";
                finca.innerHTML+=optiondef;
                const data=JSON.parse(request.responseText);
                if (data.fincas){
                    data.fincas.forEach(element => {
                        var option=document.createElement("option");
                        option.text=element[1];
                        option.value=element[0];
                        finca.appendChild(option);
                    });
                }
            }
            request.send();
            return false;
        });

        finca.addEventListener("change", function(e){
            let idFinca=e.target.value;
            const request = new XMLHttpRequest();
            request.open('GET', '/getajax/get_lote/'+idFinca);
            request.onload = ()=>{
                const template = Handlebars.compile("<option default value=\"\">Seleccione Lote</option>");
                optiondef = template();   
                lote.innerHTML="";
                lote.innerHTML+=optiondef;
                const data=JSON.parse(request.responseText);
                if (data.lotes){
                    data.lotes.forEach(element => {
                        var option=document.createElement("option");
                        option.text=element[1];
                        option.value=element[0];
                        lote.appendChild(option);
                    });
                }
            }
            request.send();
            return false;
        });

        document.getElementById("aFisico").addEventListener("change", () => {
            if (document.getElementById("aFisico").checked == true)
            {
                document.getElementById("iaFisico").classList.toggle("change-color");
            }
            else
            {
                document.getElementById("iaFisico").classList.toggle("change-color");
            }
        });
        document.getElementById("aSensorial").addEventListener("change", () => {
            if (document.getElementById("aSensorial").checked == true)
            {
                document.getElementById("iaSensorial").classList.toggle("change-color");
            }
            else
            {
                document.getElementById("iaSensorial").classList.toggle("change-color");
            }
        });

        validaciones();

        let sw = document.getElementById("sBueno");
        sw.addEventListener("change", () => {
            if (sw.checked == true ) {
                document.querySelectorAll(".habilitador").forEach(item => {
                    item.disabled = true;
                    item.checked = false;
                });
            } else {
                document.querySelectorAll(".habilitador").forEach(item => {
                    item.disabled = false;
                });
            }
        });
        
        function validarSW(){
            if (sw.checked == true ) {
                document.querySelectorAll(".habilitador").forEach(item => {
                    item.disabled = true;
                    item.checked = false;
                });
            } else {
                document.querySelectorAll(".habilitador").forEach(item => {
                    item.disabled = false;
                });
            }
        }

        validarSW();
       
        
        function validar(){
            if (document.getElementById("sRoto").checked == true || document.getElementById("sOlores").checked == true || document.getElementById("sDerrames").checked == true)
            {
                if (sw.disabled == false)
                {
                    sw.disabled = true;     
                }
            } 
            else
            {
                if (sw.disabled == true)
                {
                    sw.disabled = false;     
                }
            }
        }
        document.querySelectorAll(".habilitador").forEach(e => {
            e.addEventListener("change", validar);
        } );

        validar();
        
        let aceptación=document.getElementById("toggleAM");
        aceptación.addEventListener("click", () => {
            if (aceptación.checked == true)
            {
                document.getElementById("aceptacionMuestra").value ="1";
            }
            else
            {
                document.getElementById("aceptacionMuestra").value ="0";
            }
        });
    }
}
function clic1(){
    document.getElementById("step1").click()
}
function clic2(){
    document.getElementById("step2").click()
}

function validaciones(){
    if (document.getElementById("aFisico").checked == true)
    {
        document.getElementById("iaFisico").classList.toggle("change-color");
    }

    if (document.getElementById("aSensorial").checked == true)
    {
        document.getElementById("iaSensorial").classList.toggle("change-color");
    }
}



const saveMuestra = (event, nuevo)=>{
    event.preventDefault();
    const form = new FormData(document.querySelector("form#addMuestra"));
    const request = new XMLHttpRequest();
    request.open('POST', '/muestras/addMuestra');
    request.onload = ()=>{
        const data=JSON.parse(request.responseText);
        if (data.status==200){
            if(nuevo==true){
                document.querySelector("form#addMuestra").reset();
                document.getElementById("step1").click();
            }else{
                window.location.replace("/muestras/");
            }
        }else{
            alert(data.mensaje);
            return false;
        }
    }
    if (confirm("¿Ha revisado bien el formulario?")==true)
    {
        request.send(form);
    }
}

const editMuestra = (event, idMuestra)=>{
    event.preventDefault();
    const form = new FormData(document.querySelector("form#editMuestra"));
    const request = new XMLHttpRequest();
    request.open('POST', '/muestras/editMuestra/'+idMuestra.toString());
    request.onload = ()=>{
        const data=JSON.parse(request.responseText);
        if (data.status==200){
                alert(data.mensaje);
                window.location.replace("/muestras/editMuestra/"+idMuestra.toString());
        }else{
            alert(data.mensaje);
            return false;
        }
    }
    if (confirm("¿Ha revisado bien el formulario?")==true)
    {
        request.send(form);
    }
}