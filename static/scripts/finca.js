document.onreadystatechange = function () {
    if (document.readyState == "complete") 
    {
        var options = {
            valueNames: [ 'name', 'area', 'dpto', 'muni', 'com']
          };
          /*table = id of the div */
        var userList = new List('table-list', options);


        let searchinput=document.getElementById("Search");
        searchinput.addEventListener("keyup", function(e){
            userList.search(e.target.value);
        });

        let dpto=document.getElementById("departamento");
        let muni=document.getElementById("municipio");
        let com=document.getElementById('comunidad');
       
        dpto.addEventListener("change", function(e){
            let dptoid=e.target.value;
            const request = new XMLHttpRequest();
            request.open("GET", "/getajax/get_municipio/"+dptoid, true);
            request.onload= ()=>{
                const template = Handlebars.compile("<option default value=\"\">Seleccione el Municipio</option>");
                optiondef = template();   
                muni.innerHTML="";
                muni.innerHTML+=optiondef;
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
        });
        muni.addEventListener("change", function(e){
            let muniid=e.target.value;
            const request = new XMLHttpRequest();
            request.open("GET", "/getajax/get_comunidad/"+muniid, true);
            request.onload= ()=>{
                const template = Handlebars.compile("<option default value=\"\">Seleccione la Comunidad</option>");
                optiondef = template();   
                com.innerHTML="";
                com.innerHTML+=optiondef;
                const data=JSON.parse(request.responseText);
                if (data.comunidades){
                    data.comunidades.forEach(element => {
                        var option=document.createElement("option");
                        option.text=element[0];
                        option.value=element[1];
                        com.appendChild(option);
                    });
                }
            }
            request.send();
            return false;
        });
    }
    let sw = document.getElementById("toggle");
    sw.addEventListener("click", ()=>{
        if(sw.checked == true)
        {
            document.getElementById("unidadFinca").value="Mz";
        }
        else{
            document.getElementById("unidadFinca").value="Ha";
        }
    });
}

const rmFinca =(event, id)=>
{
    event.preventDefault();
    var req = new XMLHttpRequest();
    req.open("POST", "/rmFinca/", true);
    var formData = new FormData(document.querySelector(`form#delete-${id}`));
    formData.append("idFinca", id);
    req.onload= ()=>{
        const data=JSON.parse(req.responseText);
        if (data.status === 200){
            document.getElementById(`f-${id}`).remove();
            alert(data.mensaje);
            return false;

        }
        else{
            alert(data.mensaje);
            return false;
        }
        
    }
    if (confirm("¿Esta seguro de eliminar esta Finca?")==true)
    {
    req.send(formData);
    }
}

const updateFinca =(event, id)=>{
    event.preventDefault();
    var req = new XMLHttpRequest();
    req.open("POST", "/updateFinca/", true);
    var formData = new FormData(document.querySelector(`form#update-${id}`));
    formData.append("idFinca", id);
    var info=Object.fromEntries(formData.entries());
    req.onload= ()=>{9
        const data=JSON.parse(req.responseText);
        if (data.status === 200){
            alert(data.mensaje);
            document.getElementById(`name-${id}`).innerHTML=info.nameFinca;
            document.getElementById(`area-${id}`).innerHTML=info.areaFinca;
            document.getElementById(`dpto-${id}`).innerHTML=data.dpto;
            document.getElementById(`munic-${id}`).innerHTML=data.munic;
            document.getElementById(`com-${id}`).innerHTML=data.com;
            let c=document.getElementById(`close-${id}`);
            c.click();
            return false;
        }
        else{
            alert(data.mensaje);
            return false;
        }
        
    }
    if (confirm("¿Esta seguro de actualizar esta finca?")==true)
    {
    req.send(formData);
    }
}
const saveFinca = (event)=>{
    event.preventDefault();
    if(document.getElementById("addLoteModal").value == "false")
    {document.getElementById("addLoteModal").value='true';}
    document.getElementById("saveFincabtn").click();
}

if(document.getElementById("toggle").checked == true)
{
    document.getElementById("unidadFinca").value="Mz";
}
else{
    document.getElementById("unidadFinca").value="Ha";
}