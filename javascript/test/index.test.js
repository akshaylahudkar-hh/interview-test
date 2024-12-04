/* eslint-disable*/
const request = require('supertest');
const { app, server } = require('../index');

jest.mock('../db', () => {
  const { Sequelize } = require('sequelize');
  return new Sequelize({
    dialect: 'sqlite',
    storage: ':memory:',
    logging: false
  });
});

describe('TreeNode Routes', () => {
  describe('GET /api/tree', () => {
    it('should return an empty array if no nodes exist', async () => {
      const res = await request(app).get('/api/tree');
      expect(res.statusCode).toEqual(200);
      expect(res.body).toEqual([]);
    });
  });

  describe('POST /api/tree', () => {
    it('should create a new node and return it', async () => {
      const res = await request(app)
        .post('/api/tree')
        .send({ label: 'newnode1', parent: null });
      expect(res.statusCode).toEqual(201);
      expect(res.body).toHaveProperty('id');
      expect(res.body.label).toEqual('newnode1');
      expect(res.body.parentId).toBeNull();
    });

    it('should return a 400 error if the label is missing', async () => {
      const res = await request(app)
        .post('/api/tree')
        .send({ parent: null });
      expect(res.statusCode).toEqual(400);
    });

    it('should return a 400 error if the parent node does not exist', async () => {
      const res = await request(app)
        .post('/api/tree')
        .send({ label: 'new node', parent: 9999 });
      expect(res.statusCode).toEqual(400);
    });

    it('should return a 400 error if the label is not alphanumeric', async () => {
      const res = await request(app)
        .post('/api/tree')
        .send({ label: 'Node#' });
      expect(res.statusCode).toEqual(400);
    });
  });

  afterAll(async () => {
    await server.close();
  });
});
jest.spyOn(global.console, 'log').mockImplementation(() => jest.fn());