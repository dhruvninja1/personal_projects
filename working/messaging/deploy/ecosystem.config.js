// PM2 ecosystem config
// serverManagement.js spawns dmserver.js and all chat servers on startup
// Usage: cd messaging && pm2 start deploy/ecosystem.config.js
module.exports = {
  apps: [
    {
      name: 'messaging',
      script: 'serverManagement.js',
      cwd: './server',
      env: {
        NODE_ENV: 'production',
      },
    },
  ],
};
