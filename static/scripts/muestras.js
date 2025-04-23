document.onreadystatechange = function () {
    if (document.readyState == "complete") 
    {
        var options = {
            valueNames: [ 'codigo', 'peso', 'procesamiento', 'presentacion', 'fecha', 'repetir']
          };
          /*table = id of the div */
          var userList = new List('table-list', options);
          function search ( e ) {
            userList.search(this.value, e.target.dataset.searchType)
          }
          var searchInputs = document.getElementById('searching');
          if(searchInputs){
            searchInputs.addEventListener('keyup', search);
          }
    }
}

const rmMuestra = (event, id) => {
  event.preventDefault();
  fetch(`/muestras/delete/${id}`, {
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