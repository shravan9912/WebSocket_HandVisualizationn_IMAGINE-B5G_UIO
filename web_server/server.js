const express = require('express');
const { spawn } = require('child_process');

const app = express();
const PORT = 3000;

// Serve static files from the public directory
app.use(express.static('public'));

// Route for the video stream
app.get('/stream', (req, res) => {
    const ffmpeg = spawn('ffmpeg', [
        '-f', 'v4l2', // Use v4l2 for webcam on Linux
        '-i', '/dev/video0', // Update this if necessary
        '-f', 'mpegts', // Use MPEG-TS for streaming
        'pipe:1'
    ]);

    res.setHeader('Content-Type', 'video/mpegts');

    ffmpeg.stdout.pipe(res);
    
    ffmpeg.stderr.on('data', (data) => {
        console.error(`FFmpeg error: ${data}`);
    });

    res.on('close', () => {
        ffmpeg.kill('SIGINT');
    });
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});

