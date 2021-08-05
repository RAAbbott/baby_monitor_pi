// const AudioContext = require('web-audio-api').AudioContext;
// const AudioNode = require('web-audio-api').AudioBufferSourceNode;
// const context = new AudioContext;
// const Speaker = require('speaker');

// context.outStream = new Speaker({
//     channels: context.format.numberOfChannels,
//     bitDepth: context.format.bitDepth,
//     sampleRate: context.sampleRate
// });

// const aNode = new AudioNode(context);

// aNode._start();

const portAudio = require('naudiodon');
const fs = require('fs');
const lame = require('lame');


const ai = new portAudio.AudioIO({
    inOptions: {
        channelCount: 1,
        sampleFormat: portAudio.SampleFormat16Bit,
        sampleRate: 44100,
        closeOnError: true,
        bitRate: 256,
        lameQuality: 5
    },
    // outOptions: {
    //     channelCount: 2,
    //     sampleFormat: portAudio.SampleFormat16Bit,
    //     sampleRate: 44100,
    //     closeOnError: true // Close the stream if an audio error is detected, if set false then just log the error
    // }
})

// const encoder = new lame.Encoder({
//     // channels: 1,
//     // bitDepth: 16,
//     // sampleRate: 44100,

//     bitRate: 128,
//     outSampleRate: 22050,
//     mode: lame.STEREO
// })

const ws = fs.createWriteStream('rawAudio.mp3');
const rs = fs.createReadStream('rawAudio.mp3');

// rs.pipe(ai);
// ai.start();


// ai.on('error', err => console.error)
// process.stdin.pipe(encoder);

ai.pipe(ws);
ai.start();
// encoder.pipe(ws);

// ai.on('data', buf => console.log(buf.timestamp));

// process.on('SIGINT', () => {
//     console.log('Received SIGINT, Stopping recording');
//     ai.quit();
// })