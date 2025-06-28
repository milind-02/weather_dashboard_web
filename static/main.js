function getLocation() {
    navigator.geolocation.getCurrentPosition(pos => {
        const form = document.createElement('form');
        form.method = 'POST';
        form.style.display = 'none';

        const lat = document.createElement('input');
        lat.name = 'lat';
        lat.value = pos.coords.latitude;

        const lon = document.createElement('input');
        lon.name = 'lon';
        lon.value = pos.coords.longitude;

        form.appendChild(lat);
        form.appendChild(lon);
        document.body.appendChild(form);
        form.submit();
    });
}

function fillCity(city) {
    const input = document.querySelector('input[name="city"]');
    input.value = city;
    input.form.submit();
}

document.getElementById("toggleTheme").addEventListener("click", () => {
    document.body.classList.toggle("dark-mode");
});
