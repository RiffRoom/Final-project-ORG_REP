'use strict';

let map;

let sessionMarkerPlaced = false;
let infoWindowOpen = false;

let sessionMarker;
let currentInfoWindow;

// Dictionary of Session Markers
const sessionMarkers = {};

const addMarkerButton = document.getElementById("add_session_button");
let markerTitleInput = document.getElementById("session_title");

function MarkerObject(position, title){
    this.position = position;
    this.title = title;
}

//Gets data from server and then parses and creates MarkerObject objects
fetch(`${window.origin}/sessions`, {
    method: 'get',
    headers: {
        'content-type': 'application/json;charset=UTF-8',
    }
})
    .then(res => res.json())
    .then(sessionData => {
        console.log(sessionData);
    });
//     .then(sessionData => {
//         for(let i = 0; i < sessionData.data.length; i++) {
//             let newMarker = new MarkerObject({lat: parseFloat(sessionData.data[i].lat), lng: parseFloat(sessionData.data[i].lng)}, sessionData.data[i].title);
//             sessionMarkers[Object.entries(sessionMarkers).length] = newMarker;
//         }

//         for (const [key, value] of Object.entries(sessionMarkers)) {
//             console.log(`Key: ${key}, Value: (Lat: ${value.position.lat}, Lng: ${value.position.lng}), Title: ${value.title}`);
//         }   
// });

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


    for (const [key, value] of Object.entries(sessionMarkers)) {
        console.log(`Key: ${key}, Value: (Lat: ${value.position.lat}, Lng: ${value.position.lng}), Title: ${value.title}`);
    }


    for (const [key, value] of Object.entries(sessionMarkers)) {
        let marker = new AdvancedMarkerElement({
            map: map,
            position: value.position,
            title: value.title,
        });
        
        let infoWindow = new InfoWindow({
            content: `
            <h3>${marker.title}</h3>
            <div>
                <p>
                    <strong>Host</strong>: Noah Eddleman
                    <br>
                    <strong>Extra Info</strong>: Looking for someone to jam with me. 
                    Bring whatever you want!\n
                </p>
            </div>`,
            maxWidth: 250,
        });
        
        marker.addEventListener('gmp-click', () => {
            console.log("Clicked on: " + marker.title);
            
            if(infoWindowOpen){
                currentInfoWindow.close();
                infoWindow.open({
                    anchor: marker,
                    map,
                });
                currentInfoWindow = infoWindow;
                infoWindowOpen = true;
            }
            else {
                infoWindow.open({
                    anchor: marker,
                    map,
                });
                currentInfoWindow = infoWindow;
                infoWindowOpen = true;
            }
        });
    }
}


initMap();


