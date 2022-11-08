import React, {useState, useEffect} from 'react';
import {Table, Pagination, Dialog, Icon, Button} from '@alifd/next';
import styles from '../../../layouts/css/table.module.scss';
import {http} from '../../../tool/api/request';
import {msg, lo} from '../../../tool/fun';

const los = lo();

import useReactRouter from 'use-react-router';


export default function Home() {

    const [current, setCurrent] = useState(1);
    const [dataTotal, setTotal] = useState(0);
    const [dataSource, setData] = useState([]);

    const route = useReactRouter();
    const history = route.history;
    const role = los.get("role");

    const getList = (param) => {

        msg.loading("load list");
        http.admin.list(param)
            .then(res => {
                msg.hide();
                if (res.code == 200) {
                    if (res.data.items.length > 0) {
                        let items = res.data.items;
                        for (let i = 0; i < items.length; i++) {
                            let v = items[i];
                            if (v.role_use == 1) {
                                items[i].role_use_name = '管理员';
                            } else {
                                items[i].role_use_name = '普通用户';
                            }
                            if (v.status == 1) {
                                items[i].status_name = '开启';
                            } else {
                                items[i].status_name = '关闭';
                            }
                        }
                        setData(items);
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
        getList({page: current});
    }, []);


    const handlePagination = (current) => {
        setCurrent(current);
        getList({page: current});
    };

    const renderOper = (value, index, record) => {

        const jumpPasswd = () => {
            history.push('/admin/edit/passwd/' + record.guid);
        };

        const jumpInfo = () => {
            history.push('/admin/edit/info/' + record.guid);
        };

        const del = () => {
            msg.loading('Normal deletion..');
            http.admin.del({guid: record.guid})
                .then(res => {
                    if (res.code == 200) {
                        msg.success('successfully deleted.');
                        getList({page: current});
                    } else {
                        msg.help('failed delete');
                    }
                })
                .catch(error => {
                    msg.help('failed delete');
                    msg.error('error');
                });
        };


        if (role == 1) {
            return (
                <div>
                    <span className={styles.spanButton}>
                      <Button type="secondary" size="small" onClick={jumpPasswd}>修改密码</Button>
                    </span>

                    <span className={styles.spanButton}>
                      <Button size="small" onClick={jumpInfo}>修改资料</Button>
                    </span>

                    <span className={styles.spanButton}>
                        <Button type="normal" size="small" onClick={del} warning>删除</Button>
                    </span>
                </div>
            );
        }

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
                <Table.Column width={200} title="账号" dataIndex="email"/>
                <Table.Column width={100} title="角色" dataIndex="role_use_name"/>
                <Table.Column width={200} title="最后登录IP" dataIndex="last_ip"/>
                <Table.Column width={80} title="登录次数" dataIndex="login_count"/>
                <Table.Column width={80} title="状态" dataIndex="status_name"/>
                <Table.Column width={200} title="创建日期" dataIndex="create_time"/>
                <Table.Column width={200} title="更新日期" dataIndex="update_time"/>
                {role == 1 ? (<Table.Column
                    width={260}
                    title="操作"
                    cell={renderOper}
                    lock="right"
                    align="center"
                />) : ''}

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

