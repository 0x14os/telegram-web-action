import React, {useState, useEffect} from 'react';
import {Table, Button, Icon, Form, Select} from '@alifd/next';
import IceContainer from '@icedesign/container';
import styles from './index.module.scss';

import useReactRouter from 'use-react-router';

import {http} from '../../../tool/api/request';
import {msg, lo, isNull} from '../../../tool/fun';

const FormItem = Form.Item;

const los = lo();
const Option = Select.Option;


export default function GroupTable() {

    const [selectedRowKeys, setSelectedRowKeys] = useState([]);
    const [dataSource, setData] = useState([]);
    const [dataSelect, setDataSelect] = useState([]);
    const [isBut, setIsBut] = useState(false);
    const [dataTidSelect, setOnSelect] = useState("");
    const [isLoading] = useState(false);
    const [groupList, setGroupList] = useState([]);
    const [visibleDialog, setVisibleDialog] = useState(false);

    const route = useReactRouter();
    const history = route.history;


    useEffect(() => {
        if (route.match.params.id != '0') {
            setIsBut(true);
            getGroupList({user_account_id: route.match.params.id});
        } else if (route.match.params.id == '0') {
            getGroupList({user_account_id: '0'});
            soAcclist();
        }
    }, []);

    const soAcclist = () => {
        http.group.soAcclist({nul: 123})
            .then(res => {
                msg.hide();
                if (res.code == 200) {
                    console.log(res);
                    if (res.data.length > 0) {
                        let data = res.data;
                        let arr = [];
                        arr.push({label: "请选择TG账号查询", value: "0"});
                        for (let i = 0; i < data.length; i++) {
                            let v = data[i];
                            console.log(v);
                            arr.push({label: v.username, value: v.tid});
                        }
                        console.log(arr);
                        setDataSelect(arr);
                    }
                } else {
                    msg.error(res.message);
                }
            }).catch(error => {
            // alert('login error');
            console.log('error', error);
        });
    };


    const getGroupList = (param) => {
        msg.loading('locaing..');
        http.group.list(param)
            .then(res => {
                msg.hide();
                if (res.code == 200) {
                    if (res.data.length > 0) {
                        let data = res.data;
                        for (let i = 0; i < data.length; i++) {
                            let v = data[i];
                            if (v.status == 1) {
                                data[i].status_name = '开启';
                            } else {
                                data[i].status_name = '关闭';
                            }
                        }
                        setData(data);
                    }
                } else {
                    msg.error(res.message);
                    console.error('login error');
                }
            })
            .catch(error => {
                // alert('login error');
                console.log('error', error);
            });
    };


    // 表格可以勾选配置项
    const rowSelection = {
        // 表格发生勾选状态变化时触发
        onChange: (ids, records) => {
            console.log('ids', ids);
            console.log('records', records);
            setSelectedRowKeys(ids);
            setGroupList(records)
        },

        // 全选表格时触发的回调
        onSelectAll: (selected, records) => {
            console.log('onSelectAll', selected, records);
        },

        // 支持针对特殊行进行定制
        getProps: (record) => {
            return {
                disabled: record.id === 100306660941,
            };
        },

    };

    const clearSelectedKeys = () => {
        setSelectedRowKeys([]);
    };

    const deleteSelectedKeys = () => {
        console.log('delete keys', selectedRowKeys);
    };

    const deleteItem = (record) => {
        const {id} = record;
        console.log('delete item', id);
    };

    const renderOperator = (value, index, record) => {
        let uid = los.get('user_id');
        // 提取群成员
        const extract = () => {
            console.log(record);
            let param = {};
            param.uid = uid;
            param.tid = record.user_account_id;
            //群id
            param.tgid = record.guid;
            console.log("param:", param);
            msg.loading("loading");
            http.account.extract(param)
                .then(res => {
                    msg.hide();
                    if (res.code == 200) {
                        msg.notice("亲,大约需要1-2分钟提取群成员,请稍后.");
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

        return (
            <div>
                  <span className={styles.spanButton}>
                            <Button type="primary" size="small" onClick={extract}>提取成员</Button>
                  </span>
            </div>
        );
    };


    const pushAddTask = () => {
        if (selectedRowKeys.length >= 1) {

            // console.log(selectedRowKeys);
            // console.log(groupList);
            let tmpGroup = [];
            //user_account_id user_id
            if (!groupList[0]) {
                msg.error("请注意,浏览器异常");
                return;
            }

            let v = groupList[0];
            let losData = {
                user_account_id: v.user_account_id,
                user_id: v.user_id,
                user_account_group_list: "",
            };
            for (var i = 0; i < groupList.length; i++) {
                let val = groupList[i];
                if (val.guid) {
                    tmpGroup.push(val.guid);
                }
            }
            // console.log("tmpGroup", tmpGroup);

            let grouplos = tmpGroup.join(",");
            if (los.get("grouplos")) {
                los.del("grouplos");
            }
            losData.user_account_group_list = grouplos;
            const losrr = JSON.stringify(losData);
            los.add("grouplos", losrr);
            history.push('/account/group/task/add');
        } else {
            msg.error("请选择需要发送的群组.");
        }

    };


    const renderOperatorUser = (value, index, record) => {
        const jumpUser = () => {
            let routeParams = route.match.params;
            // console.log(routeParams);
            history.push('/account/group/user/' + record.guid + '/' + routeParams.id);
        };

        return (
            <div>
                  <span className={styles.spanButton}>
                            <Button type="normal" size="small" warning onClick={jumpUser}>查看</Button>
                  </span>
            </div>
        );

    };


    /**
     *  发送一条群消息
     * */
    const renderOperatorPushMsg = (value, index, record) => {
        // console.log(record);
        const pushMsgView = () => {
            history.push('/account/push/msg/group/' + record.user_account_id + '/' + record.channel_id + '/' + record.channel_title + '/123');
        };
        return (
            <div>
                  <span className={styles.spanButton}>
                            <Button type="secondary" size="small" warning onClick={pushMsgView}>发送消息</Button>
                  </span>
            </div>
        );
    };

    const onChangeSelect = (val, actionType, item) => {
        setOnSelect(val);
    };

    const selectClick = () => {
        if (isNull(dataTidSelect)) {
            setIsBut(false);
            msg.error("请选择正确的数据，进行查询");
        } else if (dataTidSelect != '0') {
            setIsBut(true);
            getGroupList({user_account_id: dataTidSelect})
        }
    };


    const viewSelect = () => {
        return (
            <div> 请选择TG账号
                <Select
                    style={{width: 200, marginLeft: 5}}
                    dataSource={dataSelect}
                    onChange={onChangeSelect}
                    // menuProps={{onScroll: onScroll}}
                    autoHighlightFirstItem={false}
                />
                <Button size="small" style={{margin: 10}} onClick={selectClick}>
                    查询群信息
                </Button>
            </div>
        );
    };

    const viewTask = () => {

        const addView = () => {
            return (
                <div>
                    <Button size="small" className={styles.batchBtn} onClick={pushAddTask}>
                        <Icon type="add"/>增加任务
                    </Button>
                    <Button
                        onClick={deleteSelectedKeys}
                        size="small"
                        className={styles.batchBtn}
                        disabled={!selectedRowKeys.length}
                    >
                        <Icon type="ashbin"/>删除
                    </Button>
                    <Button
                        onClick={clearSelectedKeys}
                        size="small"
                        className={styles.batchBtn}
                    >
                        <Icon type="close"/>清空选中
                    </Button>
                </div>
            );
        };
        return (
            addView()
        );
    };

    const back = () => {
        return (
            <div>
                <Button type="normal" size="small" onClick={() => {
                    history.push('/account/list');
                }}>返回</Button>
            </div>
        );
    };

    return (
        <div className={`${styles.selectableTable} selectable-table`}>
            <IceContainer className={styles.IceContainer}>
                {isBut == false ? viewSelect() : ""}
                {isBut == true ? viewTask() : ""}
                {isBut == true ? back() : ""}
            </IceContainer>

            <IceContainer>
                <Table
                    dataSource={dataSource}
                    loading={isLoading}
                    rowSelection={{
                        ...rowSelection,
                        selectedRowKeys,
                    }}
                >
                    <Table.Column title="ID" dataIndex="id" width={120}/>
                    <Table.Column title="群ID" dataIndex="channel_id" width={250}/>
                    <Table.Column title="群标题" dataIndex="channel_title" width={250}/>
                    <Table.Column title="群名称" dataIndex="channel_username" width={350}/>
                    <Table.Column title="创建时间" dataIndex="create_time" width={230}/>
                    <Table.Column title="更新时间" dataIndex="update_time" width={230}/>

                    <Table.Column
                        title="成员列表"
                        width={90}
                        cell={renderOperatorUser}
                        lock="right"
                    />
                    <Table.Column
                        title="发送消息"
                        width={90}
                        cell={renderOperatorPushMsg}
                        lock="right"
                    />
                    <Table.Column
                        title="操作"
                        cell={renderOperator}
                        lock="right"
                        width={120}
                    />
                </Table>
                <div className={styles.pagination}></div>
            </IceContainer>
        </div>
    );
}
