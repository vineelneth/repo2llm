const { ipcRenderer } = require('electron');

let selectedFolder = null;

const selectBtn = document.getElementById('select-folder-btn');
const folderPathText = document.getElementById('folder-path');
const runBtn = document.getElementById('run-btn');
const formatSelect = document.getElementById('format-select');
const statusDiv = document.getElementById('status');

// Handle Folder Selection
selectBtn.addEventListener('click', async () => {
    const folder = await ipcRenderer.invoke('select-folder');
    if (folder) {
        selectedFolder = folder;
        folderPathText.innerText = selectedFolder;
        statusDiv.style.display = 'none';
    }
});

// Handle Run Button
runBtn.addEventListener('click', async () => {
    if (!selectedFolder) {
        alert("Please select a folder first!");
        return;
    }

    runBtn.innerText = "Running...";
    runBtn.disabled = true;
    statusDiv.style.display = 'block';
    statusDiv.innerText = "Crawling repository and estimating tokens...";

    const result = await ipcRenderer.invoke('run-repo2llm', {
        folderPath: selectedFolder,
        format: formatSelect.value
    });

    runBtn.innerText = "Generate Prompt";
    runBtn.disabled = false;

    if (result.success) {
        statusDiv.style.background = "#dcfce3";
        statusDiv.innerText = "✅ Success!\n\n" + result.log;
    } else {
        statusDiv.style.background = "#fee2e2";
        statusDiv.innerText = "❌ Error:\n\n" + result.log;
    }
});