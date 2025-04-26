window.onload = function() {
    let mapa;
    const mapaContainer = document.getElementById("map");

    function initMap() {
        mapa = new google.maps.Map(mapaContainer, {
            center: {  lat: -1.455, lng: -48.490 },
            zoom: 12,
        });
    }

    initMap(); // Inicia o mapa quando a página for carregada
};
