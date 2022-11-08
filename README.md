## telegram-web-action

telegram,web电报,纸飞机,群控,多用户,群发,批量提取群成员,批量私信群发,任意语言文字搜索全球telegram群

```text
系统功能包含:
多用户,也许可以有惊喜,haha
批量自动加群(不包含打码验证)
新建群（邀请成员
群成员提取(活跃度<15天)
群消息发送
私信群发(根据关键词锁定群名称发送)
批量导入协议号
任意语言文字搜索全球telegram群
```

## PS
```text
没有商用过，算是自己产品定位推广，习惯开发产品是多用户，就顺手写了多用户。。。

这个可以研究，学习，总之你想干啥，就自己研究呗,基础都有了，高楼大厦自己建造吧。。。
```


## develop 
```text
api->
python to 3.7.13
mysql 8.*
library->api/requirements.txt

fn->
node.js to v12.*.?
react to ice.work and ice-scripts is version ^2.0.0 
```

### sql
```text
tgwc.sql 
```

## 后台账号
```text
id：x@x.com
passwd:to123456
如果密码错误，请根据登录逻辑或者创建账号逻辑，重新生成一份
```

### 后台api结构入口
```text
http web api 统一路口->api.py
telegram api 交互->worker.py 
定时任务与队列->aps.py
自动注册 telegram id->auto.py 未完成,缺少sms接码api
监控http服务 ->monitor.py ,未完成,缺少通知
```
