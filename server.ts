// Express server on port 3000
var express = require('express');
var app = express();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var port = 3000;

// Return the current time
app.get('/', function(req, res) {
  res.send('Current time: ' + new Date());
});
