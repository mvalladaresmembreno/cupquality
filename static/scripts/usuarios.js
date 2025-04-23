document.onreadystatechange = function () {
    if (document.readyState == "complete")
    {
        var options = {
            valueNames: ['email','org']
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

const deleteUser= (event, id)=>
{
    event.preventDefault();
    const form = new FormData(document.getElementById(`deleteUser-${id}`));
    form.append('id', id);
    const request = new XMLHttpRequest();
    request.open('POST', `/auth/delete`);
    request.onload = ()=>{
        const data=JSON.parse(request.responseText);
        if (data.success){
            alert(data.mensaje);
            window.location.replace("/auth/perfilAdmin");
        }else{
            alert(data.mensaje);
            return false;
        }
    }
    request.send(form);
}

const activateUser= (event, id)=>
{
    event.preventDefault();
    const form = new FormData(document.getElementById(`activateUser-${id}`));
    form.append('id', id);
    const request = new XMLHttpRequest();
    request.open('POST', `/auth/activate`);
    
    request.onload = ()=>{
        const data=JSON.parse(request.responseText);
        if (data.success){
            alert(data.mensaje);
            window.location.replace("/auth/perfilAdmin");
        }else{
            alert(data.mensaje);
            return false;
        }
    }
    request.send(form);
}

const editUser= (event, id)=>
{
    event.preventDefault();
    const form = new FormData(document.getElementById(`editUsuario-${id}`));
    form.append('id', id);
    const request = new XMLHttpRequest();
    request.open('POST', `/auth/edit`);
    
    request.onload = ()=>{
        const data=JSON.parse(request.responseText);
        if (data.success){
            alert(data.mensaje);
            window.location.replace("/auth/perfilAdmin");
        }else{
            alert(data.mensaje);
            return false;
        }
    }
    request.send(form);
}

const addUser= (event)=>
{
    event.preventDefault();
    const form = new FormData(document.getElementById(`addUserForm`));
    const request = new XMLHttpRequest();
    request.open('POST', `/auth/sign_up`);
    
    request.onload = ()=>{
        const data=JSON.parse(request.responseText);
        if (data.success){
            alert(data.mensaje);
            window.location.replace("/auth/perfilAdmin");
        }else{
            alert(data.mensaje);
            return false;
        }
    }
    request.send(form);
}