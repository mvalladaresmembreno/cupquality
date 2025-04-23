document.onreadystatechange = function () {
    if (document.readyState == "complete") {
        //SELECTS
        const cPais = document.getElementById('cPais');
        const cExp = document.getElementById('cExp');
        //BOTON FILTRAR
        const filtrar= document.getElementById('btnFiltrar');
        //SELECT MULTIPLE
        const cLote = document.getElementById('cLote');
        //SELECT
        const procesos = document.getElementById('procesos');
        const cAgricola = document.getElementById('cAgricola');
        //EVENTOS
        filtrar.addEventListener('click', getData);

        //CANVAS
        var DTP = document.getElementById('DTP').getContext('2d');
        var DTI = document.getElementById('DTI').getContext('2d');
        var DTII = document.getElementById('DTII').getContext('2d');
        var MRCHZ = document.getElementById('MRCHZ').getContext('2d');
        var MTRCHZ = document.getElementById('MTRCHZ').getContext('2d');
        var chartDPT, chartDTI, chartDTII, chartMRCHZ, chartMTRCHZ;

        //INDICADORES
        const TMR = document.getElementById('TMR');
        const TMAF = document.getElementById('TMAF');
        const TMAS = document.getElementById('TMAS');
        const PDTI = document.getElementById('PDTI');
        const PDTII = document.getElementById('PDTII');
        const PTM = document.getElementById('PTM');
        const PPM = document.getElementById('PPM');
        const PMAX = document.getElementById('PMAX');



        //INICIALIZACION DE TABLERO
        createChart();
        getData();
        
    }
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

const getData = () => {
    const sabor = document.getElementById('sabores');
    params=new URLSearchParams({
        cPais: cPais.value,
        cExp: cExp.value,
        cLote: cLote.value,
        cAgricola: cAgricola.value,
        procesos: procesos.value,
        sabores: [...sabor.selectedOptions].map(option => option.value).toString().replace(/,/g, '_'),
    }).toString()
    fetch('/lab/filtros'+'?'+params,{
        headers:{
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
        },
    })
    .then(response => response.json())
    .then(data => {
        TMR.innerHTML = data.TMR;
        TMAF.innerHTML = data.TMAF;
        TMAS.innerHTML = data.TMAS;
        PDTI.innerHTML = data.PDTI;
        PDTII.innerHTML = data.PDTII;
        PTM.innerHTML = data.PTM;
        PPM.innerHTML = data.PPM;
        PMAX.innerHTML = data.PMAX;
        chartDPT.data.datasets[0].data = data.DPT;
        chartDPT.update();
        chartDTI.data.datasets[0].data = data.DTI;
        chartDTI.update();
        chartDTII.data.datasets[0].data = data.DTII;
        chartDTII.update();
        chartMRCHZ.data.datasets[0].data = data.MRCHZ.cant;
        chartMRCHZ.data.labels = data.MRCHZ.labels;
        chartMRCHZ.update();
        chartMTRCHZ.data.datasets[0].data = data.MTRCHZ;
        chartMTRCHZ.update();

    })
    .catch(error => console.log(error));
}

function createChart(){
    chartDPT = new Chart(DTP,{
        type:'bar',
        data:{
            datasets:[{
                data:[],
                backgroundColor:["#E91E6333", "#673AB733","#2196F333","#00BCD433","#4CAF5033","#CDDC3933","#FFC10733", "#FF572233"],
                borderColor:["#E91E63", "#673AB7","#2196F3","#00BCD4","#4CAF50","#CDDC39","#FFC107", "#FF5722"],
                borderWidth: 1,
            }],    
        },
        options: 
        {
            indexAxis: 'x',
            responsive:true,
            maintainAspectRatio: false,
            barPercentage:1,
            parsing: 
            {
                xAxisKey: 'label',
                yAxisKey: 'cant',
            },
            
            plugins: {      
                legend: {
                    display:false,
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Dsitribucion de Puntajes'
                }
            },
            
        }
    });
    chartDTI = new Chart(DTI,{
        type:'bar',
        data:{
            datasets:[{
                data:[],
                backgroundColor:["#E91E6333", "#673AB733","#2196F333","#00BCD433","#4CAF5033","#CDDC3933","#FFC10733", "#FF572233"],
                borderColor:["#E91E63", "#673AB7","#2196F3","#00BCD4","#4CAF50","#CDDC39","#FFC107", "#FF5722"],
                borderWidth: 1,
            }],    
        },
        options: 
        {
            indexAxis: 'y',
            responsive:true,
            maintainAspectRatio: false,
            barPercentage:1,
            parsing: 
            {
                xAxisKey: 'cant',
                yAxisKey: 'label',
            },
            
            plugins: {      
                legend: {
                    display:false,
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Defectos Tipo I'
                }
            },
            
        }
    });
    chartDTII = new Chart(DTII,{
        type:'bar',
        data:{
            datasets:[{
                data:[],
                backgroundColor:["#E91E6333", "#673AB733","#2196F333","#00BCD433","#4CAF5033","#CDDC3933","#FFC10733", "#FF572233"],
                borderColor:["#E91E63", "#673AB7","#2196F3","#00BCD4","#4CAF50","#CDDC39","#FFC107", "#FF5722"],
                borderWidth: 1,
            }],    
        },
        options: 
        {
            indexAxis: 'y',
            responsive:true,
            maintainAspectRatio: false,
            barPercentage:1,
            parsing: 
            {
                xAxisKey: 'cant',
                yAxisKey: 'label',
            },
            
            plugins: {      
                legend: {
                    display:false,
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Defectos Tipo 2'
                }
            },
            
        }
    });
    chartMRCHZ = new Chart(MRCHZ,{
        type: 'doughnut',
        plugins: [ChartDataLabels],
        data:{
            labels: [],
            datasets:[
                {
                label:"",
                data:[],
                backgroundColor:["#C6282833", "#8BC34A33"],
                hoverOffset: 4,
                datalabels: {
                    anchor: 'center',
                    backgroundColor: null,
                    borderWidth: 0
                }
            }
        ]
            
        },
        options:{
            responsive: true,
            plugins:{
                datalabels: {
                    backgroundColor: function(context) {
                        return context.dataset.backgroundColor;
                    },
                    borderColor: 'black',
                    borderRadius: 25,
                    borderWidth: 1,
                    color: 'black',
                    display: function(context) {
                        var dataset = context.dataset;
                        var count = dataset.data.length-(dataset.data.length);
                        var value = dataset.data[context.dataIndex];
                        return value > count * 1.5;
                    },
                    font: {
                        
                        weight: 'bold'
                    },
                    padding: 6,
                    formatter: Math.round
                },
                legend:{
                    display: true,
                    position: 'top'
                },
                title:{
                    display: true,
                    text: 'Rechazados'
                }
            }
        }
    });
    chartMTRCHZ = new Chart(MTRCHZ,{
        type:'bar',
        data:{
            datasets:[{
                data:[],
                backgroundColor:["#E91E6333", "#673AB733","#2196F333","#00BCD433","#4CAF5033","#CDDC3933","#FFC10733", "#FF572233"],
                borderColor:["#E91E63", "#673AB7","#2196F3","#00BCD4","#4CAF50","#CDDC39","#FFC107", "#FF5722"],
                borderWidth: 1,
            }],    
        },
        options: 
        {
            indexAxis: 'y',
            responsive:true,
            maintainAspectRatio: false,
            barPercentage:1,
            parsing: 
            {
                xAxisKey: 'cant',
                yAxisKey: 'label',
            },
            
            plugins: {      
                legend: {
                    display:false,
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Motivos de Rechazo'
                }
            },
            
        }
    });

}