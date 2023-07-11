console.log(location.search) // lee los argumentos pasados a este formulario
var id=location.search.substr(4)
console.log(id)
const { createApp } = Vue
createApp({
data() {
return {
id:0,
nombre:"",
apellido:"",
mail:"",
fecha_nacimiento:"",
dias_restantes:0,
url:'https://naiggo.pythonanywhere.com/personas/'+id,
}
},
methods: {
fetchData(url) {
fetch(url)
.then(response => response.json())
.then(data => {

console.log(data)
this.id=data.id
this.nombre = data.nombre;
this.apellido=data.apellido
this.mail=data.mail
this.fecha_nacimiento=data.fecha_nacimiento
})
.catch(err => {
console.error(err);
this.error=true
})
},
modificar() {
let persona = {
nombre:this.nombre,
apellido: this.apellido,
mail: this.mail,
fecha_nacimiento:this.fecha_nacimiento
}
var options = {
body: JSON.stringify(persona),
method: 'PUT',
headers: { 'Content-Type': 'application/json' },
redirect: 'follow'
}
fetch(this.url, options)
.then(function () {
alert("Registro modificado")
window.location.href = "./FE-proyecto-Final-G24/personas.html";
})
.catch(err => {
console.error(err);
alert("Error al Modificar")
})
}
},
created() {
this.fetchData(this.url)
},
}).mount('#app')