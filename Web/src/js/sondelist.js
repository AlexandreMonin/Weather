const table = document.querySelector("#table-body");

async function getSonde(){
  const api = "http://127.0.0.1:5000"

  const list = await fetch(`${api}/listSonde`)
  let sondes = await list.json();

  sondes.map((sonde) => {
    let row = document.createElement('tr');
    table.appendChild(row);

    let nameCell = document.createElement('td');
    nameCell.innerHTML = sonde.name;
    row.appendChild(nameCell);

    let latCell = document.createElement('td');
    latCell.innerHTML = sonde.latitude;
    row.appendChild(latCell);

    let lonCell = document.createElement('td');
    lonCell.innerHTML = sonde.longitude;
    row.appendChild(lonCell);
  });

  }

getSonde()