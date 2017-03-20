'use strict';

var request = require('request');
var dbSession = require('../../src/backend/dbSession.js');
var Server = require('../../src/backend/server.js').Server;
var resetDatabase = require('../resetDatabase.js');
var async = require('async');

describe('The API', function () {

  var server;

  beforeEach(function (done) {
    server = Server('8081');
    server.listen(function (err) {
      resetDatabase(dbSession, function() {
        done(err);
      });
    });
  });

  afterEach(function (done) {
    server.close(function () {
      resetDatabase(dbSession, function() {
        done();
      });
    });
  });


  it('should respond to a GET request at /api/keywords/', function (done) {
    var expected = {
      "_items": [
        {'id': 1, 'value': 'Aubergine', 'categoryID': 1},
        {'id': 2, 'value': 'Onion', 'categoryID': 1},
        {'id': 3, 'value': 'Knife', 'categoryID': 2}
      ]
    };
    async.series(
      [
        function(callback) {
          dbSession.insert(
            'keyword',
            {'value': 'Aubergine', 'categoryID': 1},
            function(err) { callback(err) });
        },
        function(callback) {
          dbSession.insert(
            'keyword',
            {'value': 'Onion', 'categoryID': 1},
            function(err) { callback(err) });
        },
        function(callback) {
          dbSession.insert(
            'keyword',
            {'value': 'Knife', 'categoryID': 2},
            function(err) { callback(err) });
        }
      ],

        function(err, results) {
          if (err) throw(err);
          request.get(
            {
              'url': 'http://localhost:8081/api/keywords/',
              'json': true
            },
            function (err, res, body) {
              expect(res.statusCode).toBe(200);
              expect(body).toEqual(expected);
              done();
            }
          );
        }
      );
    });
  });
