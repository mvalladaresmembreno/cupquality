document.onreadystatechange = function () {
    if (document.readyState == "complete") 
    {
        let dpto=document.getElementById("departamento");
        let muni=document.getElementById("municipio");
        dpto.addEventListener("change", function(e){
            var selected=[];
            for (var i = 0; i < dpto.options.length; i++) {
                if (dpto.options[i].selected) {
                    selected.push(dpto.options[i].value);
                }}
            if (selected.length>0){
                selected=JSON.parse(JSON.stringify(selected));
                const request = new XMLHttpRequest();
                request.open("GET", `/getajax/get_municipios/${selected}`, true);
                request.onload= ()=>{
                    const template = Handlebars.compile("<option default value=\"\">Seleccione el Municipio</option>");
                    optiondef = template();   
                    muni.innerHTML="";
                    // muni.innerHTML+=optiondef;
                    const data=JSON.parse(request.responseText);
                    if (data.municipios){
                        data.municipios.forEach(element => {
                            var option=document.createElement("option");
                            option.text=element[0];
                            option.value=element[1];
                            muni.appendChild(option);
                        });
                    }
                }
                request.send();
                return false;
            }

        });
    }
};

const filtrar = (event) =>{
    event.preventDefault();
    var req = new XMLHttpRequest();
    req.open("POST", "/filtros/",true);
    var formData = new FormData(document.querySelector(`form#filtros`));
    req.onload= ()=>{
        console.log(req.responseText);
        if (req.responseText){
            const data=JSON.parse(req.responseText);
            if (data.status===200){
                console.log(data);
            }
            else if (data.status===404){
                console.log("Solicitud Vacia");
            }
            else{
                console.log("Error");
            }
        }
        else{
            console.log("No hay respuesta");
        }
    }
    req.send(formData);
}