module.exports = {
  apps : [{
    name: 'tgWeb',
    script: 'serve -p 3002 -s build',
    // script: 'server.js',

    // Options reference: https://pm2.io/doc/en/runtime/reference/ecosystem-file/
    args: 'one two',
    instances: 1,
    autorestart: true,
    watch: false,
    // max_memory_restart: '1G',
    // env: {
    //   PM2_SERVE_PATH: '.',
    //   PM2_SERVE_PORT: 8080,
    //   // NODE_ENV: 'development'
    // },
    // env_production: {
    //   NODE_ENV: 'production'
    // }
  }],

  // deploy : {
  //   production : {
  //     user : 'node',
  //     host : '212.83.163.1',
  //     ref  : 'origin/master',
  //     repo : 'git@github.com:repo.git',
  //     path : '/var/www/production',
  //     'post-deploy' : 'npm install && pm2 reload ecosystem.config.js --env production'
  //   }
  // }

};
