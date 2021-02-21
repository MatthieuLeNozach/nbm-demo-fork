module.exports = {
  poweredByHeader: false,
  webpackDevMiddleware: (config) => {
    config.watchOptions = {
      poll: 1000,
      aggregateTimeout: 300,
    };

    return config;
  },

  i18n: {
    locales: ["en", "fr", "es"],
    defaultLocale: "en",
  },
};
