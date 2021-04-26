require("dotenv").config({ path: "./.env" });

module.exports = {
  poweredByHeader: false,
  webpackDevMiddleware: (config) => {
    config.watchOptions = {
      poll: 1000,
      aggregateTimeout: 300,
    };

    return config;
  },
  env: {
    API_URL: process.env.API_URL,
  },
  i18n: {
    locales: ["en", "fr", "es"],
    defaultLocale: "en",
  },
  webpack: (config, { isServer }) => {
    // Fixes npm packages that depend on `fs` module
    if (!isServer) {
      config.node = {
        fs: "empty",
      };
    }

    return config;
  },
};
