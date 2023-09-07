const addForm = document.querySelector('#addForm');
const name = document.querySelector('#name');
const long = document.querySelector('#long');
const lat = document.querySelector('#lat');
const api = "http://127.0.0.1:5000"

addForm.addEventListener('submit', () => {
fetch(`${api}/addSonde`, {
  method: 'POST',
  body: JSON.stringify({
    name: name.value,
    longitude: long.value,
    latitude: lat.value,
  }),
  headers: {
    'Content-Type': 'application/json'
  }
})
.then(response => response.json())
.then(data => {
  // Traitez la réponse de la requête POST ici
})
.catch(error => {
  // Gérez les erreurs de la requête POST ici
});
});
