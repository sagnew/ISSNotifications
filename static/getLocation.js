function successFunction(position) {
  var lat = position.coords.latitude;
  var lon = position.coords.longitude;

  document.getElementById('latitude').value = lat;
  document.getElementById('longitude').value = lon;

  console.log('Your latitude is :' + lat + ' and longitude is ' + lon);
}

if (navigator.geolocation) {
  navigator.geolocation.getCurrentPosition(successFunction);
} else {
  alert('It seems like Geolocation, which is required for this page, is not enabled in your browser. Please use a browser which supports it.');
}
