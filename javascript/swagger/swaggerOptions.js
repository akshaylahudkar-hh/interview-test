const path = require('path');

const swaggerOptions = {
  swaggerDefinition: {
    openapi: '3.0.0',
    info: {
      title: 'Tree API',
      version: '1.0.0',
      description: 'API documentation for the Tree API',
    },
  },
  apis: [path.resolve(__dirname, '../routes/treeRoutes.js')],
};
module.exports = swaggerOptions;
