document.addEventListener("DOMContentLoaded", ()=>{
    let pwd = document.getElementById('password');
    let pwd_c= document.getElementById("passwordC");
    let creation = document.getElementById("creation");
    let name=document.getElementById("name");
    let lname=document.getElementById("lastname");
    creation.classList.add("disabled");
    pwd_c.addEventListener('input', () => {
        if (pwd.value == pwd_c.value)
        {
            creation.classList.remove("disabled")
            pwd.classList.remove("is-invalid")
            pwd_c.classList.remove("is-invalid")
            pwd.classList.add("is-valid")
            pwd_c.classList.add("is-valid")
        }
        else
        {
            creation.classList.add("disabled")
            pwd.classList.remove("is-valid")
            pwd_c.classList.remove("is-valid")
            pwd.classList.add("is-invalid")
            pwd_c.classList.add("is-invalid")
            
        }

    });

    name.addEventListener('input', createusername);
    lname.addEventListener('input', createusername);
    
    function createusername(){
        //console.log((name.value.split(" ")[0][0]+lname.value.split(" ")[0]).toLowerCase());
    }

    const togglePassword = document.querySelector("#togglePasswordP");
    const togglePasswordC = document.querySelector("#togglePasswordPC");
    const password = document.querySelector("#password");
    const passwordC = document.querySelector("#passwordC");

    togglePassword.addEventListener("click", function () {
    // toggle the type attribute
    const type = password.getAttribute("type") === "password" ? "text" : "password";
    password.setAttribute("type", type);
    // toggle the eye icon
    this.classList.toggle('fa-eye');
    this.classList.toggle('fa-eye-slash');
    });

    togglePasswordC.addEventListener("click", function () {
        // toggle the type attribute
        const type = passwordC.getAttribute("type") === "password" ? "text" : "password";
        passwordC.setAttribute("type", type);
        // toggle the eye icon
        this.classList.toggle('fa-eye');
        this.classList.toggle('fa-eye-slash');
        });
});