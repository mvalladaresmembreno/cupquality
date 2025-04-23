document.onreadystatechange = function () {
    if (document.readyState == "complete") {
        let radares=[];
        //do something
        Object.keys(info).forEach(element => 
            {
                radares.push(document.getElementById("polar-" + element));
            });
        radares = radares.map( radar =>
            {
                return radar.getContext("2d");
            });
        radares.forEach(element => {
            let idRadar=element.canvas.id.split("-")[1];
            let radar = new Chart(element,{
                type: 'radar',
                data: {
                    labels: Object.keys(info[idRadar]),
                    datasets:[{
                        label: "Puntuación Muestra: " + idRadar,
                        fill: true,
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        borderColor: 'rgb(255, 99, 132)',
                        data: Object.values(info[idRadar]),
                        pointBackgroundColor: 'rgb(255, 99, 132)',
                        pointBorderColor: '#fff',
                        pointHoverBackgroundColor: 'rgb(255, 99, 132)',
                        pointHoverBorderColor: 'rgb(255, 99, 132)',
                    }],
                },
                options: {
                    rensponsive: true,
                    
                    plugins: {
                      legend: {
                        display: false
                     },
                      title: {
                        display: true,
                        text: 'Puntuacion General'
                      },
                      datalabels: {
                        backgroundColor: function(context) {
                          return context.dataset.borderColor;
                        },
                        color: 'white',
                        anchor:'end',
                        align: 'end',
                        font: {
                          weight: 'bold',
                          size: 14,
                          lineHeight: 1,
                        },
                        formatter: (value) =>{
                            return value;
                        },
                        padding: 5
                      },
                      tooltip: {
                        enabled: true
                      }
                    },
                    scales: {
                        r: {
                            angleLines: {
                                display: true
                            },
                            suggestedMin: 0,
                            suggestedMax: 10,
                            
                        },
                    },
                
                    // Core options
                    elements: {
                      point: {
                        hoverRadius: 7,
                        radius: 5
                      }
                    },
                  }
            });
        });
    }
}
