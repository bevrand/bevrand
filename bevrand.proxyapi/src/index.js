Promise = require('bluebird');
const { port, env } = require('./config/variables').server;
const app = require('./config/express');

app.listen(port, () => console.info(`ProxyApi Server started on port ${port} (${env})`));

module.exports = app;
