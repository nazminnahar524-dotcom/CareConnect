/* =========================================
   Pharmacy Admin Location Picker
   Leaflet + Esri World Street Map
========================================= */

document.addEventListener("DOMContentLoaded", function () {

    /* =========================================
       Get Django Latitude / Longitude Fields
    ========================================= */

    const latitudeField =
        document.getElementById("id_latitude");

    const longitudeField =
        document.getElementById("id_longitude");


    // Fields না থাকলে কিছু করবে না
    if (!latitudeField || !longitudeField) {
        return;
    }


    /* =========================================
       Default Location: Dhaka
    ========================================= */

    const defaultLatitude = 23.8103;
    const defaultLongitude = 90.4125;


    let latitude =
        parseFloat(latitudeField.value);

    let longitude =
        parseFloat(longitudeField.value);


    const hasExistingLocation =
        !isNaN(latitude) &&
        !isNaN(longitude);


    // Existing location না থাকলে Dhaka
    if (!hasExistingLocation) {

        latitude = defaultLatitude;
        longitude = defaultLongitude;

    }


    /* =========================================
       Create Map Wrapper
    ========================================= */

    const mapWrapper =
        document.createElement("div");


    mapWrapper.className =
        "pharmacy-location-wrapper";


    mapWrapper.innerHTML = `

        <div class="pharmacy-location-title">
            Pharmacy Location
        </div>

        <div class="pharmacy-location-help">
            Click on the map to select the exact pharmacy
            location. You can also drag the marker.
        </div>

        <div
            id="pharmacy-location-map"
            class="pharmacy-map"
        ></div>

        <div class="pharmacy-location-message">
            Select the exact pharmacy location on the map.
        </div>

    `;


    /* =========================================
       Insert Map Before Latitude
    ========================================= */

    const latitudeRow =
        latitudeField.closest(".form-row");


    if (latitudeRow) {

        latitudeRow.parentNode.insertBefore(
            mapWrapper,
            latitudeRow
        );

    } else {

        latitudeField.parentNode.insertBefore(
            mapWrapper,
            latitudeField
        );

    }


    /* =========================================
       Create Leaflet Map
    ========================================= */

    const map =
        L.map(
            "pharmacy-location-map"
        ).setView(
            [latitude, longitude],
            hasExistingLocation ? 16 : 12
        );


    /* =========================================
       ESRI World Street Map
    ========================================= */

    L.tileLayer(
        "https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}",
        {
            maxZoom: 19,

            attribution:
                "Tiles &copy; Esri"
        }
    ).addTo(map);


    /* =========================================
       Marker
    ========================================= */

    let marker = null;


    /* =========================================
       Existing Marker
    ========================================= */

    if (hasExistingLocation) {

        marker =
            L.marker(
                [latitude, longitude],
                {
                    draggable: true
                }
            ).addTo(map);

    }


    /* =========================================
       Update Coordinates
    ========================================= */

    function updateCoordinates(lat, lng) {

        latitudeField.value =
            Number(lat).toFixed(6);

        longitudeField.value =
            Number(lng).toFixed(6);

    }


    /* =========================================
       Marker Drag
    ========================================= */

    function handleMarkerDrag() {

        if (!marker) {
            return;
        }


        const position =
            marker.getLatLng();


        updateCoordinates(
            position.lat,
            position.lng
        );

    }


    /* =========================================
       Existing Marker Drag Event
    ========================================= */

    if (marker) {

        marker.on(
            "dragend",
            handleMarkerDrag
        );

    }


    /* =========================================
       Map Click
    ========================================= */

    map.on(
        "click",
        function (event) {

            const lat =
                event.latlng.lat;

            const lng =
                event.latlng.lng;


            /* -----------------------------
               Create Marker
            ----------------------------- */

            if (!marker) {

                marker =
                    L.marker(
                        [lat, lng],
                        {
                            draggable: true
                        }
                    ).addTo(map);


                marker.on(
                    "dragend",
                    handleMarkerDrag
                );

            }


            /* -----------------------------
               Move Existing Marker
            ----------------------------- */

            else {

                marker.setLatLng(
                    [lat, lng]
                );

            }


            /* -----------------------------
               Update Django Fields
            ----------------------------- */

            updateCoordinates(
                lat,
                lng
            );

        }
    );


    /* =========================================
       Fix Leaflet Map Size
    ========================================= */

    setTimeout(
        function () {

            map.invalidateSize();

        },
        500
    );

});