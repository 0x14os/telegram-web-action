import React, {useState, useEffect} from 'react';
import IceContainer from '@icedesign/container';
import {Input, Form, Button} from '@alifd/next';
import styles from '../../../layouts/css/form.module.scss';
import {http} from '../../../tool/api/request';
import {msg, lo, isNull} from '../../../tool/fun';

import useReactRouter from 'use-react-router';

const FormItem = Form.Item;
const los = lo();
const formItemLayout = {
    labelCol: {xxs: 8, s: 3, l: 3},
    wrapperCol: {s: 12, l: 10},
};
const formItemLayoutP10 = {
    labelCol: {xxs: 8, s: 3, l: 3},
    wrapperCol: {s: 5, l: 5},
};

export default function GroupedForm() {

    const route = useReactRouter();
    const history = route.history;

    const [guid, setGuid] = useState('0');
    const [detail, setDetail] = useState({
        guid: "",
        title: "",
        soKey: "",
        sendNumber: 0,
        sendAccountNumber: 0,
        accountNumber: 0,
        timer: 0,
        remark: "",
    });

    useEffect(() => {
        // console.log(isNull(route.match.params.id));
        // console.log(route.match.params.id);
        // console.log(typeof (route.match.params.id));

        if (isNull(route.match.params.id) == false) {
            getDetail({guid: route.match.params.id});
            setGuid(route.match.params.id);
        } else {
            setGuid("0");
        }
    }, []);


    const formChange = (values, field) => {
        setDetail(values);
    };

    const submit = (values, errors) => {
        // let user_id = los.get("user_id");
        if (!errors) {
            if (isNull(guid)) {
                values.guid = "0"
                console.log('addValues', values);
                pushAdd(values);
            } else {
                // console.log('editVal', values);
                values.guid = guid;
                if (isNull(values.remark)) {
                    values.remark = ""
                }
                // console.log(values);
                pushEdit(values);
            }
        } else {
            msg.error(errors);
            console.error('submit', errors);
        }
    };

    const getDetail = (param) => {

        msg.loading('locaing..');

        http.private.one(param)
            .then(res => {
                msg.hide();
                if (res.code == 200) {
                    console.log(res.data);
                    setGuid(res.data.guid);
                    let i = res.data;
                    let info = {
                        guid: i.guid,
                        title: isNull(i.title) ? "" : i.title,
                        soKey: isNull(i.soKey) ? "" : i.soKey,
                        sendNumber: isNull(i.sendNumber) ? "" : i.sendNumber,
                        sendAccountNumber: isNull(i.sendAccountNumber) ? "" : i.sendAccountNumber,
                        accountNumber: isNull(i.accountNumber) ? "" : i.accountNumber,
                        timer: isNull(i.timer) ? "" : i.timer,
                        text: isNull(i.text) ? "" : i.text,
                    };
                    setDetail(info);
                } else {
                    msg.error(res.msg);
                    console.error('login error');
                }
            })
            .catch(error => {
                msg.error(error);
                console.log('error', error);
            });
    };


    const pushEdit = (params) => {
        http.private.edit(params)
            .then(res => {
                if (res.code == 200) {
                    history.push('/private/list');
                } else {
                    msg.error("请求错误..");
                    console.error('error edit', error);
                }
            })
            .catch(error => {
                msg.error("请求错误..");
                console.log('error edit', error);
            });
    };

    const pushAdd = (param) => {
        http.private.add(param)
            .then(res => {
                if (res.code == 200) {
                    history.push('/private/list');
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

    const view = () => {
        return (
            <div className="grouped-form">
                <IceContainer className={styles.container}>
                    <div className={styles.topFanhui}>
                        <Button type="normal" size="small" onClick={() => {
                            history.push('/private/list');
                        }}>返回</Button>
                    </div>
                    <Form onChange={formChange}>
                        <div>
                            <div className={styles.subForm}>
                                <h3 className={styles.formTitle}>编辑</h3>
                                <div>
                                    <FormItem label="任务标题：" {...formItemLayout} required requiredMessage="请填写任务标题">
                                        <Input name="title" placeholder="请输任务标题" value={detail.title}/>
                                    </FormItem>


                                    <FormItem label="搜素关键词：" {...formItemLayout} required requiredMessage="请填写关键词">
                                        <Input name="soKey" placeholder="请输入查询关联群的关键词" value={detail.soKey}/>
                                    </FormItem>


                                    <FormItem label="发送数量：" {...formItemLayoutP10} required requiredMessage="请填写条数">
                                        <Input name="sendAccountNumber" placeholder="请输入每个账号发送的条数 如：10"
                                               value={detail.sendAccountNumber}/>
                                    </FormItem>


                                    <FormItem label="任务账号数量：" {...formItemLayoutP10} required
                                              requiredMessage="请填写该任务启用发送的账号数量">
                                        <Input name="accountNumber" placeholder="请输入账号数量，如:3"
                                               value={detail.accountNumber}/>
                                    </FormItem>

                                    <FormItem label="休眠时间：" {...formItemLayoutP10} required
                                              requiredMessage="请填写休眠时间">
                                        <Input name="timer" placeholder="请输入休眠时间的秒数" value={detail.timer}/>
                                    </FormItem>

                                    <FormItem label="发送文本：" {...formItemLayout} required requiredMessage="请填写发送的内容">
                                        <Input.TextArea
                                            name="text"
                                            placeholder="请输入发送的内容"
                                            value={detail.text}
                                            aria-label="auto height"
                                            autoHeight={{minRows: 10, maxRows: 15}}
                                        />
                                    </FormItem>

                                    <FormItem label="备注：" {...formItemLayout} >
                                        <Input name="remark" placeholder="如需要填写备注.." value={detail.remark}/>
                                    </FormItem>

                                </div>
                            </div>

                            <FormItem label=" " {...formItemLayout}>
                                <div>
                                    <Form.Submit type="primary" htmlType="submit" validate onClick={submit}>
                                        保存
                                    </Form.Submit>

                                </div>
                            </FormItem>
                        </div>
                    </Form>
                </IceContainer>
            </div>
        );
    };

    return (view());

}
