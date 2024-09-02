
  function selectOriginCity(cityName) {
    document.getElementById('originInput').value = cityName;
    document.getElementById('origin_result').innerHTML = '';
  }

  function selectDepartureCity(cityName) {
    document.getElementById('departureInput').value = cityName;
    document.getElementById('departure_result').innerHTML = '';
  }

  document.addEventListener('htmx:configRequest', function(event) {
    event.detail.headers['X-CSRFToken'] = '{{ csrf_token }}';
  });
