
const sessionId =
    sessionStorage.getItem("rum_session_id") ||
    crypto.randomUUID();

sessionStorage.setItem("rum_session_id", sessionId);

const userId = "demo_user_001";

async function trackEvent(
    eventName,
    pageName,
    taskId = null,
    description = "",
    metadata = {}
) {
    const event = {
        session_id: sessionId,
        user_id: userId,
        event_name: eventName,
        page_name: pageName,
        task_id: taskId,
        action_description: description,
        timestamp: new Date().toISOString(),
        metadata: metadata
    };

    try {
        const response = await fetch("/api/events", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(event)
        });

        if (!response.ok) {
            console.error("Event collection failed");
        }
    } catch (error) {
        console.error("RUM tracking error:", error);
    }
}


// Track page visit
trackEvent(
    "page_view",
    "home",
    null,
    "User opened Cloud Operations Portal"
);


// Track feature usage
document.querySelectorAll("[data-feature]").forEach(button => {

    button.addEventListener("click", () => {

        const feature = button.dataset.feature;

        trackEvent(
            "feature_used",
            feature,
            null,
            `User accessed ${feature}`
        );

    });

});


// Start support ticket task
document.getElementById("startTicket")
    .addEventListener("click", () => {

        trackEvent(
            "task_started",
            "support_tickets",
            "ticket_creation",
            "User started creating a support ticket"
        );

    });


// Complete support ticket task

document.getElementById("ticketForm").addEventListener("submit", async event => {
    event.preventDefault();

    const issue = document.getElementById("issue").value;

    // Send the actual ticket to Flask
    try {
        const response = await fetch("/api/tickets", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                user_id: userId,
                description: issue
            })
        });

        const result = await response.json();

        if (response.ok) {

            // Record successful task completion
            await trackEvent(
                "task_completed",
                "support_tickets",
                "ticket_creation",
                "Support ticket successfully created",
                { ticket_id: result.ticket_id }
            );

            document.getElementById("message").innerText =
                "Ticket created successfully! ID: " + result.ticket_id;

            event.target.reset();

        } else {

            // Record failed task
            await trackEvent(
                "task_failed",
                "support_tickets",
                "ticket_creation",
                "Ticket creation failed",
                { error: result.error }
            );

            document.getElementById("message").innerText =
                "Ticket creation failed: " + result.error;
        }

    } catch (error) {

        // Record communication or unexpected failure
        await trackEvent(
            "task_failed",
            "support_tickets",
            "ticket_creation",
            "Unable to communicate with ticket service",
            { error: error.message }
        );

        document.getElementById("message").innerText =
            "Unable to contact the server.";
    }
});

