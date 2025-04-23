document.onreadystatechange = function () {
    if (document.readyState == "complete") {
        

        var options = {};
        var values=[]
        var listMuestras;
        getData();
        const dpto = document.getElementById('dpto');
        const mun = document.getElementById('mun');
        //BOTON FILTRAR
        const filtrar= document.getElementById('btnFiltrar');
        const desc = document.getElementById('btndsc')
        //SELECT MULTIPLE
        const certs = document.getElementById('certs');
        
        //SELECT
        const procesos = document.getElementById('procesos');
        //EVENTOS
        dpto.addEventListener('change', getMuni);
        filtrar.addEventListener('click', getData);
        desc.addEventListener('click', () => {
            const sabor = document.getElementById('sabores');
            let params = new URLSearchParams({
                org: document.getElementById('org').value,
                dpto: dpto.value,
                mun: mun.value,
                cert: [...certs.selectedOptions].map(option => option.value).toString().replace(/,/g, '_'),
                procesos: procesos.value,
                genero: document.getElementById('genero').value,
                sabores: [...sabor.selectedOptions].map(option => option.value).toString().replace(/,/g, '_'),
            });
            window.open ('/getajax/downloadPerfil/?'+ params);
        });
    }
}

const getData= () => {
    const sabor = document.getElementById('sabores');
    let params = new URLSearchParams({
        org: document.getElementById('org')? document.getElementById('org').value : '',
        dpto: dpto.value,
        mun: mun.value,
        cert: [...certs.selectedOptions].map(option => option.value).toString().replace(/,/g, '_'),
        procesos: procesos.value,
        genero: document.getElementById('genero').value,
        sabores: [...sabor.selectedOptions].map(option => option.value).toString().replace(/,/g, '_'),
    });
    fetch('/cooperativa/getPerfilMuestras'+'?'+ params,{
        headers:{
            'Accept': 'application/json',
             'X-Requested-With': 'XMLHttpRequest',
        },
    })
    .then(response => response.json())
    .then(data => {
        options = {
            valueNames: [ 'muestra', 'rechazo','conciliado', 'aEfectuado','genero', 'DTI', 'DTII', 'aroma', 'sabor', 'pf' ],
            item:'<tr><td class="muestra"></td><td class="rechazo"></td><td class="conciliado"></td><td class="aEfectuado"></td><td class="genero"></td><td class="DTI"></td><td class="DTII"></td><td class="aroma"></td><td class="sabor"></td><td class="pf"></td></tr>',
          };
        values=[];
        document.getElementById('listaMuestra').innerHTML="";
        if (Object.keys(data).length > 0){
            Object.keys(data).forEach(d => {
                values.push(data[d]);
            });
            listMuestras = new List('muestras', options, values);
        }
        else {
            document.getElementById('listaMuestra').innerHTML="<tr><td colspan='10'>No hay datos correspondientes a los filtros asignados</td></tr>";
        };

        
    })
    .catch(error => console.log(error));
}


const getMuni  = () => {
    const url = '/getajax/get_municipio/' + event.target.value;
    let select = mun;
    fetch(url,{
        headers:{
            'Accept': 'application/json',
             'X-Requested-With': 'XMLHttpRequest',
        },
    })
    .then(response => response.json())
    .then(data => {
        select.innerHTML = '';
        let option = document.createElement('option');
        option.value = '';
        option.text = 'Seleccione un municipio';
        option.defaultSelected = true;
        select.appendChild(option);
        data.municipios.forEach(m => {
            let option = document.createElement('option');
            option.value = m[1];
            option.text = m[0];
            select.appendChild(option);
        });
    });
}