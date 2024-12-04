/**
 * @swagger
 * tags:
 *   name: Tree
 *   description: Operations related to the Tree API
 */

/**
 * @swagger
 * /api/tree:
 *   get:
 *     summary: Retrieve Tree Data
 *     tags: [Tree]
 *     responses:
 *       '200':
 *         description: Successful response with tree data
 *         content:
 *           application/json:
 *             example:
 *               - 1:
 *                   label: "NewNode"
 *                   children:
 *                   - 2:
 *                       label: "New Node"
 *                       children: []
 *
 */
/**
 * @swagger
 * /api/tree:
 *   post:
 *     summary: Create a Tree Node
 *     tags: [Tree]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               label:
 *                 type: string
 *                 description: The label for the new node (alphanumeric)
 *                 example: "NewNode"
 *               parent:
 *                 type: integer
 *                 description: The ID of the parent node (optional)
 *                 example: 1
 *     responses:
 *       '201':
 *         description: Successfully created a new tree node
 *         content:
 *           application/json:
 *             example:
 *               id: 3
 *               label: "New Node"
 *               parent: 1
 *       '400':
 *         description: Bad Request, validation errors or invalid parent node
 *         content:
 *           application/json:
 *             example:
 *               errors:
 *                 label: "Label is required"
 *                 alphanumeric: "Label must be alphanumeric"
 *                 parent: "Invalid parent node."
 *                 general: "Error creating node."
 *       '500':
 *         description: Internal Server Error, failed to create node
 *         content:
 *           application/json:
 *             example:
 *               message: "Error creating node."
 */

const express = require('express');

const router = express.Router();
const { body, validationResult } = require('express-validator');

const TreeNode = require('../models/TreeNode');

const TreeService = require('../services/treeService');
const TreeUtils = require('../utils/treeUtils');
const TreeController = require('../controllers/treeControllers');

const treeServiceInstance = new TreeService(TreeNode);
const treeUtilsInstance = new TreeUtils();

const treeNodeController = new TreeController(treeServiceInstance, treeUtilsInstance);

// Validation middleware for the 'tree' POST route
const validateTreePost = [
  body('label')
    .notEmpty()
    .withMessage('Label is required')
    .isAlphanumeric()
    .withMessage('Label must be alphanumeric'),
  body('parent').optional(),
];

router.get('/tree', async (req, res) => {
  try {
    const tree = await treeNodeController.fetchTree();
    res.json(tree);
  } catch (error) {
    res.status(500).json({ message: 'Error fetching tree data.' });
  }
});

router.post('/tree', validateTreePost, async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }
    const { label, parent } = req.body;
    let parentNode;

    if (parent) {
      parentNode = await treeNodeController.getNodeById(parent);
      if (!parentNode) {
        return res.status(400).json({ message: 'Invalid parent node.' });
      }
    }
    const node = await treeNodeController.createNode(label, parent);
    return res.status(201).json(node);
  } catch (error) {
    return res.status(500).json({ message: 'Error creating node.' });
  }
});

module.exports = router;
