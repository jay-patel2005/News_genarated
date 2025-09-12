document.getElementById('feedbackForm').addEventListener('submit', function (e) {
    e.preventDefault();
    const name = document.getElementById('name').value.trim();
    const message = document.getElementById('message').value.trim();

    if (!name || !message) {
        alert("Please fill in both fields.");
        return;
    }

    console.log("Feedback submitted:", { name, message });
    alert("Thank you for your feedback!");

    this.reset(); // Clear form
});
