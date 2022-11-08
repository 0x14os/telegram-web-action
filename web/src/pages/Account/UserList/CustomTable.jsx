import React, {useState, useEffect} from 'react';
import {Table, Pagination, Dialog, Icon, Button} from '@alifd/next';
import styles from '../../../layouts/css/table.module.scss';
import {http} from '../../../tool/api/request';
import {msg} from '../../../tool/fun';

import useReactRouter from 'use-react-router';


export default function Home() {

    const [current, setCurrent] = useState(1);
    const [dataTotal, setTotal] = useState();

    const [dataSource, setData] = useState([]);
    const [dataPerPage, setPerPage] = useState(20);

    const route = useReactRouter();
    const history = route.history;

    const getList = (param) => {

        msg.loading("load list");
        http.account.groupUserList(param)
            .then(res => {
                msg.hide();
                if (res.code == 200) {
                    let items = res.data.items;
                    setData(items);
                    setTotal(res.data.total);
                } else {
                    msg.error(res.message);
                    console.error('login error');
                }
            })
            .catch(error => {
                msg.error(error);
                // alert('login error');
                console.log('error', error);
            });
    };

    useEffect(() => {
        if (route.match.params.id != '0') {
            getList({
                uagid: route.match.params.id,
                page: current
            });
        }
    }, []);


    const handlePagination = (current) => {
        setCurrent(current);
        getList({
            uagid: route.match.params.id,
            page: current
        });
    };

    /**
     *  发送一条群消息
     * */
    const renderOperatorPushMsg = (value, index, record) => {

        const pushMsgView = () => {
            // console.log(record);
            // console.log(value);
            // console.log(index);
            history.push('/account/push/msg/private/' + record.user_account_id + '/' + record.tg_username + '/' + record.tg_nicename + '/' + record.user_account_group_id);
        };

        return (
            <div>
                  <span className={styles.spanButton}>
                            <Button type="secondary" size="small" warning onClick={pushMsgView}>发送消息</Button>
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
                <Table.Column width={200} title="群标题" dataIndex="channel_title"/>
                <Table.Column width={120} title="昵称" dataIndex="tg_nicename"/>
                <Table.Column width={260} title="最后登录时间" dataIndex="tg_last_time"/>
                <Table.Column width={200} title="用户名" dataIndex="tg_username"/>
                <Table.Column width={200} title="手机" dataIndex="tg_phone"/>
                <Table.Column width={200} title="创建日期" dataIndex="create_time"/>

                <Table.Column
                    title="发送消息"
                    width={90}
                    cell={renderOperatorPushMsg}
                    lock="right"
                />

            </Table>

            <Pagination
                className={styles.pagination}
                current={current}
                onChange={handlePagination}
                total={dataTotal}
                pageSize={dataPerPage}
            />
        </div>
    );
}

