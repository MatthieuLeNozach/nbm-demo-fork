// vetur.config.js
// Vue tooling for VS Code
// See : https://vuejs.github.io/vetur/
/* @type {import('vls').VeturConfig} */
module.exports = {
  settings: {
    "vetur.useWorkspaceDependencies": true,
    "vetur.experimental.templateInterpolationService": true,
  },
  projects: [
    {
      root: "./frontend",
      package: "./package.json",
      tsconfig: "./tsconfig.json",
      snippetFolder: "./.vscode/vetur/snippets",
      globalComponents: ["./src/components/**/*.vue"],
    },
  ],
};
