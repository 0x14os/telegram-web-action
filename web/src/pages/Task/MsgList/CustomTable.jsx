import React, {useState, useEffect} from 'react';
import {Table, Dialog, Button} from '@alifd/next';
import styles from '../../../layouts/css/table.module.scss';
import {http} from '../../../tool/api/request';
import {msg} from '../../../tool/fun';

import useReactRouter from 'use-react-router';


export default function Home() {

    const [dataSource, setData] = useState([]);

    const route = useReactRouter();
    const history = route.history;

    const getList = (param) => {
        msg.loading("load list..");
        http.task.msg(param)
            .then(res => {
                msg.hide();
                if (res.code == 200) {
                    let data = res.data;
                    if (data.length > 0) {
                        for (let i = 0; i < data.length; i++) {
                            let v = data[i];
                            if (v.status == 1) {
                                data[i].status_name = '正常';
                            } else if (v.status == 2) {
                                data[i].status_name = '删除';
                            } else if (v.status == 0) {
                                data[i].status_name = '异常';
                            }
                        }
                        setData(data);
                    } else {
                        setData([]);
                    }
                } else {
                    setData([]);
                }
            })
            .catch(error => {
                // alert('login error');
                console.log('error', error);
            });
    };

    useEffect(() => {
        if (route.match.params.id != '0') {
            getList({task_id: route.match.params.id});
        }
    }, []);


    const popupShow = (title, content) => {
        const dialog = Dialog.show({
            title: title,
            content: content,
            footer: (
                <Button type="primary" onClick={() => dialog.hide()}>关闭</Button>
            )
        });
    };


    const renderOper = (value, index, record) => {
        // console.log("task id ", record.guid);
        const pushCon = () => {
            return popupShow("发送内容", record.text);
        };

        const del = () => {
            Dialog.confirm({
                title: '是否删除该群?',
                content: '删除后，不会对此群进行发送消息',
                onOk: () => {
                    msg.loading('load deletion..');
                    http.task.delMsg({msgId: record.id})
                        .then(res => {
                            msg.hide();
                            msg.success('successfully deleted.');
                            getList({page: current, status: 1});
                        }).catch(error => {
                            msg.help('failed delete');
                        });
                },
                onCancel: () => console.log('cancel')
            });
        };
        return (
            <div>
                <span className={styles.spanButton}>
                    <Button type="secondary" size="small" onClick={pushCon}>发送内容</Button>
                </span>
                <span className={styles.spanButton}>
                    <Button type="primary" size="small" onClick={del} warning>删除</Button>
                </span>
            </div>
        );
    };

    return (
        <div className={styles.tableContainer}>
            <Table
                dataSource={dataSource}
                className="custom-table"
            >
                <Table.Column
                    width={50}
                    lock="left"
                    title="ID"
                    dataIndex="id"
                    align="center"
                />
                {/*<Table.Column width={100} title="任务ID" dataIndex="task_id"/>*/}
                <Table.Column width={100} title="群名称" dataIndex="groupName"/>
                {/*<Table.Column width={100} title="群组ID" dataIndex="user_account_group_id"/>*/}
                {/*<Table.Column width={200} title="触发时间" dataIndex="status_time"/>*/}
                {/*<Table.Column width={80} title="状态" dataIndex="status_name"/>*/}
                <Table.Column width={120} title="创建日期" dataIndex="create_time"/>
                <Table.Column width={120} title="更新日期" dataIndex="update_time"/>
                <Table.Column
                    width={120}
                    title="操作"
                    cell={renderOper}
                    lock="right"
                    align="center"
                />

            </Table>


        </div>
    );
}

