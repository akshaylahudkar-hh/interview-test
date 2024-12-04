class TreeController {
  constructor(treeService, treeUtils) {
    this.treeService = treeService;
    this.treeUtils = treeUtils;
  }

  async fetchTree() {
    const nodes = await this.treeService.getNodes();
    const nodeDict = this.treeUtils.transformNodesIntoDict(nodes);
    return this.treeUtils.buildTree(nodeDict);
  }

  async createNode(label, parent = null) {
    return this.treeService.createNode(label, parent);
  }

  async getNodeById(id) {
    return this.treeService.getNodeById(id);
  }
}

module.exports = TreeController;
