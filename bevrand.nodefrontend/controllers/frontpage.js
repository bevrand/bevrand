var request = require('request');
const defaultList = process.env.DEFAULT_FRONTPAGE_LIST;

/**
 * Middleware to retrieve the standard FrontpageLists
 * @param {*} req 
 * @param {*} res 
 * @param {*} next 
 */
var retrieveFrontpageLists = function(req, res, next) {
   var test= process.env.MONGO_API;
   request(process.env.MONGO_API + '/api/frontpage', function(err, response, data){
        if(err){
            err.status = 502;
            console.error(err);
            next(err);
        } else {
            try{
                var parsedData = JSON.parse(data);
            } catch (err){
                console.error(err);
                next(err);
            }
            console.log(parsedData.front_page_lists[0]);
            res.locals.frontPageLists = parsedData.front_page_lists;
            next();
        }
    });
};

/**
 * Middleware to retrieve the default Playlist
 * @param {*} req 
 * @param {*} res 
 * @param {*} next 
 */
var retrieveFrontpageDefaultList = function(req, res, next) {
    request(process.env.MONGO_API + '/api/frontpage?list=' + defaultList, function(err, response, data){
        console.log(data);
        if(err){
            err.status = 502;
            console.error(err);
            next(err);
        } else {
            try{
                var frontPageDefaultList = JSON.parse(data);
                console.log(data);
            } catch (err){
                err.status = 500
                next(err);
            }
            res.locals.frontPageDefaultList = frontPageDefaultList.beverages;
            next();
        }
    });
};


/**
 * Render the frontpage with the retrieved data from the MongoApi
 * @param {*} req 
 * @param {*} res 
 */
var renderFrontpage = function(req, res) {
    res.render('index', 
        { 
            title: 'The Beverage Randomizer', 
            defaultList: res.locals.frontPageDefaultList,
            frontPageList: res.locals.frontPageLists
        });
}


module.exports = {
    renderFrontpage,
    retrieveFrontpageLists,
    retrieveFrontpageDefaultList
};