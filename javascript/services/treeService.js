class TreeService {
  constructor(model) {
    this.model = model;
  }

  async getNodes() {
    try {
      return this.model.findAll({ raw: true });
    } catch (error) {
      throw new Error(`Error getting nodes: ${error.message}`);
    }
  }

  async createNode(label, parent = null) {
    try {
      const node = await this.model.create({
        label,
        parentId: parent,
      });
      return node;
    } catch (error) {
      throw new Error(`Error creating node: ${error.message}`);
    }
  }

  async getNodeById(id) {
    try {
      return await this.model.findByPk(id);
    } catch (error) {
      throw new Error(`Error getting node by ID: ${error.message}`);
    }
  }
}

module.exports = TreeService;
