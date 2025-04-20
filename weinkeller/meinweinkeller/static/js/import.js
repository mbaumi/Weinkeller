let jsonData = null;

document.getElementById('json_file').addEventListener('change', function() {
    document.getElementById('previewButton').disabled = !this.files.length;
});

document.getElementById('previewButton').addEventListener('click', function() {
    const fileInput = document.getElementById('json_file');
    const file = fileInput.files[0];

    if (!file) {
        alert('Please select a file');
        return;
    }

    const reader = new FileReader();
    reader.onload = function(e) {
        try {
            jsonData = JSON.parse(e.target.result);
            displayPreview(jsonData);
        } catch (error) {
            alert('Error parsing JSON file: ' + error.message);
        }
    };

    reader.onerror = function() {
        alert('Error reading file');
    };

    reader.readAsText(file);
});

function displayPreview(data) {
    const previewContent = document.getElementById('previewContent');
    previewContent.innerHTML = '';

    console.log(data);
    data.forEach((wine, index) => {
        const wineDiv = document.createElement('div');
        wineDiv.className = 'wine-preview';
        wineDiv.innerHTML = `
            <h3>${wine.winename || 'Unnamed Wine'} (${wine.year || 'No Year'})</h3>
            <p>Type: ${wine.type}</p>
            <p>Winery: ${wine.wineryName || 'Not specified'}</p>
            <p>Price: ${wine.price || 'Not specified'} ${wine.currency || ''}</p>
        `;
        previewContent.appendChild(wineDiv);
    });

    document.getElementById('previewSection').style.display = 'block';
}

document.getElementById('importButton').addEventListener('click', async function() {
    if (!jsonData) {
        alert('No data to import');
        return;
    }

    let formData = new FormData();
    const token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    formData.append('json_data', JSON.stringify(jsonData));
    formData.append('csrfmiddlewaretoken', token);

    try {
        const response = await fetch('/api/import/', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        
        if (result.success) {
            alert(result.message || 'Import successful!');
            window.location.href = '/'; // Redirect to main page after success
        } else {
            alert('Error: ' + (result.error || 'Unknown error occurred'));
        }
    } catch (error) {
        console.error('Import error:', error);
        alert('Error during import: ' + error.message);
    }
});

document.getElementById('cancelButton').addEventListener('click', function() {
    document.getElementById('previewSection').style.display = 'none';
    document.getElementById('json_file').value = '';
    document.getElementById('previewButton').disabled = true;
    jsonData = null;
});