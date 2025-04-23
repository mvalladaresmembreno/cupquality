const check = document.getElementById("CheckRec");
const comments = document.getElementsByClassName("recomendaciones");
const defecto = document.getElementsByClassName("defectos");

const cambio = (event) => {
    for (const c of comments) {
        if (event.target.checked) {
            c.style.display = "none"; 
        } else {
            c.style.display = "block";
        }
    }
    for (const d of defecto) {
        if (event.target.checked) {
            let custom = document.createElement("ul");
            let li = document.createElement("li");
            let text= document.createElement('textarea');
            text.style.width = "100%";
            text.style.height = "150px";
            text.style.resize = "none";
            text.style.padding = "0px";
            text.style.border = "none";
            text.style.marginLeft = "-35px";
            text.style.borderRadius = "5px";
            text.style.backgroundColor = "#f2f2f2";
            custom.style.listStyle = "none";
            custom.className = "custom";
            li.appendChild(text);
            custom.appendChild(li);
            d.appendChild(custom);
        } else {
            d.removeChild(d.lastChild)
        }
    }
}

check.addEventListener("change", cambio);