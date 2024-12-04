// index.js
const express = require('express');
const swaggerJsdoc = require('swagger-jsdoc');
const swaggerUi = require('swagger-ui-express');
const sequelize = require('./db');
const treeRoutes = require('./routes/treeRoutes');
const swaggerOptions = require('./swagger/swaggerOptions');

const app = express();
const port = 3001;

app.use(express.json());

sequelize.sync()
  .then(() => {})
  .catch((error) => {
    console.log('An error occurred while creating the table:', error);
  });

app.use('/api', treeRoutes);

// Initialize swagger-jsdoc
const swaggerSpec = swaggerJsdoc(swaggerOptions);

// Use Swagger UI middleware
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerSpec));

app.get('/', (req, res) => res.send('Hello World!'));

const server = app.listen(port, () => console.log(`Example app listening on port ${port}!`));

module.exports = {
  app,
  server,
};

process.on('SIGTERM', () => {
  server.close(() => {
    console.log('Server closed');
  });
});
