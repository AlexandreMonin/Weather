const ctx = document.querySelector("#myChart");
const table = document.querySelector("#table-body");

async function hourly(){
  const api = "http://127.0.0.1:5000"

  const dailyData = await fetch(`${api}/hourlyStatements`)
  let data = await dailyData.json();

    data.map((statement) => {
    let row = document.createElement('tr');
    table.appendChild(row);

    let dateCell = document.createElement('td');
    dateCell.innerHTML = statement.date;
    row.appendChild(dateCell);

    let temperatureCell = document.createElement('td');
    temperatureCell.innerHTML = `${statement.temperature} °C`;
    if (statement.temperature >= 25){
        temperatureCell.className = "bg-danger"
    }
    if (statement.temperature <= 12){
        temperatureCell.className = "bg-primary"
    }
    row.appendChild(temperatureCell);

    let humidityCell = document.createElement('td');
    humidityCell.innerHTML = `${statement.humidity} %`;
    row.appendChild(humidityCell);
  });

  new Chart(ctx, {
    type: 'line',
    data: {
    labels: data.map(row => row.date),
      datasets: [
      {
      label: 'Temperature',
        data: data.map(row => row.temperature)
      },
      {
        label: 'Humidité',
        data: data.map(row => row.humidity)
      }
      ]
    },
  });

}

hourly()
