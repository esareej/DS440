document.addEventListener('DOMContentLoaded', () => {
    const backButton = document.getElementById('back-button');
    backButton.addEventListener('click', function() {
        window.location.href = 'upload.html'; // Ensure this matches the filename of your main page
    });
    // Retrieve the score from the URL parameter
    const urlParams = new URLSearchParams(window.location.search);
    const score = parseFloat(urlParams.get('score')); // Make sure the score is a floating point number

    // Update the score on the page
    const scoreElement = document.getElementById('score');
    scoreElement.textContent = score.toFixed(2);

    // Determine the prediction and update the page accordingly
    const predictionElement = document.getElementById('prediction');
    const finalResultElement = document.getElementById('final-result-value');

    if (score < 0.4) {
        predictionElement.textContent = 'Fake';
        finalResultElement.textContent = 'Fake';
        finalResultElement.style.color = '#e53e3e'; // Red color for fake
    } else if (score >= 0.4 && score < 0.6) {
        predictionElement.textContent = 'Uncertain';
        finalResultElement.textContent = 'Uncertain';
        finalResultElement.style.color = '#d69e2e'; // Yellow color for unsure
    } else {
        predictionElement.textContent = 'Real';
        finalResultElement.textContent = 'Real';
        finalResultElement.style.color = '#48bb78'; // Green color for real
    }
});