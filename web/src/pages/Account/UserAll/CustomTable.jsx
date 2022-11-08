import React, {useState, useEffect} from 'react';
import {Table, Button, Icon, Select, Form, Input, Pagination} from '@alifd/next';
import IceContainer from '@icedesign/container';

import styles from './index.module.scss';
import {http} from '../../../tool/api/request';
import {msg, lo} from '../../../tool/fun';

import useReactRouter from 'use-react-router';

import XLSX from 'xlsx';

const los = lo();

export default function Home() {

    //批量索引值
    const [selectedRowKeys, setSelectedRowKeys] = useState([]);
    const [isLoading] = useState(false);

    //当前分页列数
    const [current, setCurrent] = useState(1);
    //列表总数据条
    const [dataTotal, setTotal] = useState(0);
    //列表数据
    const [dataSource, setData] = useState([]);
    const [dataKeyData, setKeyData] = useState([]);
    //设置群名称
    const [groupName, setGroupName] = useState('');
    //批量导入的用户
    const [xlsList, setXlsList] = useState([]);
    //请求搜索列表
    const [dataSourceAcc, setDataAcc] = useState([]);
    //搜索 选择哪个账号来新建群
    const [searchVal, setSearchVal] = useState({tid: "", name: ""});

    const route = useReactRouter();
    const history = route.history;

    const importf = (obj) => {
        // console.log(obj);

        let wb;//读取完成的数据
        let rABS = false; //是否将文件读取为二进制字符串
        if (!obj.target.files) {
            return;
        }

        let f = obj.target.files[0];
        let reader = new FileReader();
        reader.onload = function (e) {
            let data = e.target.result;
            if (rABS) {
                wb = XLSX.read(btoa(this.fixdata(data)), {//手动转化
                    type: 'base64'
                });
            } else {
                wb = XLSX.read(data, {
                    type: 'binary'
                });
            }

            let sheetInner = XLSX.utils.sheet_to_json(wb.Sheets[wb.SheetNames[0]]);
            let reqList = [];
            console.log(sheetInner);
            for (let i in sheetInner) {
                reqList.push(sheetInner[i]['username']);
            }
            console.log("reqList===", reqList);
            console.log("upload groupName", groupName);

            if (reqList.length === sheetInner.length && reqList.length !== 0) {
                setXlsList(reqList)
            }
        };

        if (rABS) {
            reader.readAsArrayBuffer(f);
        } else {
            reader.readAsBinaryString(f);
        }
        obj.target.value = '';
    };
    const fixdata = (data) => { //文件流转BinaryString
        var o = "",
            l = 0,
            w = 10240;
        for (; l < data.byteLength / w; ++l) o += String.fromCharCode.apply(null, new Uint8Array(data.slice(l * w, l * w + w)));
        o += String.fromCharCode.apply(null, new Uint8Array(data.slice(l * w)));
        return o;
    };

    const getList = (param) => {

        msg.loading("load list");

        http.account.groupUserAll(param)
            .then(res => {
                msg.hide();
                if (res.code == 200) {
                    let items = res.data.items;
                    if (JSON.stringify(items) !== '{}') {
                        setData(items);
                        setTotal(res.data.total);
                    } else {
                        console.error("没有数据而已，不用紧张...");
                    }
                }
            })
            .catch(error => {
                msg.error(error);
                // alert('login error');
                console.log('error', error);
            });

    };

    const getUseriD = () => {
        return los.get('user_id');
    };

    useEffect(() => {
        let uid = getUseriD();

        if (uid) {
            getList({
                uid: uid,
                page: current
            });
        }
    }, []);

    // 表格可以勾选配置项
    const rowSelection = {
        // 表格发生勾选状态变化时触发
        onChange: (ids, records) => {
            console.log('ids', ids);
            console.log('records', records);
            setSelectedRowKeys(ids);
            setKeyData(records)
        },

        // 全选表格时触发的回调
        onSelectAll: (selected, records) => {
            console.log("取消事件");
            console.log('onSelectAll', selected, records);
            if (selected == false) {
                setXlsList([]);
            }
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
        return window.location.reload();
    };

    const deleteSelectedKeys = () => {
        console.log('delete keys', selectedRowKeys);
    };

    const handlePagination = (current) => {
        setCurrent(current);
        getList({
            uid: getUseriD(),
            page: current
        });
    };

    const pushNewGroup = () => {
        // console.log("1312234234");
        // console.log(dataKeyData);
        // console.log("groupName size", groupName.length);
        if (groupName.length == 0 && groupName.length == "") {
            msg.error("群名称不能为空.");
            return;
        }

        for (let i = 0; i < dataKeyData.length; i++) {
            let val = dataKeyData[i];
            if (val.tg_username) {
                xlsList.push(val.tg_username);
            }
        }

        if (searchVal.tid == "") {
            msg.error("请选择一个TG账号来创建群.");
            return;
        }

        if (xlsList.length == 0) {
            msg.error("新建群，必须添加群成员");
            return;
        }

        let newGroup = {};
        newGroup.name = groupName;
        newGroup.tid = searchVal.tid;
        newGroup.uid = getUseriD();
        // newGroup.uname = searchVal.name;
        newGroup.users = xlsList.join(",");
        console.log("xls size", newGroup);
        msg.loading("正在创建新群");

        http.account.newGroup(newGroup)
            .then(res => {
                msg.hide();
                if (res.code == 200) {
                    setGroupName('');
                    setSearchVal([]);
                    setXlsList([]);
                    setDataAcc([]);
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


    //新群名
    const newGroupName = (v, e) => {
        console.log(v);
        setGroupName(v);
    };

    const handleSearch = (value) => {
        console.log(value);

        let param = {};

        param.username = value;
        param.uid = getUseriD();
        console.log(param);
        msg.loading("正在查找..");

        http.account.searchUsername(param)
            .then(res => {
                msg.hide();
                let list = res.data;
                if (list.length > 0) {
                    let n = 1;
                    let acc = [];
                    for (let i = 0; i < list.length; i++) {
                        let tmp = {};
                        tmp.value = list[i].username;
                        tmp.tid = list[i].tid;
                        acc.push(tmp);
                    }
                    setDataAcc(acc);
                    console.log("accc", acc);
                } else {
                    setDataAcc([])
                }
                console.log(res);

            }).catch(error => {
            msg.error(error);
            // alert('login error');
            console.log('error', error);
        });
    };


    const onChangeSelect = (val, actionType, itmes) => {
        // console.log(val);
        // console.log(actionType);
        // console.log(itmes);
        let tmp = {};
        tmp.tid = itmes.tid;
        tmp.name = itmes.value;
        setSearchVal(tmp);
    };

    return (

        <div className={`${styles.selectableTable} selectable-table`}>

            <IceContainer className={styles.IceContainer}>
                <div>
                    新建群名称：<Input size="small" name="groupName" onChange={newGroupName} className={styles.GroupName}/>

                    <Button size="small" className={styles.batchBtn} onClick={pushNewGroup}>
                        <Icon type="add"/>创建新群
                    </Button>

                    <Button
                        onClick={clearSelectedKeys}
                        size="small"
                        className={styles.batchBtn}
                    >
                        <Icon type="close"/>清光
                    </Button>

                    <Select showSearch
                            placeholder="搜个TG账号"
                            filterLocal={false}
                            dataSource={dataSourceAcc}
                            onSearch={handleSearch}
                            style={{width: 300}}
                            onChange={onChangeSelect}
                    />

                    {/*<span>PS:目前仅支持：有用户名称的用户进行建群拉人.</span>*/}
                </div>

                <div>
                    xls导入：<input type='file' accept='.xlsx, .xls' onChange={importf}/>
                </div>

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
                    <Table.Column
                        width={100}
                        lock="left"
                        title="ID"
                        dataIndex="id"
                        align="center"
                    />
                    <Table.Column width={200} title="群标题" dataIndex="channel_title"/>
                    <Table.Column width={100} title="昵称" dataIndex="tg_nicename"/>
                    <Table.Column width={200} title="用户名" dataIndex="tg_username"/>
                    <Table.Column width={200} title="手机" dataIndex="tg_phone"/>
                    <Table.Column width={260} title="最后登录时间" dataIndex="tg_last_time"/>
                    <Table.Column width={200} title="创建日期" dataIndex="create_time"/>
                </Table>

                <div className={styles.pagination}>
                    <Pagination
                        current={current}
                        onChange={handlePagination}
                        total={dataTotal}
                        pageSize={30}
                    />
                </div>
            </IceContainer>

            <div>

            </div>
        </div>
    );
}

