let { PythonShell } = require('python-shell');

PythonShell.run('./pyth.py', null, function(err, results){
    console.log(results);
    console.log("python finished")
})