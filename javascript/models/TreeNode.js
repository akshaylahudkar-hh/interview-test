const { DataTypes } = require('sequelize');
const sequelize = require('../db');

const TreeNode = sequelize.define(
  'TreeNode',
  {
    id: {
      type: DataTypes.INTEGER,
      autoIncrement: true,
      primaryKey: true,
    },
    label: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    parentId: {
      type: DataTypes.INTEGER,
      references: {
        model: 'treenodes',
        key: 'id',
      },
    },
  },
  {
    tableName: 'treenodes',
    timestamps: false,
  },
);

TreeNode.belongsTo(TreeNode, { as: 'parent', foreignKey: 'parentId' });
TreeNode.hasMany(TreeNode, { as: 'children', foreignKey: 'parentId' });

module.exports = TreeNode;
