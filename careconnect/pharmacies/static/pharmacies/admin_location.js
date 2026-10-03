/* =========================================
   Pharmacy Admin Location Picker
========================================= */

document.addEventListener("DOMContentLoaded", function () {

    const latitudeField =
        document.getElementById("id_latitude");

    const longitudeField =
        document.getElementById("id_longitude");

    // Latitude/Longitude field না থাকলে stop
    if (!latitudeField || !longitudeField) {
        return;
    }

    // Default location: Dhaka
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

    /*
    =========================================
    Create Location Section
    =========================================
    */

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

    /*
    =========================================
    Insert Map Before Latitude
    =========================================
    */

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

    /*
    =========================================
    Create Leaflet Map
    =========================================
    */

    const map =
        L.map(
            "pharmacy-location-map"
        ).setView(
            [latitude, longitude],
            hasExistingLocation ? 16 : 12
        );

    /*
    =========================================
    OpenStreetMap
    =========================================
    */

    L.tileLayer(
        "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        {
            maxZoom: 19,

            attribution:
                "&copy; OpenStreetMap contributors"
        }
    ).addTo(map);

    let marker = null;

    /*
    =========================================
    Existing Marker
    =========================================
    */

    if (hasExistingLocation) {

        marker =
            L.marker(
                [latitude, longitude],
                {
                    draggable: true
                }
            ).addTo(map);

    }

    /*
    =========================================
    Update Coordinates
    =========================================
    */

    function updateCoordinates(lat, lng) {

        latitudeField.value =
            Number(lat).toFixed(6);

        longitudeField.value =
            Number(lng).toFixed(6);
    }

    /*
    =========================================
    Marker Drag
    =========================================
    */

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

    if (marker) {

        marker.on(
            "dragend",
            handleMarkerDrag
        );
    }

    /*
    =========================================
    Map Click
    =========================================
    */

    map.on(
        "click",
        function (event) {

            const lat =
                event.latlng.lat;

            const lng =
                event.latlng.lng;

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

            } else {

                marker.setLatLng(
                    [lat, lng]
                );
            }

            /*
            Update Django fields
            */

            updateCoordinates(
                lat,
                lng
            );
        }
    );

    /*
    =========================================
    Fix Leaflet Map Size
    =========================================
    */

    setTimeout(
        function () {

            map.invalidateSize();

        },
        300
    );

});