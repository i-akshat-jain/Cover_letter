document.addEventListener("DOMContentLoaded", function() {
    const readPageButton = document.getElementById("readPage");
    const pageContent = document.getElementById("pageContent");

    readPageButton.addEventListener("click", function() {
        // Use the chrome.tabs API to get the current active tab's URL
        chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
            const activeTab = tabs[0];
            const currentUrl = activeTab.url;

            // Use the Fetch API to send the URL to your Flask service
            fetch('http://localhost:5000/get_data?url=' + encodeURIComponent(currentUrl))
                .then(response => response.text())
                .then(data => {
                    pageContent.innerText = data; // Display the fetched data
                })
                .catch(error => {
                    pageContent.innerText = "Error fetching data";
                });
        });
    });
});