document.addEventListener("DOMContentLoaded", function() {
    const readPageButton = document.getElementById("readPage");
    const generateCoverLetterButton = document.getElementById("generateCoverLetter");
    const pageContent = document.getElementById("pageContent");

    readPageButton.addEventListener("click", async function() {
        try {
            const tabs = await chrome.tabs.query({
                active: true,
                currentWindow: true
            });
            const activeTab = tabs[0];
            const currentUrl = activeTab.url;

            const response = await fetch('http://localhost:5000/get_data?url=' + encodeURIComponent(currentUrl));

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.text();

            pageContent.innerText = data; // Display the fetched data
        } catch (error) {
            pageContent.innerText = "Error fetching data: " + error.message;
        }
    });

    generateCoverLetterButton.addEventListener("click", async function() {
        // Send the job data to your Flask app to generate a cover letter
        const jobData = pageContent.innerText; // Use the job data from the page

        const response = await fetch('http://localhost:5000/generate_cover_letter', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                job_data: jobData,
            }),
        });

        if (!response.ok) {
            pageContent.innerText = "Error generating cover letter";
        } else {
            const data = await response.json();
            pageContent.innerText = data.cover_letter;
        }
    });
});