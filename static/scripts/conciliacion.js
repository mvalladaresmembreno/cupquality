document.onreadystatechange = function(){
    if(document.readyState == 'complete'){
        const idMuestra=document.getElementById('idMuestra').value;
        const request = new XMLHttpRequest();
        request.open('GET', '/getajax/get_sensorial/'+idMuestra);
        request.onload = () => 
        {
            const data=JSON.parse(request.responseText);
            if (data.success)
            {
                if(data.sensorial.length>0)
                {promediar(data, idMuestra);}
                
            }
        }
        request.send();
    }
}

const saveConciliacion = (event, idMuestra)=>{
    event.preventDefault();
    const form = new FormData(document.querySelector(`form#conciliacion-${idMuestra}`));
    form.append('idMuestra', idMuestra);
    const request = new XMLHttpRequest();
    request.open('POST', `/muestras/conciliar/${idMuestra}`, true);
    request.onload = ()=>{
        const data=JSON.parse(request.responseText);
        if (data.status==200){
                alert(data.mensaje);
                document.getElementById(`saveCon-${idMuestra}`).disabled=true;
                window.location.href = '/muestras/verPuntaje/'+idMuestra;
                return false;
        }else{
            alert(data.mensaje);
            return false;
        }
    }
    request.send(form);
}

const calculate= (idMuestra)=>{
    let sabor=parseFloat(document.getElementById('sabor-'+idMuestra).value);
    let aroma=parseFloat(document.getElementById('aroma-'+idMuestra).value);
    let acidez=parseFloat(document.getElementById('acidez-'+idMuestra).value);
    let cuerpo=parseFloat(document.getElementById('cuerpo-'+idMuestra).value);
    let remanente=parseFloat(document.getElementById('remanente-'+idMuestra).value);
    let uniformidad=parseFloat(document.getElementById('uniformidad-'+idMuestra).value);
    let tLimpia=parseFloat(document.getElementById('tLimpia-'+idMuestra).value);
    let dulzor=parseFloat(document.getElementById('dulzor-'+idMuestra).value);
    let balance=parseFloat(document.getElementById('balance-'+idMuestra).value);
    let pSensorial=parseFloat(document.getElementById('pSensorial-'+idMuestra).value);
    let tDefectuosas=parseFloat(document.getElementById('tDefectuosas-'+idMuestra).value);
    let intensidad=parseFloat(document.getElementById('intensidad-'+idMuestra).value);
    let total=0;
    if (intensidad == 1 || intensidad == 2)
    {total=parseFloat((sabor+aroma+acidez+cuerpo+remanente+uniformidad+tLimpia+dulzor+balance+pSensorial)-(4*tDefectuosas));}
    else
    {total=parseFloat((sabor+aroma+acidez+cuerpo+remanente+uniformidad+tLimpia+dulzor+balance+pSensorial)-(2*tDefectuosas));}
    document.getElementById('pFinal-'+idMuestra).value=total;
}

function promediar(data,idMuestra){
    let pSabor=0.0, pAroma=0.0, pAcidez=0.0, pCuerpo=0.0, pRemanente=0.0, pUniformidad=0.0, pTLimpia=0.0, pDulzor=0.0, pBalance=0.0, pPSensorial=0.0, pTDefectuosas=0.0;
    data.sensorial.forEach(s=>{
        pSabor+=parseFloat(s[3]);
        pAroma+=parseFloat(s[2]);
        pAcidez+=parseFloat(s[5]);
        pCuerpo+=parseFloat(s[6]);
        pRemanente+=parseFloat(s[4]);
        pUniformidad+=parseFloat(s[8]);
        pTLimpia+=parseInt(s[9]);
        pDulzor+=parseFloat(s[10]);
        pBalance+=parseFloat(s[7]);
        pPSensorial+=parseFloat(s[11]);
        pTDefectuosas=5-parseInt(s[9]);
    });
    pSabor=pSabor/data.sensorial.length;
    pAroma=pAroma/data.sensorial.length;
    pAcidez=pAcidez/data.sensorial.length;
    pCuerpo=pCuerpo/data.sensorial.length;
    pRemanente=pRemanente/data.sensorial.length;
    pUniformidad=pUniformidad/data.sensorial.length;
    pTLimpia=pTLimpia/data.sensorial.length;
    pDulzor=pDulzor/data.sensorial.length; 
    pBalance=pBalance/data.sensorial.length;
    pPSensorial=pPSensorial/data.sensorial.length;
    pTDefectuosas=pTDefectuosas/data.sensorial.length;
    document.getElementById('sabor-'+idMuestra).value=pSabor;
    document.getElementById('aroma-'+idMuestra).value=pAroma;
    document.getElementById('acidez-'+idMuestra).value=pAcidez;
    document.getElementById('cuerpo-'+idMuestra).value=pCuerpo;
    document.getElementById('remanente-'+idMuestra).value=pRemanente;
    document.getElementById('uniformidad-'+idMuestra).value=pUniformidad;
    document.getElementById('tLimpia-'+idMuestra).value=pTLimpia;
    document.getElementById('dulzor-'+idMuestra).value=pDulzor;
    document.getElementById('balance-'+idMuestra).value=pBalance;
    document.getElementById('pSensorial-'+idMuestra).value=pPSensorial;
    document.getElementById('tDefectuosas-'+idMuestra).value=pTDefectuosas;
    calculate(idMuestra);
}

