import React, {useState, useEffect, useCallback} from 'react';
import {Button, Dialog, Drawer, Input, Upload} from '@alifd/next';
import styles from '../../../layouts/css/table.module.scss';
import useReactRouter from 'use-react-router';
import {http} from "../../../tool/api/request";
import {msg, accessToken, isNull} from "../../../tool/fun";
import copy from 'copy-to-clipboard';

export default function TableFilter() {

    const [visible, setVisible] = useState(false);
    const [sovisible, setSoVisible] = useState(false);
    const [copied, setCopied] = useState(false);
    const [soval, setSoval] = useState("");
    const [soChangeVal, setSoChangeVal] = useState("");
    const routeResult = useReactRouter();
    const history = routeResult.history;

    useEffect(() => {
        setVisible(false);
        setSoVisible(false);
    }, []);

    const defaultValue = [];

    const handleHistoryPush = () => {
        history.push('/account/edit/0');
    };

    const load = (param) => {
        console.log("load", param);
        http.account.load(param)
            .then(res => {
                msg.hide();
                if (res.code == 200) {
                    // history.push('/account/list');
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

    const onOpen = () => {
        console.log(http.load);
        setVisible(true);
    };

    const onClose = (reason, e) => {
        setVisible(false);
    }

    const onSOOpen = () => {
        setSoVisible(true);
    };

    const onSOClose = (reason, e) => {
        setSoVisible(false);
    }

    const beforeUpload = (info) => {
        console.log("beforeUpload : ", info);
    };

    const onChange = (info) => {
        console.log("onChange : ", info);
    };

    const onError = (info) => {
        console.log("onError : ", info);
        if (info.response.success == false) {
            msg.error(info.response.message);
        }
    };

    const onSuccess = (info) => {
        // info.response.message
        // console.log("onSuccess : ", info.response.message);
        if (info.response.success) {
            msg.success(info.response.message);
        } else {
            msg.error(info.response.message);
        }
    };

    let opsheaders = {}
    opsheaders.Authorization = accessToken();


    const popupConfirm = () => {
        Dialog.confirm({
            title: '检测账号',
            content: '自动检测该账号下的所有TG账号,并且自动标注账号是否注销',
            onOk: () => {
                msg.loading('load deletion..');
                http.account.checkAccount({})
                    .then(res => {
                        msg.hide();
                        if (res.code == 200) {
                            msg.success('开始执行检测');
                        } else {
                            msg.error(res.msg);
                        }
                    }).catch(error => {
                    msg.error('error');
                });
            },
            onCancel: () => console.log('cancel')
        });
    };


    const onSoChange = (v) => {
        setSoChangeVal(v);
    }

    const onSoClick = (v) => {
        // console.log(soChangeVal);
        if (isNull(soChangeVal) === false) {
            msg.loading("正在请求数据..")
            http.account.so({keys: soChangeVal})
                .then(res => {
                    msg.hide();
                    if (res.code == 200) {
                        console.log(res.data);
                        let dat = res.data;
                        if (dat.length > 0) {
                            let uri = "";
                            for (let i = 0; i < dat.length; i++) {
                                uri += dat[i] + "\n\r";
                            }
                            setSoval(uri);
                        }
                    } else {
                        msg.error(res.msg);
                    }
                }).catch(error => {
                msg.error('error');
            });
        }
    }

    const handleCopy = () => {
        console.log(soval);
        if (isNull(soval) === false) {
            copy(soval);
            msg.success("复制成功");
        } else {
            msg.error("没有内容");
        }
    };


    return (
        <div className={styles.tableFilter}>
            <div className={styles.title}>TG账号</div>
            <div className={styles.filter}>

                <Button type="secondary" size="small" onClick={onSOOpen} className={styles.submitButton}>
                    搜索公开群
                </Button>

                <Button type="secondary" size="small" onClick={onOpen} className={styles.submitButton}>
                    导入协议号
                </Button>

                <Button type="primary" warning size="small" onClick={popupConfirm} className={styles.submitButton}>
                    检测账号
                </Button>

                <Button type="primary" size="small" onClick={handleHistoryPush} className={styles.submitButton}>
                    添加
                </Button>

            </div>

            <Drawer
                title="导入协议号"
                placement="right"
                visible={visible}
                onClose={onClose}
            >
                <Upload
                    action={http.load}
                    beforeUpload={beforeUpload}
                    onChange={onChange}
                    onError={onError}
                    onSuccess={onSuccess}
                    listType="text"
                    defaultValue={defaultValue}
                    headers={opsheaders}
                    multiple
                >
                    <Button type="secondary" size="small" style={{margin: "0 0 5px", padding: "0 70px"}}>
                        上传协议号
                    </Button>
                </Upload>
            </Drawer>

            <Drawer
                title="搜索群"
                placement="right"
                visible={sovisible}
                onClose={onSOClose}
                style={{width: "600px"}}
            >
                <div>

                    <Input
                        hasClear
                        // defaultValue="abc"
                        style={{width: "470px", height: "30px"}}
                        placeholder="请搜索需要的电报公开群"
                        onChange={onSoChange}
                    />
                    <Button style={{height: "32px"}} onClick={onSoClick}>查询</Button>
                </div>
                <div style={{margin: "10px 0 0 0"}}>
                    <Input.TextArea
                        name="soval"
                        // size="large"
                        // placeholder="搜索内容"
                        style={{width: "560px"}}
                        value={soval}
                        aria-label="TextArea"
                        autoHeight={{minRows: 20, maxRows: 20}}
                    />
                </div>
                <Button onClick={handleCopy} type="secondary" size="small" style={{margin: "10px 0 5px", padding: "0 70px",width: "560px"}}>
                    点击复制链接
                </Button>
            </Drawer>
        </div>
    );
}
