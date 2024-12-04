class TreeUtils {
  buildTree(dict, parentId = null) {
    const res = [];
    if (parentId in dict) {
      dict[parentId].forEach((node) => {
        const tree = {};
        tree[node.id] = {
          label: node.label,
          children: this.buildTree(dict, node.id),
        };
        res.push(tree);
      });
    }
    return res;
  }

  // this is a dict where key is the parentId and value are the children
  // I made this optimization to improve the retrieval complexity
  transformNodesIntoDict(nodes) {
    const nodeDict = {};
    nodes.forEach((node) => {
      if (node.parentId in nodeDict) {
        nodeDict[node.parentId].push(node);
      } else {
        nodeDict[node.parentId] = [node];
      }
    });
    return nodeDict;
  }
}

module.exports = TreeUtils;
