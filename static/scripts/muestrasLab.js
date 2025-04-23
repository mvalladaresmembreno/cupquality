document.onreadystatechange = function () {
    if (document.readyState == "complete") 
    {
        var options = {
            valueNames: [ 'codigo', 'peso', 'procesamiento', 'presentacion', 'fecha', 'repetir']
          };
          /*table = id of the div */
          var userList = new List('table-fisico', options);
    }
}

const rmMuestra = (event, id) => {
    event.preventDefault();
    fetch(`/lab/delete/${id}`, {
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'XMLHttpRequest'
      },
    })
    .then(res => res.json())
    .then(data => {
      if(data.status == 200){
        event.target.parentElement.parentElement.remove()
      }
    })
    .catch(err => console.log(err))
  }