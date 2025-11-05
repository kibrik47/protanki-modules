document.getElementById("check-btn").addEventListener("click", function() {
    const turretSelect = document.getElementById("turret-select");
    const selectedTurret = parseInt(turretSelect.value);

    if (isNaN(selectedTurret)) {
        alert("Please select a turret.");
        return;
    }

    fetch(`/get_missing_turrets/${selectedTurret}`)
        .then(response => response.json())
        .then(data => {
            const missingTurretsList = document.getElementById("missing-turrets");
            missingTurretsList.innerHTML = ''; // Clear previous results

            if (data.error) {
                alert(data.error);
            } else {
                data.forEach(turret => {
                    const li = document.createElement("li");
                    li.textContent = turret;
                    missingTurretsList.appendChild(li);
                });
            }
        })
        .catch(error => {
            console.error("Error fetching data:", error);
        });
});
