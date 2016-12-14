'use strict'

const express = require('express')
const request = require('request')
var bodyParser = require('body-parser')
const path = require('path')
const app = express()
var PythonShell = require('python-shell');
var async = require('async')

app.set('port', (process.env.PORT || 5000))

app.use( bodyParser.json() );       // to support JSON-encoded bodies
app.use(bodyParser.urlencoded({     // to support URL-encoded bodies
  extended: true
}))

app.use(express.static(__dirname + '/public'));

app.get('/', function (req, res) {
  res.sendFile(path.join(__dirname + '/views/index.html'));
})

app.post('/send', function(req, res){
  var msg = JSON.stringify(req.body.user_input);
	//console.log('body: ' + msg);
  res.end(msg)
});

app.post('/respond', function(req, res){
  var msg = JSON.stringify(req.body.user_input);
  
  async.series(
         [
            function(callback)
            {
                PythonShell.run('brain.py', { scriptPath: 'public/scripts', args:[msg] }, function (err, results) {
                  if (err)
                  {
                    callback(null, "I don't know that yet. I am a learner myself.")
                  }
                  else{
                    callback(null, results[2])
                  }
                });
            }
         ],
        function(err, results){
          // results is ['a', 'b', 'c', 'd']
          // final callback code
          var out = results[0].toString()
          res.json({ "outres" : out })
        }
   );
});

// Spin up the server
app.listen(app.get('port'), function() {
    console.log('running on port', app.get('port'))
})