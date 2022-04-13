// load the express package and create our app
var express = require('express');
var app = express();
const PORT = process.env.PORT || 8080;

//python entry point
let {PythonShell} = require('python-shell')

PythonShell.run('./pyth.py', null, function(err, results){
    console.log(results);
    console.log("python finished")
})


// set the port based on environment (more on environments later)
var port = PORT;

// send our index.html file to the user for the home page
app.get('/', function(req, res) {
    //res.sendFile(__dirname + '/index.html');
    res.send("HELLO WORLD")
});

// create routes for the admin section
//get an instance of the router
var adminRouter = express.Router();

 // route middleware that will happen on every request
 adminRouter.use(function(req, res, next) {
    // log each request to the console
    console.log(req.method, req.url);
    // continue doing what we were doing and go to the route
    next(); });



// start the server
app.listen(PORT);
console.log(`Express Server running at http://127.0.0.1:${ PORT }/`);



//mongoDB
/*
const { MongoClient } = require('mongodb');
const uri = "mongodb://127.0.0.1:27017";
MongoClient.connect(uri, function (err, db) {
    if(err) throw err;
    console.log('Start the database stuff');
    var dbo = db.db('mydb');
    var userInput = {firstInput: 'user1', secondInput: 'user1again'};
    dbo.collection('u sers').insertOne(userInput), function(err, res){

    }
    //Write databse Insert/Update/Query code here..
    });
*/



//mongoDB end


/* //node server
//hello
fs = require('fs');
const PORT = process.env.PORT || 3000;
var http = require('http');

http.createServer(function(request, response){
    response.writeHead(200, {
        'Content-Type': "text/html",
        'Access-Control_Allow-Origin': '*'
    });
    var readStream = fs.createReadStream(__dirname + '/index.html');
    //send message
    readStream.pipe(response);
}).listen(PORT);

console.log(`Our app is running on port http://127.0.0.1:${ PORT }/`);
console.log('hehe');
*/

/*
http.createServer(function(request, response){
    response.writeHead(200, {'Content-type': 'text/plain'});
    response.end('Hello World\n');
}).listen(PORT);

 console.log(`Our app is running on port http://127.0.0.1:${ PORT }/`);
*/
