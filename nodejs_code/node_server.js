var config = require('./config');
var querystring = require('querystring');
var redis = require('redis');
var http = require('http');
var io = require('socket.io');
var path = require('path');
var celery = require('node-celery');
var express = require('express');


var redis_url = 'redis://' + config.redis.host + ':' + config.redis.port + '/0';  // uses env vars, or defaults to localhost
console.log("redis url " + redis_url);

// Celery instance - URL, ROUTES, Events, etc.
var client = celery.createClient({
    CELERY_BROKER_URL: redis_url,
    CELERY_RESULT_BACKEND: redis_url,
    CELERY_ROUTES: {
        'tasks.test_celery': {
            queue: 'testing'
        }
    }
});
client.on('error', function(err) {
    console.log(err);
});


// Express lib used for hosting websocket and http:
var app = express()
var server = http.createServer(app)
var io = io.listen(server);

var nodejs_port = config.server.port;  // set in local config.js
var nodejs_host = config.server.host;  // set in local config.js

// Running HTTP and socket.io w/ same server instance
// Note: setup this way in cts_nodejs for hosting standalone nodejs test page (not included here)
server.listen(nodejs_port);

io.sockets.on('connection', function (socket) 
{
    console.log("session id: " + socket.id);

    // REDIS CLIENT AND EVENT
    //++++++++++++++++++++++++++++
    var message_client = redis.createClient(redis_url);
    message_client.subscribe(socket.id); // create channel with client's socket id
    
    // Grab message from Redis that was created by django and send to client
    message_client.on('message', function(channel, message){
        console.log("nodejs redis client 'message' event: sending results to client...");
        socket.send(message); // send to browser
    });


    // WEBSOCKET EVENTS
    //+++++++++++++++++++++++++++
    socket.on('disconnect', function () {
        console.log("user " + socket.id + " disconnected..");
        message_client.unsubscribe(socket.id); // unsubscribe from redis channel
        // var message_obj = {'cancel': true};  // cancel user's jobs
    });

    socket.on('error', function () {
        console.log("A socket error occured in cts_nodejs..");
    });

    socket.on('test_socket', function (message) {
        console.log("node received message: ");
        console.log(message);
        socket.send("hello from nodejs! at " + config.server.host + ", port " + config.server.port);
    });

    // test django-cts celery worker
    socket.on('test_celery', function (message) {
        console.log("received message: " + message);
        var query = querystring.stringify({
            sessionid: socket.id, // cts will now publish to session channel
            message: "hello celery"
        });

        console.log("sending message to celery worker..");
        console.log("message: " + query);

        // Send request to test_celery consumer across 'testing' queue:
        client.call('tasks.test_celery', [socket.id, 'hello celery'], function(result) {
            console.log("result info: ");
            console.log(result);
        });

    });

});