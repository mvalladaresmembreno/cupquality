document.onreadystatechange = function () {
    if (document.readyState == "complete") 
    {
        var options = {
            valueNames: [ 'name', 'depto', 'munic', 'coop' ]
          };
          /*table = id of the div */
        var userList = new List('table-list', options);
        
        let searchinput=document.getElementById("Search");
        searchinput.addEventListener("keyup", function(e){
            userList.search(e.target.value);
        });

        let dpto=document.getElementById("departamento");
        let muni=document.getElementById("municipio");
       
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

        var today = new Date();
        var dd = today.getDate();
        var mm = today.getMonth() + 1; //January is 0!
        var yyyy = today.getFullYear()-18;

        if (dd < 10) {
        dd = '0' + dd;
        }

        if (mm < 10) {
        mm = '0' + mm;
        }

        today = yyyy + '-' + mm + '-' + dd;
        document.getElementById("fechaNac").setAttribute("max", today);
    }
}

const rmProd =(event, id)=>
{
    event.preventDefault();
    var req = new XMLHttpRequest();
    req.open("POST", "/rmProd/", true);
    var formData = new FormData(document.querySelector(`form#delete-${id}`));
    formData.append("idProd", id);
    req.onload= ()=>{
        const data=JSON.parse(req.responseText);
        if (data.status === 200){
            document.getElementById(`p-${id}`).remove();
            alert(data.mensaje);
            return false;

        }
        else{
            alert(data.mensaje);
            return false;
        }
        
    }
    if (confirm("¿Esta seguro de eliminar este productor?")==true)
    {
    req.send(formData);
    }
}

const updateProd =(event, id)=>{
    event.preventDefault();
    var req = new XMLHttpRequest();
    req.open("POST", "/updateProd/", true);
    var formData = new FormData(document.querySelector(`form#update-${id}`));
    formData.append("idProd", id);
    var info=Object.fromEntries(formData.entries());
    req.onload= ()=>{
        const data=JSON.parse(req.responseText);
        if (data.status === 200){
            alert(data.mensaje);
            document.getElementById(`name-${id}`).innerHTML=info.fname + " " + info.lname;
            document.getElementById(`dpto-${id}`).innerHTML=data.dpto;
            document.getElementById(`munic-${id}`).innerHTML=data.mun;
            let c=document.getElementById(`close-${id}`);
            c.click();
            return false;
        }
        else{
            alert(data.mensaje);
            return false;
        }
        
    }
    if (confirm("¿Esta seguro de actualizar este productor?")==true)
    {
    req.send(formData);
    }
}

const saveProd = (event)=>{
    event.preventDefault();
    form=document.getElementById("addProd");
    if(document.getElementById("addFincaModal").value == "false")
    {document.getElementById("addFincaModal").value='true';}
    document.getElementById("saveProdbtn").click();
}