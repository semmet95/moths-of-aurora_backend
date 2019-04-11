// imports firebase-functions module
const functions = require('firebase-functions');
// imports firebase-admin module
const admin = require('firebase-admin');

// // Create and Deploy Your First Cloud Functions
// // https://firebase.google.com/docs/functions/write-firebase-functions
//
// exports.helloWorld = functions.https.onRequest((request, response) => {
//  response.send("Hello from Firebase!");
// });

admin.initializeApp(functions.config().firebase);

/* Listens for new messages added to facebook and sends a notification to subscribed users */
exports.pushFa = functions.database.ref('/facebook').onWrite( ( change,context) => {
console.log('Push notification event triggered');
/* Grab the current value of what was written to the Realtime Database */
    var valueObject = change.after.val();
/* Create a notification and data payload. They contain the notification information, and message to be sent respectively */ 
    const payload = {
        /*notification: {
            title: 'Moths of Aurora',
            body: "New facebok",
            sound: "default"
        },*/
        data: {
            title: "Facebook",
            message: "new facebook post"
        }
    };
/* Create an options object that contains the time to live for the notification and the priority. */
    const options = {
        priority: "high",
        timeToLive: 60 * 60 * 24 //24 hours
    };
return admin.messaging().sendToTopic("alldevices", payload, options);
});

/* Listens for new messages added to instagram and sends a notification to subscribed users */
exports.pushIn = functions.database.ref('/instagram/data').onWrite( ( change,context) => {
console.log('Push notification event triggered');
/* Grab the current value of what was written to the Realtime Database */
    var valueObject = change.after.val();
/* Create a notification and data payload. They contain the notification information, and message to be sent respectively */ 
    const payload = {
        /*notification: {
            title: 'Moths of Aurora',
            body: "New instagram",
            sound: "default"
        },*/
        data: {
            title: "Instagram",
            message: "new instagram post"
        }
    };
/* Create an options object that contains the time to live for the notification and the priority. */
    const options = {
        priority: "high",
        timeToLive: 60 * 60 * 24 //24 hours
    };
return admin.messaging().sendToTopic("alldevices", payload, options);
});

/* Listens for new messages added to tickets and sends a notification to subscribed users */
exports.pushTi = functions.database.ref('/tickets').onWrite( ( change,context) => {
console.log('Push notification event triggered');
/* Grab the current value of what was written to the Realtime Database */
    var valueObject = change.after.val();
/* Create a notification and data payload. They contain the notification information, and message to be sent respectively */ 
    const payload = {
        /*notification: {
            title: 'Moths of Aurora',
            body: "New ticket",
            sound: "default"
        },*/
        data: {
            title: "Tickets",
            message: "new live show ticket"
        }
    };
/* Create an options object that contains the time to live for the notification and the priority. */
    const options = {
        priority: "high",
        timeToLive: 60 * 60 * 24 //24 hours
    };
return admin.messaging().sendToTopic("alldevices", payload, options);
});

/* Listens for new messages added to twitter and sends a notification to subscribed users */
exports.pushTw = functions.database.ref('/twitter').onWrite( ( change,context) => {
console.log('Push notification event triggered');
/* Grab the current value of what was written to the Realtime Database */
    var valueObject = change.after.val();
/* Create a notification and data payload. They contain the notification information, and message to be sent respectively */ 
    const payload = {
        /*notification: {
            title: 'Moths of Aurora',
            body: "New twitter",
            sound: "default"
        },*/
        data: {
            title: "Twitter",
            message: "new tweet"
        }
    };
/* Create an options object that contains the time to live for the notification and the priority. */
    const options = {
        priority: "high",
        timeToLive: 60 * 60 * 24 //24 hours
    };
return admin.messaging().sendToTopic("alldevices", payload, options);
});

/* Listens for new messages added to youtube and sends a notification to subscribed users */
exports.pushYo = functions.database.ref('/youtube').onWrite( ( change,context) => {
console.log('Push notification event triggered');
/* Grab the current value of what was written to the Realtime Database */
    var valueObject = change.after.val();
/* Create a notification and data payload. They contain the notification information, and message to be sent respectively */ 
    const payload = {
        /*notification: {
            title: 'Moths of Aurora',
            body: "New youtube",
            sound: "default"
        },*/
        data: {
            title: "Youtube",
            message: "new video uploaded"
        }
    };
/* Create an options object that contains the time to live for the notification and the priority. */
    const options = {
        priority: "high",
        timeToLive: 60 * 60 * 24 //24 hours
    };
return admin.messaging().sendToTopic("alldevices", payload, options);
});
