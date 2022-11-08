import React, {useState, useEffect, useCallback} from 'react';
import {Table, Pagination, Dialog, Button, Form, Input} from '@alifd/next';
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

    const route = useReactRouter();
    const history = route.history;

    const getList = (param) => {
        msg.loading('locaing..');
        param.uid = los.get("user_id");

        http.private.list(param)
            .then(res => {
                msg.hide();

                if (res.code == 200) {
                    let data = res.data.items;

                    if (data.length > 0) {

                        for (let i = 0; i < data.length; i++) {
                            let v = data[i];
                            if (v.status == 1) {
                                data[i].status_name = '待启动';
                            } else if (v.status == 2) {
                                data[i].status_name = '已启动';
                            } else {
                                data[i].status_name = '已结束';
                            }
                        }
                        setData(data);
                        setTotal(res.data.total);
                    }
                } else {
                    alert(res.message);
                    console.error('login error');
                }
            })
            .catch(error => {
                // alert('login error');
                console.log('error', error);
            });
    };

    useEffect(() => {
        getList({page: current, status: 1});
    }, []);


    const handlePagination = (current) => {
        setCurrent(current);
        getList({page: current, status: 1});
    };

    const renderOper = (value, index, record) => {
        const jumpEdit = () => {
            history.push('/private/edit/' + record.guid);
        };

        const jumpLog = () => {
            history.push('/private/log/' + record.guid);
        };

        let butNmae = "按钮错误";
        let stu = 0;
        if (record.status == 1) {
            butNmae = "启动";
            stu = 1;
        } else if (record.status == 2) {
            butNmae = "停止";
            stu = 2;
        }

        const popupStartConfirm = () => {
            Dialog.confirm({
                title: '是否确认' + butNmae,
                content: '启动咯，祝您今天开门大吉.',
                onOk: () => {
                    msg.loading('load deletion..');
                    http.private.start({guid: record.guid, status: stu})
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

        const popupStopConfirm = () => {
            let uid = los.get("user_id");
            Dialog.confirm({
                title: '请确认停止？',
                content: '停止私信群发..',
                onOk: () => {
                    msg.loading('load deletion..');
                    http.private.stop ({guid: record.guid, uid: uid})
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

        const popupDelConfirm = () => {
            let uid = los.get("user_id");
            Dialog.confirm({
                title: '请您确认删除？',
                content: '请注意,删除该项会导致关联数据全部清空.',
                onOk: () => {
                    msg.loading('load deletion..');
                    http.private.del ({guid: record.guid, uid: uid})
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

        const butView = () => {
            return (
                <div>
                    {stu == 1 || stu == 2? (  <span className={styles.spanButton}>
                        <Button type={stu == 1? "secondary" :"primary"} size="small" onClick={stu == 1 ? popupStartConfirm : popupStopConfirm}>{butNmae}</Button>
                    </span>):''}

                    <span className={styles.spanButton}>
                        <Button type="normal" size="small" onClick={jumpEdit}>编辑</Button>
                    </span>

                    <span className={styles.spanButton}>
                        <Button type="normal" size="small" onClick={jumpLog}>发送列表</Button>
                    </span>

                    <span className={styles.spanButton}>
                        <Button type="normal" size="small" onClick={popupDelConfirm} warning>删除</Button>
                    </span>
                </div>
            );
        };
        return butView();
    };


    return (
        <div className={styles.tableContainer}>
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
                <Table.Column width={150} title="标题" dataIndex="title"/>
                <Table.Column width={200} title="关键词" dataIndex="soKey"/>
                <Table.Column width={100} title="总数量" dataIndex="sendNumber"/>
                <Table.Column width={100} title="账号数量" dataIndex="accountNumber"/>
                <Table.Column width={100} title="账号条数" dataIndex="sendAccountNumber"/>
                <Table.Column width={100} title="休眠时间" dataIndex="timer"/>
                <Table.Column width={100} title="备注" dataIndex="remark"/>
                <Table.Column width={200} title="状态" dataIndex="status_name"/>
                <Table.Column width={200} title="创建日期" dataIndex="create_time"/>
                <Table.Column width={200} title="更新日期" dataIndex="update_time"/>

                <Table.Column
                    width={300}
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

