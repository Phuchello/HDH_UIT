// @ts-check
const { defineConfig, devices } = require('@playwright/test');

const fs = require('fs');
const path = require('path');

let pythonCmd = 'python';
if (process.env.APPDATA) {
  const uvPy = path.join(process.env.APPDATA, 'uv', 'python', 'cpython-3.11-windows-x86_64-none', 'python.exe');
  if (fs.existsSync(uvPy)) {
    pythonCmd = `"${uvPy}"`;
  }
}

module.exports = defineConfig({
  testDir: './tests',
  fullyParallel: false,
  workers: 1,
  reporter: 'list',
  use: {
    baseURL: 'http://127.0.0.1:8080',
    trace: 'on-first-retry',
  },
  webServer: {
    command: `${pythonCmd} -m http.server 8080 --directory public/site`,
    url: 'http://127.0.0.1:8080',
    reuseExistingServer: !process.env.CI,
    timeout: 15000,
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
});
