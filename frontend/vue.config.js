/* eslint-disable @typescript-eslint/no-var-requires */
const { preserveFunctionNamesWithTerser } = require("typesafe-vuex/helpers");

module.exports = {
  configureWebpack: (config) => {
    if (process.env.NODE_ENV === "production") {
      preserveFunctionNamesWithTerser(config);
    }
  },
  devServer: {
    proxy: {
      "/api/": {
        target: "http://backend:8000",
        https: true,
      },
      "/ws/": {
        target: "ws://backend:8000",
        secure: false,
        ws: true,
      },
    },
  },
};
