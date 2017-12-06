var express = require('express');
var request = require('request');
var router = express.Router();

/**
 * Proxy for GET randomize call
 */
router.get('/randomize', function(req, res){
    request(`${process.env.RANDOMIZER_API}/api/randomize?user=${req.query.user}&list=${req.query.list}`, function(error, result) {
        if(error){
            error.status = error.status ? error.status : 500;
            console.log(error);
            res.send(error);
        } else {
            console.log(result.body);
            console.log(`Result of the Randomizerandomize call: ${result.body}`);
            res.send(result.body);
        }
    })
});

router.get('/redisuser', function(req, res) {
    request(`${process.env.RANDOMIZER_API}/api/redisuser?user=${req.query.user}&list=${req.query.list}`, function(error, result) {
        if(error){
            console.log(error);
        } else {
            console.log(`Result of redisuser call: ${result}`);
            res.send(result.body);
        }
    });
});

module.exports = router;