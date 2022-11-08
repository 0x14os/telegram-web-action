
#部署测试 & node v8.16.0 and nvpm ^6+
```text
npm install -g serve
npm install -g pm2
npm install -g pushstate-server
> https://www.jianshu.com/p/47cfac0d69b0

```

#start 
```text
npm run build
pm2 start ecosystem.config.js
```


#nginx test

```text

upstream tg {
    server 127.0.0.1:8091;
}

server {
    listen 80;
    server_name tg.cn381.com
    index index.html index.htm;
    root /usr/local/work/tg/web;
	location / {
		try_files $uri $uri/ /index.html;
	}
           
    location /v1 {
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_pass http://tg;
        #add_header Access-Control-Allow-Origin *;
        #add_header Access-Control-Allow-Methods 'GET, POST';
        #add_header Access-Control-Allow-Headers 'DNT,X-Mx-ReqToken,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Authorization';
        #client_max_body_size 10M;
    }

	location ~ .*\.(gif|jpg|jpeg|png|bmp|swf)$
	{
		expires 30d;
	}

	location ~ .*\.(js|css)?$
	{
		expires 1h;
	}

	error_page   500 502 503 504  /50x.html;
    location = /50x.html {
         root   /usr/share/nginx/html;
    }

}
```




# ice-design-ecommerce

## 使用

- 启动调试服务: `npm start`
- 构建 dist: `npm run build`

## 目录结构

- react-router @4.x 默认采用 hashHistory 的单页应用
- 入口文件: `src/index.js`
- 导航配置: `src/menuConfig.js`
- 路由配置: `src/routerConfig.js`
- 路由入口: `src/router.jsx`
- 布局文件: `src/layouts`
- 通用组件: `src/components`
- 页面文件: `src/pages`

## 配色

- 主色：#447eff
- 功能主色：#5e83fb、#f7da47、#58ca9a、#ee706d
- 字体颜色：#333、#666

## 效果图

![screenshot](https://img.alicdn.com/tfs/TB1O_6jDOrpK1RjSZFhXXXSdXXa-2860-1580.png)
