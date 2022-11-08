import axios from 'axios'
import {accessToken,logout} from '../fun'

//创建axios实例
const service = axios.create({
  baseURL: process.env.BASE_API, // api的base_url
  timeout: 20000, // 请求超时时间
  withCredentials: true, // 选项表明了是否是跨域请求,
});

//添加请求拦截器
service.interceptors.request.use(function (config) {
  const acc = accessToken();
  if (acc) {
    config.headers.Authorization = `${acc}`
    // console.log("config.headers===",config.headers);
  }

  return config;
}, function (error) {
  //请求错误时做些事
  return Promise.reject(error);
});


//拦截响应
service.interceptors.response.use(config => {
  return config;
}, err => {
  console.log('响应失败');
  return Promise.reject(err);
});

// respone拦截器
service.interceptors.response.use(
  response => {

    const res = response.data;

    if(res.code){
        // console.log("res====", res);

        if (res.code === 200) {
            return response.data;
        } else if (res.code > 200 && res.code !== 400) {
            return response.data;
        } else if (res.code == 400) {
            logout();
            // alert("安全退出中..");
            // lo().clear();
            jump('/login');
            // console.log("退出啦");
        } else {
            return Promise.reject('error')
        }
    }

  },
  error => {
    return Promise.reject(error);
  }
);

export default service;
