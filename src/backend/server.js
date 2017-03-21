'use strict';

var Percolator = require('percolator').Percolator;
var dbSession = require('../../src/backend/dbSession.js');
var spawn = require("child_process").spawn;

var Server = function(port) {
  var server = Percolator({'port': port, 'autoLink': false});
  server.route('/getSaoPaulo',
  {
    GET: function (req, res) {
      var process = spawn('python',["../../collector/trazdia.py", 'getJournal', 'Diario_Oficial_SP']);

      process.stdout.on('data', function (data){
        res.collection(data).send();
      });
    }
  });
  return server;
};

module.exports = {'Server': Server};
