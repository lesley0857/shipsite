mapboxgl.accessToken = '{{mapbox_access_token}}';
var map = new mapboxgl.Map({
container: 'map',
style: 'mapbox://styles/mapbox/streets-v11', // stylesheet location
center: [9.000 ,7.5463885 ], // starting position [lng, lat]
zoom: 9 // starting zoom
});