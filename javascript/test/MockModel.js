class MockModel {
  constructor() {
    this.data = [];
  }

  async findAll() {
    return this.data;
  }

  async create(node) {
    this.data.push(node);
    return node;
  }
}

module.exports = MockModel;
