const { port, env } = require('./config').server;
const app = require('./api');

/* eslint-disable no-console */
app.listen(port, () => console.info(`ProxyApi Server started on port ${port} (${env})`));

module.exports = app;
