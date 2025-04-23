document.onreadystatechange = function () {
    if (document.readyState == "complete") 
    {
        var options = {
            valueNames: [ 'name', 'area', 'alt', 'vars', 'certs']
          };
          /*table = id of the div */
          var userList = new List('table-list', options);
    }

    let searchinput=document.getElementById("Search");
    searchinput.addEventListener("keyup", function(e){
        userList.search(e.target.value);
    });

    let finca=document.getElementById("finca");
    finca.addEventListener("change", (e)=>{
        var req = new XMLHttpRequest();
        req.open("GET", "/getajax/getFincaUnidad/"+ e.target.value, true);
        req.onload= ()=>{
            const data=JSON.parse(req.responseText);
            document.getElementById("unidadLote").innerHTML=data.unidad;
        }
        req.send();
        return false;
    });
}
const rmLote =(event, id)=>
{
    event.preventDefault();
    var req = new XMLHttpRequest();
    req.open("POST", "/rmLote/", true);
    var formData = new FormData(document.querySelector(`form#delete-${id}`));
    formData.append("idLote", id);
    req.onload= ()=>{
        const data=JSON.parse(req.responseText);
        if (data.status === 200){
            document.getElementById(`l-${id}`).remove();
            alert(data.mensaje);
            return false;

        }
        else{
            alert(data.mensaje);
            return false;
        }
        
    }
    if (confirm("¿Esta seguro de eliminar este Lote?")==true)
    {
    req.send(formData);
    }
}

const updateLote =(event, id)=>{
    event.preventDefault();
    var req = new XMLHttpRequest();
    req.open("POST", "/updateLote/", true);
    var formData = new FormData(document.querySelector(`form#update-${id}`));
    formData.append("idLote", id);
    var info=Object.fromEntries(formData.entries());
    req.onload= ()=>{
        const data=JSON.parse(req.responseText);
        const varList=document.getElementById(`varList-${id}`);
        const certList=document.getElementById(`certList-${id}`);
        if (data.status === 200){
            alert(data.mensaje);
            document.getElementById(`name-${id}`).innerHTML=info.nameLote;
            document.getElementById(`area-${id}`).innerHTML=info.areaLote;
            document.getElementById(`altitud-${id}`).innerHTML=info.altitudLote;
            if(data.variedades){
                varList.innerHTML="";
                data.variedades.forEach(element => {
                    const li=document.createElement("li");
                    li.innerText=element;
                    varList.appendChild(li);
                });
            }
            if(data.certificaciones){
                certList.innerHTML="";
                data.certificaciones.forEach(element => {
                    const li=document.createElement("li");
                    li.innerText=element;
                    certList.appendChild(li);
                });
            }

            let c=document.getElementById(`close-${id}`);
            c.click();
            return false;
        }
        else{
            alert(data.mensaje);
            return false;
        }
        
    }
    if (confirm("¿Esta seguro de actualizar este lote?")==true)
    {
        req.send(formData);
    }
}