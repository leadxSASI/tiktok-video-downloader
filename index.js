const express = require('express');
const Tiktok = require('@tobyg74/tiktok-api-dl');
const axios = require('axios');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;
app.use(express.json());

// Create downloads folder
const downloadsDir = path.join(__dirname, 'downloads');
if (!fs.existsSync(downloadsDir)) {
    fs.mkdirSync(downloadsDir, { recursive: true });
}

// API Endpoint: POST /download-video
// Body: { "url": "https://vt.tiktok.com/xxxxxxxx" }
app.post('/download-video', async (req, res) => {
    const { url } = req.body;
    if (!url) return res.status(400).json({ error: 'TikTok URL required!' });

    try {
        // Use tiktok-api-dl to get video data (without watermark)
        const result = await Tiktok.Downloader(url, { version: 'v1' });
        if (!result.video || !result.video.noWatermark) {
            return res.status(404).json({ error: 'No video found or download failed!' });
        }

        const videoUrl = result.video.noWatermark;
        const title = result.title.replace(/[^a-z0-9]/gi, '_').toLowerCase();
        const filename = `${title}.mp4`;
        const filepath = path.join(downloadsDir, filename);

        // Download video
        const response = await axios({ url: videoUrl, method: 'GET', responseType: 'stream' });
        response.data.pipe(fs.createWriteStream(filepath));

        response.data.on('end', () => {
            console.log(`Downloaded video to ${filepath}`);
            res.json({ 
                success: true, 
                title: result.title,
                author: result.author,
                downloaded: filename,
                size: result.video.size || 'Unknown'
            });
        });
    } catch (error) {
        console.error('Error:', error.message);
        res.status(500).json({ error: 'Failed to download: ' + error.message });
    }
});

// Health check
app.get('/', (req, res) => res.send('TikTok Video Downloader API Ready!'));

app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));
