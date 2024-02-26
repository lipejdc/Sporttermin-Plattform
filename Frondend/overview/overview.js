function applyFilters() {
    var searchInput = document.getElementById("searchInput").value.toLowerCase();
    var eventContainers = document.querySelectorAll(".col-lg-3");

    eventContainers.forEach(function (container) {
        var title = container.querySelector("h2").textContent.toLowerCase();
        if (title.includes(searchInput)) {
            container.style.display = "block";
        } else {
            container.style.display = "none";
        }
    });
}
