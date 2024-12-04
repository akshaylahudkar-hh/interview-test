const TreeUtils = require('../utils/treeUtils');

jest.mock('../models/TreeNode');

describe('TreeUtils', () => {
  let treeUtils;

  beforeEach(() => {
    treeUtils = new TreeUtils();
  });

  describe('buildTree', () => {
    it('should correctly build a tree from a dictionary of nodes', () => {
      // this is a dict where key is the parentId and value are the children
      // I made this optimization to improve the retrieval complexity
      const dict = {
        1: [
          { id: 2, label: 'ant', parentId: 1 },
          { id: 3, label: 'bear', parentId: 1 },
          { id: 7, label: 'frog', parentId: 1 },
        ],
        3: [
          { id: 4, label: 'cat', parentId: 3 },
          { id: 5, label: 'dog', parentId: 3 },
        ],
        5: [
          { id: 6, label: 'elephant', parentId: 5 },
        ],
        null: [
          { id: 1, label: 'root', parentId: null },
        ],
      };
      const expectedTree = [
        {
          1: {
            label: 'root',
            children: [
              {
                2: {
                  label: 'ant',
                  children: [],
                },
              },
              {
                3: {
                  label: 'bear',
                  children: [
                    {
                      4: {
                        label: 'cat',
                        children: [],
                      },
                    },
                    {
                      5: {
                        label: 'dog',
                        children: [
                          {
                            6: {
                              label: 'elephant',
                              children: [],
                            },
                          },
                        ],
                      },
                    },
                  ],
                },
              },
              {
                7: {
                  label: 'frog',
                  children: [],
                },
              },
            ],
          },
        },
      ];
      expect(treeUtils.buildTree(dict)).toEqual(expectedTree);
    });
  });

  describe('transformNodesIntoDict', () => {
    it('should correctly transform nodes into dict', async () => {
      // Mock the findAll method to return a predefined list of nodes
      const nodes = [
        { id: 1, label: 'root', parentId: null },
        { id: 2, label: 'child', parentId: 1 },
      ];

      const expecteddict = {
        null: [{ id: 1, label: 'root', parentId: null }],
        1: [{ id: 2, label: 'child', parentId: 1 }],
      };

      const dict = treeUtils.transformNodesIntoDict(nodes);
      expect(dict).toEqual(expecteddict);
    });
  });
});
