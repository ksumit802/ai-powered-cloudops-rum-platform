
// Load dashboard summary
async function loadDashboardSummary() {
    try {
        const response = await fetch("/api/dashboard/summary");
        if (!response.ok) throw new Error("Dashboard API failed");

        const data = await response.json();

        document.getElementById("availability-value").innerText =
            data.service_availability + "%";

        document.getElementById("incidents-value").innerText =
            data.active_incidents;

        document.getElementById("tickets-value").innerText =
            data.total_tickets;

        document.getElementById("sessions-value").innerText =
            data.user_sessions;

    } catch (error) {
        console.error("Dashboard error:", error);
    }
}


// Sidebar navigation
function setupNavigation() {
    const navItems = document.querySelectorAll(".nav-item");
    const sections = document.querySelectorAll(".page-section");
    const breadcrumb = document.getElementById("breadcrumb");

    navItems.forEach(item => {
        item.addEventListener("click", () => {

            const target = item.dataset.target;

            sections.forEach(section => {
                section.classList.add("hidden");
            });

            document.getElementById(target).classList.remove("hidden");

            navItems.forEach(nav => nav.classList.remove("active"));
            item.classList.add("active");

            breadcrumb.innerText =
                "Workspace / " + item.innerText.trim();

            // Load relevant data when opening a section
            if (target === "services") loadServices();
            if (target === "incidents") loadIncidents();
        });
    });
}


// Load services from Flask
async function loadServices() {
    try {
        const response = await fetch("/api/services");
        if (!response.ok) throw new Error("Services API failed");

        const services = await response.json();

        console.log("Services loaded:", services);

    } catch (error) {
        console.error("Service loading error:", error);
    }
}


// Load incidents from Flask
async function loadIncidents() {
    try {
        const response = await fetch("/api/incidents");
        if (!response.ok) throw new Error("Incidents API failed");

        const incidents = await response.json();

        console.log("Incidents loaded:", incidents);

    } catch (error) {
        console.error("Incident loading error:", error);
    }
}


// Initialize dashboard
document.addEventListener("DOMContentLoaded", () => {
    loadDashboardSummary();
    setupNavigation();
});
