const ctx = document.querySelector("#myChart");

async function hourly(){
  const api = "http://127.0.0.1:5000"

  const dailyData = await fetch(`${api}/hourlyStatements`)
  let data = await dailyData.json();

console.log(data);
console.log(data[0]);

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
