var express = require('express');
var spawn = require("child_process").spawn;
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
    res.status(200).send('ok');
  });

module.exports = router;
