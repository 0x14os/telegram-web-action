import React, {useEffect, useState} from 'react';
import {Icon, Grid, Button, Dialog, Input} from '@alifd/next';
import styles from './index.module.scss';

import useReactRouter from 'use-react-router';

import {http} from '../../tool/api/request';

import {msg, lo} from '../../tool/fun';

const los = lo();


const {Row, Col} = Grid;


export default function Index() {


    const [dataTotal, setTotal] = useState(0);
    const [dataPage, setPage] = useState(30);
    const [data, setData] = useState([]);
    const [activationCode, setActivationCode] = useState(0);
    const [initCode, setInitCode] = useState(0);
    const [dialogClose, setDialogClose] = useState(false);


    const routeResult = useReactRouter();
    const history = routeResult.history;

    const handleJumpAddId = () => {
        history.push('/account/edit/0');
    };


    const getList = (param) => {
        msg.loading('locaing..');

        param.uid = los.get("user_id");

        http.account.list(param)
            .then(res => {
                msg.hide();
                if (res.code == 200) {
                    let data = res.data.items;

                    if (data.length > 0) {

                        for (let i = 0; i < data.length; i++) {
                            let v = data[i];
                            if (v.status == 1) {
                                data[i].status_name = '开启';
                            } else {
                                data[i].status_name = '关闭';
                            }

                            if (v.is_activation == 1) {
                                data[i].activation_name = '未激活';
                            } else if (v.is_activation == 2) {
                                data[i].activation_name = '已激活';
                            } else {
                                data[i].activation_name = '异常';
                            }
                        }
                        setData(data);
                        setTotal(res.data.total);
                    }
                } else {
                    setData([]);
                    setTotal(0);
                }
            })
            .catch(error => {
                console.log('error', error);
            });
    };

    useEffect(() => {
        getList({page: 1, status: 1});
        // setActivationCode(0);
    }, []);


    const but = (item) => {
        let uid = los.get("user_id");
        let butNmae = "按钮错误";
        let stu = 0;
        if (item.status == 1) {
            butNmae = "关闭账号";
            stu = 2;
        } else if (item.status) {
            butNmae = "开启账号";
            stu = 1;
        }

        const getCode = () => {
            msg.loading("加载请求..");
            let param = {};
            param.uid = item.user_id;
            param.tid = item.guid;
            console.log("param", param);
            http.account.getCode(param)
                .then(res => {
                    msg.hide();
                    if (res.code == 200) {
                        history.push('/dashboard');
                    } else {
                        msg.error("请求错误..");
                        console.error('error', error);
                    }
                })
                .catch(error => {
                    msg.error("请求错误..");
                    console.log('error', error);
                });
        };


        const onDialogOpen = () => {
            setDialogClose(true);
            console.log(initCode);
        };

        const onDialogClose = () => {
            setDialogClose(false);
            setInitCode(0);
            console.log(initCode);
        };

        const onChangeDialog = (value) => {
            setInitCode(value);
            console.log(value);
        };

        const onCancelDialog = () => {
            setDialogClose(false);
            setInitCode(0);
            console.log(initCode);
        };

        const onOkDialog = () => {
            console.log(initCode);

            let param = {};
            param.uid = item.user_id;
            param.guid = item.guid;
            param.code = initCode;
            console.log(param);
            msg.loading("正在验证激活..");
            http.account.activation(param)
                .then(res => {
                    msg.hide();
                    if (res.code == 200) {
                        history.push('/dashboard');
                    } else {
                        msg.error("请求错误..");
                    }
                })
                .catch(error => {
                    msg.error("请求错误..");
                    // console.log('error', error);
                });
        };

        const jumpGroupList = () => {
            history.push('/account/group/list/' + item.guid);
        };

        const jumpEdit = () => {
            history.push('/account/edit/' + item.guid);
        };

        const popupConfirm = () => {
            Dialog.confirm({
                title: '是否确认' + butNmae,
                content: '账户删除，正在执行的任务，即全部删除.',
                onOk: () => {
                    msg.loading('load deletion..');
                    http.account.status({guid: item.guid, status: stu})
                        .then(res => {
                            msg.hide();
                            if (res.code == 200) {
                                msg.success('successfully deleted.');
                                getList({page: 1, status: 1});
                            } else {
                                msg.help('failed delete');
                            }
                        })
                        .catch(error => {
                            msg.help('failed delete');
                        });
                },
                onCancel: () => console.log('cancel')
            });
        };


        const popupConfirmGroup = () => {

            Dialog.confirm({
                title: '更新群功能.',
                content: '请注意，目前更新群功能是测试阶段,请勿多次点击.',
                onOk: () => {
                    msg.loading('load deletion..');
                    http.account.getGroup({tid: item.guid, uid: uid})
                        .then(res => {
                            msg.hide();
                            if (res.code == 200) {
                                msg.success('请求成功..');
                                getList({page: current, status: 1});
                            } else {
                                msg.help('failed delete');
                            }
                        })
                        .catch(error => {
                            msg.error('error');
                        });
                },
                onCancel: () => console.log('cancel')
            });
        };


        let is_activation = item.is_activation;
        if (is_activation == 2) {
            return (
                <div>
                    <span className={styles.spanP10}>
                        <Button size="small" onClick={jumpGroupList}>
                            <Icon type="set"/>
                             群功能管理
                         </Button>
                    </span>
                    {item.is_group == 1 ?
                        <span className={styles.spanP10}>
                            <Button size="small" type="primary" onClick={popupConfirmGroup}>
                                <Icon type="refresh"/>
                                 同步群列表
                             </Button>
                        </span> : ''}
                    <span className={styles.spanP10}>
                         <Button type="primary" size="small" warning onClick={popupConfirm}>
                             {stu == 2 ? <Icon type="delete-filling"/> : <Icon type="success-filling"/>}
                             {butNmae}
                        </Button>
                    </span>
                </div>
            );
        } else {
            return (
                <div>
                    <span className={styles.spanP10}>
                         <Button size="small" onClick={getCode}>
                           <Icon type="account"/>
                            获取验证码
                         </Button>
                    </span>
                    <span className={styles.spanP10}>
                        <Button size="small" warning onClick={onDialogOpen}>
                            <Icon type="switch"/>
                            输入验证码
                        </Button>
                    </span>

                    <span className={styles.spanP10}>
                        <Button type="primary" size="small" onClick={jumpEdit}>
                            <Icon type="edit"/>
                            编辑账户
                        </Button>
                    </span>

                    <Dialog
                        title="激活电报账号"
                        visible={dialogClose}
                        onOk={onOkDialog}
                        onCancel={onCancelDialog}
                        onClose={onDialogClose}>
                        <Input size="large" placeholder="请输入验证码" onChange={onChangeDialog} maxLength={5}
                               htmlType="number"/>
                    </Dialog>

                </div>
            );
        }
    };

    let tgStatus = los.get("tgStatus");
    let role = los.get("role");
    console.log("tgStatus:", tgStatus);
    let statusx = 0;
    if (role == 1) {
        statusx = 1;
    } else if (role == 2 && tgStatus == 1) {
        statusx = 1;
    } else {
        statusx = 2;
    }
    return (
        <div className={styles.container}>
            {/*<Filter />*/}
            <Row wrap gutter="20">

                <Col l="6" xs="12" xxs="24">
                    {statusx == 1 ? <div className={`${styles.card} ${styles.createScheme}`} onClick={handleJumpAddId}>
                        <Icon type="add" size="large" className={styles.addIcon}/>
                        <span>新增账号</span>
                    </div> : <div className={`${styles.card} ${styles.createScheme}`}>
                        <Icon type="refresh" size="large" className={styles.addIcon}/>
                        <span>账号已满</span>
                    </div>}
                </Col>

                {data.map((item, index) => {


                    return (
                        <Col l="6" xs="12" xxs="24" key={index}>
                            <div className={styles.card}>
                                <div className={styles.head}>
                                    <h4 className={styles.title}>{item.api_name}</h4>
                                    {/*<p className={styles.desc}>激活状态:{item.activation_name}</p>*/}
                                </div>

                                <div className={styles.body}>

                                    <p className={`${styles.creator} ${styles.info}`}>
                                        <span className={`${styles.spanMr}`}>账号状态：{item.status_name}</span>
                                        <span className={`${styles.spanMr}`}>激活状态：{item.activation_name}</span>
                                    </p>

                                    <p className={`${styles.leader} ${styles.info}`}>
                                        <span className={`${styles.spanMr}`}>群数量：{item.group_count}</span>
                                        <span className={`${styles.spanMr}`}>定时任务：{item.task_count}</span>
                                    </p>

                                    <p className={`${styles.time} ${styles.info}`}>
                                        更新时间：
                                        {item.update_time}
                                    </p>
                                    <p className={`${styles.time} ${styles.info} ${styles.hx}`}>
                                        {but(item)}
                                    </p>
                                </div>

                            </div>
                        </Col>
                    );
                })}
            </Row>
        </div>
    );
}
