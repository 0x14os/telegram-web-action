import React, {useState, useEffect, useCallback} from 'react';
import {Table, Pagination, Dialog, Button, Drawer, Input, Tab} from '@alifd/next';
import styles from '../../../layouts/css/table.module.scss';
import {http} from '../../../tool/api/request';
import {msg, lo, isNull} from '../../../tool/fun';

const los = lo();

import useReactRouter from 'use-react-router';


export default function Home() {

    const [current, setCurrent] = useState(1);
    const [dataTotal, setTotal] = useState(0);
    const [dataPage, setPage] = useState(30);
    const [dataSource, setData] = useState([]);
    const [activationCode, setActivationCode] = useState();
    const [visible, setVisible] = useState(false);
    const [joinText, setJoinText] = useState("");
    const [tid, setTid] = useState("");

    const route = useReactRouter();
    const history = route.history;


    const onOpen = () => {
        setVisible(true);
    };

    const onClose = (reason, e) => {
        setVisible(false);
    }

    const getList = (param) => {
        msg.loading('locaing..');
        param.uid = los.get("user_id");
        http.account.list(param)
            .then(res => {
                msg.hide();
                if (res.code == 200) {
                    let data = res.data.items;
                    console.log("data.length:", data.length);
                    if (data.length > 0) {
                        for (let i = 0; i < data.length; i++) {
                            let v = data[i];
                            if (v.status == 1) {
                                data[i].status_name = '开启';
                            } else {
                                data[i].status_name = '关闭';
                            }

                            if (v.mode == 1) {
                                data[i].modeName = "群发";
                            } else {
                                data[i].modeName = "1v1";
                            }

                            if (v.is_activation == 1) {
                                data[i].activation_name = '未激活';
                            } else if (v.is_activation == 2) {
                                data[i].activation_name = '已激活';
                            } else if (v.is_activation == 3) {
                                data[i].activation_name = '注销';
                            }
                        }
                        setData(data);
                        setTotal(res.data.total);
                    } else {
                        setData([]);
                        setTotal(0);
                    }
                } else {
                    msg.error(res.message);
                    // console.error('login error');
                }
            })
            .catch(error => {
                // alert('login error');
                console.log('error', error);
            });
    };

    useEffect(() => {
        getList({page: current, status: 1});
        // setActivationCode(0);
    }, []);


    const handlePagination = (current) => {
        setCurrent(current);
        getList({page: current, status: 1});
    };

    const codeChange = (value) => {
        setActivationCode(value);
        console.log("======", activationCode);
        if (values.length >= 6) {
            msg.error("您的验证码有误");
        } else {
            console.log("========values", value);
        }
    };


    const renderOper = (value, index, record) => {

        const jumpGroupList = () => {
            history.push('/account/group/list/' + record.guid);
        };

        const jumpEdit = () => {
            history.push('/account/edit/' + record.guid);
        };


        const jumpCode = () => {
            history.push('/account/code/' + record.guid);
        };


        const jumpSend = () => {
            msg.loading("加载请求..");
            let param = {};
            param.uid = record.user_id;
            param.tid = record.guid;
            console.log("param", param);

            http.account.getCode(param)
                .then(res => {
                    msg.hide();
                    if (res.code == 200) {
                        history.push('/account/list');
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


        let butNmae = "按钮错误";
        let stu = 0;
        if (record.status == 1) {
            butNmae = "关闭账号";
            stu = 2;
        } else if (record.status) {
            butNmae = "开启账号";
            stu = 1;
        }

        const popupConfirm = () => {
            Dialog.confirm({
                title: '是否确认' + butNmae,
                content: '账户删除，正在执行的任务，即全部删除.',
                onOk: () => {
                    msg.loading('load deletion..');
                    http.account.status({guid: record.guid, status: stu})
                        .then(res => {
                            msg.hide();
                            if (res.code == 200) {
                                msg.success('successfully deleted.');
                                getList({page: current, status: 1});
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
            let uid = los.get("user_id");
            Dialog.confirm({
                title: '更新群功能.',
                content: '请注意，目前更新群功能是测试阶段,请勿多次点击.',
                onOk: () => {
                    msg.loading('load deletion..');
                    http.account.getGroup({tid: record.guid, uid: uid})
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


        let is_activation = record.is_activation;

        // console.log("is_activation===", is_activation);
        let tid = record.guid;

        const openJoinGroup = (record) => {
            console.log("openJoinGroup:", tid);
            setTid(tid)
            onOpen();
        }

        const activation = () => {

            if (is_activation == 2) {
                return (
                    <div>
                        <span className={styles.spanButton}>
                            <Button size="small" onClick={openJoinGroup}>自动加群</Button>
                        </span>

                        <span className={styles.spanButton}>
                            <Button size="small" onClick={jumpGroupList}>群管理功能</Button>
                        </span>

                        {record.is_group == 1 ? (<span className={styles.spanButton}>
                            <Button type="secondary" size="small" onClick={popupConfirmGroup}>同步群列表</Button>
                        </span>) : ''}

                        <span className={styles.spanButton}>
                                <Button type="normal" size="small" onClick={popupConfirm} warning>{butNmae}</Button>
                        </span>
                    </div>
                );

            } else {
                if (record.mode !== 2) {
                    return (
                        <div>
                        <span className={styles.spanButton}>
                            <Button type="secondary" size="small" onClick={jumpSend}>获取验证码</Button>
                        </span>

                            <span className={styles.spanButton}>
                            <Button type="normal" size="small" onClick={jumpCode} warning>输入验证码</Button>
                        </span>

                            <span className={styles.spanButton}>
                            <Button type="normal" size="small" onClick={jumpEdit}>编辑账户</Button>
                        </span>
                        </div>
                    );
                }
            }
        };
        if (record.is_activation === 3) {
            return (<div></div>)
        } else {
            return activation();
        }
    };

    const onJoinTextChange = (val, e) => {
        // console.log("join:",val);
        setJoinText(val)
    };


    const subPost = () => {
        console.log(joinText);
        console.log("tid", tid);
        http.account.joinGroup({tid: tid, groupLink: joinText})
            .then(res => {
                msg.hide();
                if (res.code == 200) {
                    msg.success("提交成功");
                    getList({page: current, status: 1});
                } else {
                    msg.error("提交失败");
                }
            }).catch(error => {
            // alert('login error');
            console.log('error', error);
        });
    };


    const onTabChange = (key) => {
        //all,active,invalid
        console.log(key);
        if (key == "all") {
            getList({page: current, status: 1});
        } else if (key == "active") {
            getList({page: current, status: 2});
        } else if (key == "invalid") {
            getList({page: current, status: 3});
        } else {
            msg.error("数据异常..");
        }
    };

    const viewTable = () => {
        return (
            <div>
                <Table
                    dataSource={dataSource}
                    className="custom-table"
                >

                    <Table.Column
                        width={100}
                        lock="left"
                        title="ID"
                        dataIndex="id"
                        align="center"
                    />
                    <Table.Column width={150} title="模式" dataIndex="modeName"/>
                    <Table.Column width={150} title="用户名" dataIndex="username"/>
                    <Table.Column width={200} title="手机号码" dataIndex="phone"/>
                    <Table.Column width={200} title="api名称" dataIndex="api_name"/>
                    <Table.Column width={150} title="api id" dataIndex="api_id"/>
                    <Table.Column width={200} title="api hash" dataIndex="api_hash"/>
                    <Table.Column width={100} title="群组数量" dataIndex="group_count"/>
                    <Table.Column width={100} title="定时任务" dataIndex="task_count"/>
                    <Table.Column width={100} title="激活状态" dataIndex="activation_name"/>
                    <Table.Column width={200} title="状态" dataIndex="status_name"/>
                    <Table.Column width={200} title="创建日期" dataIndex="create_time"/>
                    <Table.Column width={200} title="更新日期" dataIndex="update_time"/>

                    <Table.Column
                        width={500}
                        title="操作"
                        cell={renderOper}
                        lock="right"
                        align="center"
                    />

                </Table>

                <Pagination
                    className={styles.pagination}
                    current={current}
                    onChange={handlePagination}
                    pageSize={dataPage}
                    total={dataTotal}
                />
            </div>
        );
    }


    return (
        <div className={styles.tableContainer}>
            <Tab shape="pure" onChange={onTabChange}>
                <Tab.Item key="active" title="活跃">
                    {viewTable()}
                </Tab.Item>
                <Tab.Item key="invalid" title="注销">
                    {viewTable()}
                </Tab.Item>
                <Tab.Item key="all" title="所有">
                    {viewTable()}
                </Tab.Item>
            </Tab>
            <Drawer
                title="自动加群"
                placement="right"
                visible={visible}
                onClose={onClose}
            >
                ps：一行一个群链接
                <Input.TextArea
                    name="api_certificate"
                    placeholder="请输入群链接"
                    aria-label="auto height"
                    onChange={onJoinTextChange}
                    autoHeight={{minRows: 30, maxRows: 15}}
                />

                <Button type="secondary" onClick={subPost} size="small"
                        style={{margin: "5px 0 5px", padding: "0 75px"}}>
                    执行加群
                </Button>
            </Drawer>

        </div>

    );
}

