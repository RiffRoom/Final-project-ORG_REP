'use strict';

let map;

let sessionMarkerPlaced = false;
let infoWindowOpen = false;

let sessionMarker;
let currentInfoWindow;

const addMarkerButton = document.getElementById("create_session_button");
let markerTitleInput = document.getElementById("session_title");
let markerMessageInput = document.getElementById("session_message");
let markerDateInput = document.getElementById("session_date_time");


async function initMap() {
    
    const { Map } = await google.maps.importLibrary("maps");
    const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");
    const { InfoWindow } = await google.maps.importLibrary("maps");

    const position = { lat: 35.30882205337362, lng: -80.73374243196827 };
    
    map = new Map(document.getElementById("map"), {
        zoom: 16,
        center: position,
        mapId: "DEMO_MAP_ID",
    });

    google.maps.event.addListener(map, "click", function (e) {
        let latitude = e.latLng.lat();
        let longitude = e.latLng.lng();

        if(!sessionMarkerPlaced){
            sessionMarker = new AdvancedMarkerElement({
                map: map,
                position: { lat: latitude, lng: longitude },
                title: "New Session"
            });
            sessionMarkerPlaced = true;

        }
        else {
            sessionMarker.position = {lat: latitude, lng: longitude};
        }
    });


    addMarkerButton.addEventListener('click', function (e) {
        if(sessionMarkerPlaced){
                sessionMarkers[Object.keys(sessionMarkers).length] = new MarkerObject(
                    {lat: sessionMarker.position.lat, lng: sessionMarker.position.lng},
                );

                sessionMarkerPlaced = false;

                let data = {
                    title: markerTitleInput.value,
                    message: markerMessageInput.value,
                    lat: sessionMarker.position.lat,
                    lng: sessionMarker.position.lng,
                    date: markerDateInput.value
                }

                let json_data = JSON.stringify(data);

                fetch(`${window.origin}/sessions/new_session`, {
                    method: 'POST',
                    redirect: 'follow',
                    headers: {
                        'Accept': 'application/json, multipart/form-data',
                        'Content-Type': 'application/json; charset=UTF-8'
                    },
                    body: json_data
                })
                initMap();
            }
        });

}


initMap();


