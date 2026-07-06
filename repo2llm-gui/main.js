const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const { spawn } = require('child_process');
const path = require('path');

let mainWindow;

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 600,
        height: 500,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        }
    });

    mainWindow.loadFile('index.html');
}

app.whenReady().then(createWindow);

// Listen for the folder picker request
ipcMain.handle('select-folder', async () => {
    const result = await dialog.showOpenDialog(mainWindow, {
        properties: ['openDirectory']
    });
    return result.filePaths[0];
});

// Listen for the "Run" command
ipcMain.handle('run-repo2llm', async (event, args) => {
    const { folderPath, format } = args;

    return new Promise((resolve) => {

        const outputPath = path.join(folderPath, 'repo_prompt.txt');

        const child = spawn(
            'repo2llm',
            [
                folderPath,
                '--format',
                format,
                '--out',
                outputPath
            ],
            {
                env: {
                    ...process.env,
                    PYTHONIOENCODING: 'utf-8'
                }
            }
        );

        let output = "";
        let errorOutput = "";

        child.stdout.on('data', (data) => {
            output += data.toString();
        });

        child.stderr.on('data', (data) => {
            errorOutput += data.toString();
        });

        child.on('close', (code) => {

            if (code !== 0) {
                resolve({
                    success: false,
                    log: errorOutput || `Exited with code ${code}`
                });
                return;
            }

            resolve({
                success: true,
                log: output
            });
        });
    });
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit();
});