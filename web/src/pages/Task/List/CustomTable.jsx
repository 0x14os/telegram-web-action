import React, {useState, useEffect} from 'react';
import {Table, Pagination, Balloon, Icon, Button, Dialog} from '@alifd/next';
import styles from '../../../layouts/css/table.module.scss';
import {http} from '../../../tool/api/request';
import {msg,lo} from '../../../tool/fun';
import useReactRouter from 'use-react-router';

const los = lo();

export default function Home() {

    const [current, setCurrent] = useState(1);
    const [dataTotal, setTotal] = useState(0);
    const [dataSource, setData] = useState([]);

    const route = useReactRouter();
    const history = route.history;

    const getList = (param) => {

        msg.loading("load list..");
        http.task.list(param)
            .then(res => {
                msg.hide();
                if (res.code == 200) {

                    if (res.data.items.length > 0) {
                        let data = res.data.items;
                        for (let i = 0; i < data.length; i++) {
                            let v = data[i];

                            if (v.status == 1) {
                                data[i].status_name = '正常';
                            } else {
                                data[i].status_name = '删除';
                            }

                            if (v.method == 'interval') {
                                data[i].methodName = '间隔';
                            } else {
                                data[i].methodName = '一次性';
                            }
                        }
                        setData(data);
                        setTotal(res.data.total);
                    }else{
                        setData([]);
                        setTotal(0);
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
        getList({page: current});
    }, []);


    const handlePagination = (current) => {
        setCurrent(current);
        getList({page: current});
    };

    const renderOper = (value, index, record) => {

        const jump = () => {
            // console.log("jump id", '/task/msg/list/' + record.guid);
            history.push('/task/msg/list/' + record.guid + '/' + record.title);
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
                content: '开始循环群发信息?',
                onOk: () => {
                    msg.loading('load deletion..');
                    http.group.start({guid: record.guid, status: stu})
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
                content: '停止循环发送群发?',
                onOk: () => {
                    msg.loading('load deletion..');
                    http.group.stop ({guid: record.guid, uid: uid})
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

        const del = () => {
            let userId = los.get('user_id');
            console.log("userId:",userId);
            msg.loading('Normal deletion..');
            http.task.del({guid: record.guid,userId:userId})
                .then(res => {
                    msg.hide();
                    console.log(res);
                    if (res.code == 200) {
                        msg.success('successfully deleted.');
                        getList({page: current});
                    } else {
                        msg.help('failed delete');
                    }
                })
                .catch(error => {
                    msg.error('error');
                });
        };

        return (
            <div>

                {stu == 1 || stu == 2? (  <span className={styles.spanButton}>
                        <Button type={stu == 1? "secondary" :"primary"} size="small" onClick={stu == 1 ? popupStartConfirm : popupStopConfirm}>{butNmae}</Button>
                    </span>):''}

                <span className={styles.spanButton}>
                <Button type="secondary" size="small" onClick={jump}>群发送列表</Button>
              </span>

                <span className={styles.spanButton}>
                  <Button type="normal" size="small" onClick={del} warning>删除</Button>
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
                    width={100}
                    lock="left"
                    title="ID"
                    dataIndex="id"
                    align="center"
                />
                <Table.Column width={200} title="标题" dataIndex="title"/>
                <Table.Column width={100} title="群发数量" dataIndex="send_group_number"/>
                <Table.Column width={200} title="间隔" dataIndex="timer"/>
                <Table.Column width={200} title="备注" dataIndex="remark"/>
                <Table.Column width={200} title="创建日期" dataIndex="create_time"/>
                <Table.Column
                    width={230}
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
                total={dataTotal}
            />
        </div>
    );
}

