document.onreadystatechange = function () 
{
    if (document.readyState == "complete")
    {
        //Función para validar el check y los campos
        const tamizados = document.querySelectorAll(".tamizados");
        const defectos1 = document.querySelectorAll(".defectost1");
        const defectos2 = document.querySelectorAll(".defectost2");
        const pesosDefectos=document.querySelectorAll(".dPesos");
        tamizados.forEach( (e) => { 
          e.addEventListener("change", calcularTamiz);
          e.addEventListener("keyup", calcularTamiz);
        });
        defectos1.forEach( (e) => {
          e.addEventListener("change", activarDefectos);
        } );
        defectos2.forEach( (e) => {
          e.addEventListener("change", activarDefectos);
        } );
       pesosDefectos.forEach( (e) => {
          e.addEventListener("change", calcularDefectos);
          e.addEventListener("keyup", calcularDefectos);
        } );

    }
}

var calcularTamiz = (event) =>
{
    let element=event.target;
    let id=element.dataset.muestra;
    let total=0;
    let pesoTamiz=parseFloat(document.getElementById("pesoTamiz_"+id).value);
    let porcentajeTotal=0;
    if( parseFloat(element.value) > pesoTamiz)
    {
      element.value = element.value / 10;
    }
    let porcentaje = (parseFloat(element.value)*100) / pesoTamiz;
    document.getElementById("POR_"+element.id).value = porcentaje.toFixed(2);

    let tamizados = document.querySelectorAll(".tamizados");
    tamizados.forEach( (e) => {
    if (e.dataset.muestra==id)
    {
        total+=parseFloat(e.value);
        document.getElementById("PCtotal_"+id).value = total.toFixed(2);
        porcentajeTotal += parseFloat(document.getElementById("POR_"+e.id).value);
        document.getElementById("PORtotal_"+id).value = porcentajeTotal.toFixed(2);
    }
    } );
  
};

var calcularDefectos = (event) =>
{
    let element=event.target;
    let id=element.dataset.muestra;
    let total=0;
    let porcentajeTotal=0;
    let pesoMuestra=parseFloat(document.getElementById("peso-"+id).value);
    let defecto=element.name.split("_");
    defecto=defecto[1];
    document.getElementById("POR_"+defecto+"_"+id).value= ((parseFloat(element.value)*100) / pesoMuestra).toFixed(2);
    let pesos=document.querySelectorAll(".dPesos");
    pesos.forEach( (e) => {
    if (e.dataset.muestra==id)
    {
      total+=parseFloat(e.value);
      document.getElementById("pDefectos-"+id).value = total.toFixed(2);
      document.getElementById("pDefectos-D-"+id).innerHTML = total.toFixed(2);
      porcentajeTotal = (parseFloat(document.getElementById("pDefectos-"+id).value)*100)/pesoMuestra;
      document.getElementById("por-"+id).innerHTML = porcentajeTotal.toFixed(2);
      document.getElementById("POR_D_"+id).value = porcentajeTotal.toFixed(2);
      }
    } );

    
}

var activarDefectos = (event) =>
{
    let element=event.target;
    if(element.checked){
      document.getElementById("E_"+element.id).readOnly = false;
      document.getElementById("P_"+element.id).readOnly = false;
      document.getElementById("D_"+element.id).readOnly = false;
    }
    else{
      document.getElementById("E_"+element.id).readOnly = true;
      document.getElementById("P_"+element.id).readOnly = true;
      document.getElementById("D_"+element.id).readOnly = true;
      document.getElementById("E_"+element.id).value = "0";
      document.getElementById("P_"+element.id).value = "0";
      document.getElementById("POR_"+element.id).value = "0";
      document.getElementById("D_"+element.id).value = "0";
      document.getElementById("P_"+element.id).dispatchEvent(new Event('change'));
    }

}

const saveFisica = (event, idMuestra)=>{
  event.preventDefault();
  const form = new FormData(document.getElementById("addFisico_"+idMuestra));
  form.append('idMuestra', idMuestra);
  const request = new XMLHttpRequest();
  request.open('POST', '/lab/saveFisico');
  request.onload = ()=>{
      const data=JSON.parse(request.responseText);
      if (data.status==200){
              alert(data.mensaje);
              for (e in form.elements)
              {
                e.readOnly=true;
              }
              document.getElementById(`save-${idMuestra}`).onclick=null;
              document.getElementById(`save-${idMuestra}`).parentElement.style.backgroundColor="black";
              document.getElementById(`save-${idMuestra}`).parentElement.style.color="white";
              document.getElementById(`save-${idMuestra}`).style.color="white";
              document.getElementById(`save-${idMuestra}`).style.cursor="not-allowed";
              document.getElementById(`save-${idMuestra}`).after="";
              document.getElementById(`save-${idMuestra}`).innerHTML="Guardado";
      }else{
          alert(data.mensaje);
          return false;
      }
  }
  request.send(form);
}