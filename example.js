var http = require('http');
var sys = require('sys');
var amqp = require('/usr/local/lib/node/node-amqp/amqp');
var io = require('/usr/local/lib/node/socket.io');
var connection = amqp.createConnection({host: 'ec2-50-18-18-186.us-west-1.compute.amazonaws.com', password: 'n0td3f4ult'})
var clients = [];
//var connection = amqp.createConnection({host: '127.0.0.1'});
var server = http.createServer(function(request, response){
    response.writeHead(200, {'Content-Type': 'text/plain'});
    response.end('Hello World\n');
});
server.listen(8124);
var socket = io.listen(server);
socket.on('connection', function(client){
    client.on('message', function(){
        console.log('got message');
    });
    client.on('disconnect', function(){
        console.log('disconnect');
        clients.pop(client);
    });
    clients.push(client);
});
connection.addListener('ready', function(){
    var q = connection.queue('testq2',
        {autoDelete: true, durable: false, exclusive: false});
    q.bind('#'); //gets all messages
    q.subscribe(function(message){
        sys.puts(sys.inspect(message));
        sys.puts(message.data);
        for (clienti in clients){
            var client = clients[clienti];
            console.log(message);
            console.log(message.data);
            client.send(message);
            console.log('sent that to a client');
        };
    });
});

console.log('Server running at http://127.0.0.1:8124/');

