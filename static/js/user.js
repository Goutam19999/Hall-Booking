
function toggleFloatingOptions() {
    const floatingMenu = document.getElementById("floating-menu");
    floatingMenu.style.display = floatingMenu.style.display === "block" ? "none" : "block";
}

// Hide menu when clicking outside
document.addEventListener("click", function (event) {
    const userDiv = document.getElementById("user");
    const floatingMenu = document.getElementById("floating-menu");

    if (!userDiv.contains(event.target)) {
        floatingMenu.style.display = "none";
    }
});