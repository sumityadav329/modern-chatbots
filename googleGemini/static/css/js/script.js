document.getElementById('analyzeButton').addEventListener('click', function() {
    var fileInput = document.getElementById('imageUpload');
    if (fileInput.files.length === 0) {
        alert("Please upload an image first.");
        return;
    }

    var file = fileInput.files[0];
    var reader = new FileReader();

    reader.onloadend = function() {
        var imageData = reader.result;
        // Sending image data to the server
        fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ image: imageData })
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('resultContent').innerHTML = data.result;
        })
        .catch(error => console.error('Error:', error));
    };

    reader.readAsDataURL(file);
});
