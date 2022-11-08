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
        param.id = route.match.params.id;

        http.private.logList(param)
            .then(res => {
                console.log(res);
                msg.hide();

                if (res.code == 200) {
                    let data = res.data.items;

                    if (data.length > 0) {

                        for (let i = 0; i < data.length; i++) {
                            let v = data[i];
                            if (v.status == 1) {
                                data[i].status_name = '待发送';
                            } else if (v.status == 2) {
                                data[i].status_name = '已发送';
                            } else {
                                data[i].status_name = '异常';
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
                <Table.Column width={200} title="关键词" dataIndex="soKey"/>
                <Table.Column width={200} title="TG用户名" dataIndex="tg_username"/>
                <Table.Column width={150} title="TGID" dataIndex="tg_user_id"/>
                <Table.Column width={250} title="TG哈希值" dataIndex="tg_access_hash"/>
                <Table.Column width={200} title="TG昵称" dataIndex="tg_nicename"/>
                <Table.Column width={200} title="TG手机号码" dataIndex="tg_phone"/>
                <Table.Column width={300} title="发送内容" dataIndex="text"/>
                <Table.Column width={200}  lock="right"
                              align="center" title="状态" dataIndex="status_name"/>
                <Table.Column width={200} title="创建日期" dataIndex="create_time"/>
                <Table.Column width={200} title="更新日期" dataIndex="update_time"/>
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

