module.exports = {
  env: {
    es6: true,
    node: true,
  },
  extends: [
    'airbnb-base',
    'plugin:jest/recommended',
  ],
  plugins: ['jest'],
  globals: {
    Atomics: 'readonly',
    SharedArrayBuffer: 'readonly',
  },
  parserOptions: {
    ecmaVersion: 2018,
    sourceType: 'module',
  },
  rules: {
    'no-console': 'off', // Disable the no-console rule
    'class-methods-use-this': 'off', // Disable the class-methods-use-this rule
  },
};
