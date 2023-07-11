const { createApp } = Vue
createApp({
data() {
return {
personas:[],
//url:'http://localhost:5000/productos',
// si el backend esta corriendo local usar localhost 5000(si no lo subieron a pythonanywhere)
url:'https://naiggo.pythonanywhere.com/personas', // si ya lo subieron a pythonanywhere
error:false,
cargando:true,
/*atributos para el guardar los valores del formulario */
id:0,
nombre:"",
apellido:"",
mail:"",
fecha_nacimiento:"",
}
},
methods: {
fetchData(url) {
fetch(url)
.then(response => response.json())
.then(data => {
this.personas = data;
this.cargando=false
})
.catch(err => {
console.error(err);
this.error=true
})
},
eliminar(persona) {
const url = this.url+'/' + persona;
var options = {
method: 'DELETE',
}
fetch(url, options)
.then(res => res.text()) // or res.json()
.then(res => {
location.reload();
})
},
grabar(){
let persona = {
nombre:this.nombre,
apellido: this.apellido,
mail: this.mail,
fecha_nacimiento:convertirFecha(this.fecha_nacimiento)
}

console.log(persona)


var options = {
body:JSON.stringify(persona),
method: 'POST',
headers: { 'Content-Type': 'application/json' },
redirect: 'follow'
}
fetch(this.url, options)
.then(function () {
alert("Registro grabado")
window.location.href = "./personas.html";
})
.catch(err => {
console.error(err);
alert("Error al Grabarr")
})
}
},
created() {
this.fetchData(this.url)
},
}).mount('#app')

function convertirFecha(fecha) {
    let fechaNueva = new Date(fecha);
    let dia = fechaNueva.getDate();
    let mes = fechaNueva.getMonth() + 1; // Los meses en JavaScript son base 0, por lo que se suma 1
    let anio = fechaNueva.getFullYear();
  
    let fechaString = anio + "-" + (mes < 10 ? "0" + mes : mes) + "-" + (dia < 10 ? "0" + dia : dia);
  
    return fechaString;
  }