var express = require('express');
var spawn = require("child_process").spawn;
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.contentType("application/pdf");
  var process = spawn('python',["./home/marco/trazdia/collector/trazdia.py", 'Diario_Oficial_SP', '01/03/2017']);
  process.stdout.on('data', function (data){
    res.send(data);
  });
});

module.exports = router;
