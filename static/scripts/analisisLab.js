var sabores, aromas, aSabores={}, aAromas={};

document.onreadystatechange = function () {
    if (document.readyState == "complete") {
        
        ids.forEach((id)=>{
            aSabores['badgeSabor-'+id]=[];
            aAromas['badgeAroma-'+id]=[];
            aSabores['badgeSabor-'+id+'-selected']=[];
            aAromas['badgeAroma-'+id+'-selected']=[];
        });

        if (document.querySelectorAll('select[name=sabores]') != null && document.querySelectorAll('select[name=aromas]') != null) {
            sabores=document.querySelectorAll('select[name=sabores]');
            aromas=document.querySelectorAll('select[name=aromas]');
            sabores.forEach((sabor)=>{
                sabor.addEventListener('optionSelect.mdb.select', badges.bind(sabor, sabor.dataset.badge, aSabores[""+sabor.dataset.badge+""], aSabores[""+sabor.dataset.badge+"-selected"], true));
                sabor.addEventListener('optionDeselect.mdb.select', badges.bind(sabor, sabor.dataset.badge, aSabores[""+sabor.dataset.badge+""], aSabores[""+sabor.dataset.badge+"-selected"],false));
            });
            aromas.forEach((aroma)=>{
                aroma.addEventListener('optionSelect.mdb.select', badges.bind(aroma, aroma.dataset.badge, aAromas[""+aroma.dataset.badge+""], aAromas[""+aroma.dataset.badge+"-selected"], true));
                aroma.addEventListener('optionDeselect.mdb.select', badges.bind(aroma, aroma.dataset.badge, aAromas[""+aroma.dataset.badge+""], aAromas[""+aroma.dataset.badge+"-selected"], false));
            });
        }
        let tazas = document.querySelectorAll('.tazas');
        tazas.forEach((taza)=>{
            taza.addEventListener('change', tazasEncendidas);
            if (taza.id.split('-')[0] == "cTLimpia")
            {
                taza.addEventListener('change', calculate);
            }
        });
        let inputs = document.querySelectorAll('.calculated');
        inputs.forEach((input)=>{
            input.addEventListener('change', calculate);
            input.addEventListener('keyup', calculate);
        });
        let ranges = document.querySelectorAll('input[name=icuerpo]');
        ranges.forEach((range)=>{
            range.addEventListener('change', calculate);
        });
    }
}

var calculate = ()=>{
    let e=event.target;
    let idMuestra=e.dataset.muestra;
    let sabor=parseFloat(document.getElementById('Sabor-'+idMuestra).value);
    let aroma=parseFloat(document.getElementById('Fragancia-'+idMuestra).value);
    let acidez=parseFloat(document.getElementById('Acidez-'+idMuestra).value);
    let cuerpo=parseFloat(document.getElementById('Cuerpo-'+idMuestra).value);
    let remanente=parseFloat(document.getElementById('Remanente-'+idMuestra).value);
    let uniformidad=parseFloat(document.getElementById('pUniformidad-'+idMuestra).value);
    let tLimpia=parseFloat(document.getElementById('pTLimpia-'+idMuestra).value);
    let dulzor=parseFloat(document.getElementById('pDulzor-'+idMuestra).value);
    let balance=parseFloat(document.getElementById('Balance-'+idMuestra).value);
    let pSensorial=parseFloat(document.getElementById('pCatador-'+idMuestra).value);
    let tDefectuosas=5-document.getElementById('cTLimpia-'+idMuestra).value;
    let intensidad=document.getElementById('iCuerpo-'+idMuestra).value;
    let total=0.0;
    if ( intensidad == 3)
    {
        total=parseFloat((sabor+aroma+acidez+cuerpo+remanente+uniformidad+tLimpia+dulzor+balance+pSensorial)-(4*tDefectuosas));
        document.getElementById("castigo-"+idMuestra).value=(4*tDefectuosas).toFixed(2);
    }
    else if (intensidad == 1 || intensidad == 2)
    {
        total=parseFloat((sabor+aroma+acidez+cuerpo+remanente+uniformidad+tLimpia+dulzor+balance+pSensorial)-(2*tDefectuosas));
        document.getElementById("castigo-"+idMuestra).value=(2*tDefectuosas).toFixed(2);
    }
    total<0?total=0:total=total;
    document.getElementById("puntajeFinal-"+idMuestra).innerHTML=total.toFixed(2);
    document.getElementById('pFinal-'+idMuestra).value=total.toFixed(2);
}

const saveSensorial = (event, idMuestra)=>{
    event.preventDefault();
    const form = new FormData(document.querySelector(`form#addSensorial-${idMuestra}`));
    form.append('idMuestra', idMuestra);
    form.append('sabores', aSabores['badgeSabor-'+idMuestra+'-selected']);
    form.append('aromas', aAromas['badgeAroma-'+idMuestra+'-selected']);
    const request = new XMLHttpRequest();
    request.open('POST', '/lab/saveSensorial');
    request.onload = ()=>{
        const data=JSON.parse(request.responseText);
        if (data.status==200){
            alert(data.mensaje);
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

function calculate(e, idMuestra, peso){
        document.getElementById(`por-${idMuestra}`).innerHTML= ((parseFloat(e.target.value)/parseFloat(peso))*100).toFixed(2);
        
}
let validkeys = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'];
function validate10(e){
    if(e.target.value>10 || e.target.value<0){
        e.target.value=e.target.value/10;
        if (validkeys.indexOf(e.key) > 0)
        {
            e.preventDefault();
        } 
    }
}

var badges = (contenedor, array, selected, add) => {
    let e=event.target.selectedOptions, color;
    let container=document.querySelector(`.${contenedor}`), id=contenedor.split('-')[1];
    if (add){
        for (let i=0; i<e.length; i++){
            if (!array.includes(e[i].text)){
                array.push(e[i].text);
                let badge = document.createElement('span');
                contenedor.includes("Sabor")?color="badge-primary":color="badge-danger";
                badge.classList.add('badge', 'rounded-pill', color, 'm-1');
                badge.id=id+"_"+e[i].text;
                badge.innerHTML=e[i].text;
                //badge.addEventListener('click', deleteBadge);
                container.appendChild(badge);
            }
            if(!selected.includes(e[i].value)){
                selected.push(e[i].value);
            }
        }
    }
    else{
        let todos , eliminados=[], seleccionados2=[], selected2=[], deleted=[];
        if (contenedor.includes('Sabor'))
        {
            todos=document.querySelectorAll("select[name=sabores][form=addSensorial-"+id+"]");
        }
        else if (contenedor.includes('Aroma')){
            todos=document.querySelectorAll("select[name=aromas][form=addSensorial-"+id+"]");
        }
        
        todos.forEach((select)=>{
            select.querySelectorAll('option').forEach((option)=>
            {
                if (option.selected)
                {
                    if(!seleccionados2.includes(option.textContent) && !selected2.includes(option.value))
                    {
                        seleccionados2.push(option.textContent);
                        selected2.push(option.value);
                    }
                }
            });
        });
        //Eliminados es el nuevo arreglo de los que aun
        //deberian estar seleccionados sin los eliminados
        //Nombre ambiguo, pero es lo que hace.
        eliminados=getDifference(array, seleccionados2);
        eliminados.forEach((element)=>{
            if(array.includes(element)){
                array.splice(array.indexOf(element),1);
                document.getElementById(id+"_"+element).remove();
            }
        });
        //Eliminados es el nuevo arreglo de los que aun
        //deberian estar seleccionados sin los eliminados
        //Nombre ambiguo, pero es lo que hace.
        deleted=getDifference(selected, selected2);
        deleted.forEach((element)=>{
            if(selected.includes(element)){
                selected.splice(selected.indexOf(element),1);
            }
        });
    }
    
}

var deleteBadge = (event)=>{
    let element=event.target.parentElement;
    element.remove();

}

function getDifference(array1, array2) {
    return array1.filter(object1 => {
      return !array2.some(object2 => {
        return object1 === object2;
      });
    });
  }

  var tazasEncendidas =  ()=>{
    let e= event.target;
    let id=e.id.split('-');
    let dato= document.getElementById(`${id[0]}-${parseInt(id[1])+1}-${id[2]}`);
    if (e.value<5 && dato.checked && dato.value>e.value)
    {
        for (let i = dato.value ; i <=5; i++) 
        {
            document.getElementById(`${id[0]}-${i}-${id[2]}`).checked=false;
            if (document.getElementById(`${id[0]}-btn-${i}-${id[2]}`).classList.contains('change-color'))
            {
                document.getElementById(`${id[0]}-btn-${i}-${id[2]}`).classList.toggle('change-color');
            }
        }
        if(!e.checked){
            e.checked=true;
            document.getElementById(`${id[0]}-${id[2]}`).value=e.value;
            e.click();
            return
        } 
    }

    if (e.checked){
        document.getElementById(`${id[0]}-btn-${id[1]}-${id[2]}`).classList.toggle('change-color');
        if(e.value>1 && e.value<6){
            for (let i = e.value-1; i >= 1; i--){
                document.getElementById(`${id[0]}-${i}-${id[2]}`).checked=true;
                if(!document.getElementById(`${id[0]}-btn-${i}-${id[2]}`).classList.contains('change-color')){
                    document.getElementById(`${id[0]}-btn-${i}-${id[2]}`).classList.toggle('change-color');
                }
            }
            document.getElementById(`${id[0]}-${id[2]}`).value=e.value;
        }
        
    }
    else
    {
        document.getElementById(`${id[0]}-btn-${id[1]}-${id[2]}`).classList.toggle('change-color');
        if (e.value<=5 && e.value>0)
        {
            for (let x = e.value-1; x >= 1; x--){
                document.getElementById(`${id[0]}-${x}-${id[2]}`).checked=false;
                if(document.getElementById(`${id[0]}-btn-${x}-${id[2]}`).classList.contains('change-color')){
                    document.getElementById(`${id[0]}-btn-${x}-${id[2]}`).classList.toggle('change-color');
                }

            }
        }
        document.getElementById(`${id[0]}-${id[2]}`).value=0;
    }
  }