module.exports = {
  authentication: require('./authentication').router,
  playlist: require('./playlist').router,
  randomizer: require('./randomizer').router,
  swagger: require("./swagger").router,
}