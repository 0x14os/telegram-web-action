import React, {useState, useEffect} from 'react';
import IceContainer from '@icedesign/container';
import {Input, Form, Button} from '@alifd/next';
import styles from '../../../layouts/css/form.module.scss';
import {http} from '../../../tool/api/request';
import {msg} from '../../../tool/fun';

import useReactRouter from 'use-react-router';
import md5 from "md5"

const FormItem = Form.Item;


const formItemLayout = {
    labelCol: {xxs: 8, s: 3, l: 3},
    wrapperCol: {s: 12, l: 10},
};

export default function GroupedForm() {

    const route = useReactRouter();
    const history = route.history;

    const [guid, setGuid] = useState('0');
    const [type, setType] = useState('passwd');
    const [detail, setDetail] = useState({
        guid: '',
        passwd: '',
        taskNumber: 0,
        tgNumber: 0,
        tgGroupNumber: 0,
    });

    useEffect(() => {
        if (route.match.params.id != '0') {
            getDetail({guid: route.match.params.id});
        }
        setType(route.match.params.type)
    }, []);


    const formChange = (values, field) => {
        setDetail(values);
    };

    const submit = (values, errors) => {
        // console.log('error', errors, 'value', values);
        console.log('pirnt', errors);
        values.type = type;
        if (!errors) {
            values.passwd = md5(values.passwd);
            if (guid === '0') {
                console.log('value', values);
                values.guid = 0;
                pushAdd(values);
            } else {
                console.log('edit', values);
                values.guid = guid;
                pushEditPasswd(values);
            }

        } else {
            msg.error(errors);
            console.error('submit', errors);
        }
    };

    const getDetail = (param) => {

        msg.loading('locaing..');

        http.admin.detail(param)
            .then(res => {
                msg.hide();
                if (res.code == 200) {
                    setGuid(res.data.guid);
                    setDetail(res.data);
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

    const pushEditPasswd = (params) => {

        http.admin.editPasswd(params)
            .then(res => {
                if (res.code == 200) {
                    history.push('/admin/list');
                } else {
                    msg.error(error);
                    console.error('error edit', error);
                }
            })
            .catch(error => {
                msg.error(error);
                console.log('error edit', error);
            });
    };

    const pushAdd = (param) => {
        http.admin.edit(param)
            .then(res => {
                if (res.code == 200) {
                    history.push('/admin/list');
                } else {
                    msg.error(error);
                    console.error('error', error);
                }
            })
            .catch(error => {
                msg.error(error);
                console.log('error', error);
            });
    };


    const byTypeView = () => {

        if (type == 'add') {
            return (
                <div>
                    <FormItem label="邮箱：" {...formItemLayout} required requiredMessage="请填写邮箱">
                        <Input name="email" placeholder="请输入管理员邮箱" value={detail.email}/>
                    </FormItem>

                    <FormItem label="密码：" {...formItemLayout} required requiredMessage="请填写密码">
                        <Input name="passwd" placeholder="请输入输密码" htmlType="password"
                               value={detail.passwd}/>
                    </FormItem>

                    <FormItem label="可绑定TG账号数量：" {...formItemLayout} required requiredMessage="请填写数量">
                        <Input name="tgNumber" size="small" placeholder="请输入该账户下可以绑定多少TG账号" value={detail.tgNumber}
                               htmlType="number"/>
                    </FormItem>

                    <FormItem label="可绑定群发数量：" {...formItemLayout} required requiredMessage="请填写数量">
                        <Input name="tgGroupNumber" placeholder="请输入该账户下可以群发多少个群" value={detail.tgGroupNumber}
                               htmlType="number"/>
                    </FormItem>

                    <FormItem label="可创建任务数量：" {...formItemLayout} required requiredMessage="请填写数量">
                        <Input name="taskNumber" placeholder="请输入该账户下，可以创建多少个任务" value={detail.taskNumber}
                               htmlType="number"/>
                    </FormItem>
                </div>
            );
        } else if (type == "info") {
            return (
                <div>
                    <FormItem label="可绑定TG账号数量：" {...formItemLayout} required requiredMessage="请填写数量">
                        <Input name="tgNumber" placeholder="请输入该账户下可以绑定多少TG账号" value={detail.tgNumber}
                               htmlType="number"/>
                    </FormItem>

                    <FormItem label="可绑定群发数量：" {...formItemLayout} required requiredMessage="请填写数量">
                        <Input name="tgGroupNumber" size="small" placeholder="请输入该账户下可以群发多少个群"
                               value={detail.tgGroupNumber}
                               htmlType="number"/>
                    </FormItem>

                    <FormItem label="可创建任务数量：" {...formItemLayout} required requiredMessage="请填写数量">
                        <Input name="taskNumber" placeholder="请输入该账户下，可以创建多少个任务" value={detail.taskNumber}
                               htmlType="number"/>
                    </FormItem>
                </div>
            );
        } else if (type == 'passwd') {
            return (
                <div>
                    <FormItem label="密码：" {...formItemLayout} required requiredMessage="请填写密码">
                        <Input name="passwd" placeholder="请输入输密码" htmlType="password"
                               value={detail.passwd}/>
                    </FormItem>
                </div>
            );
        }

    };

    const view = () => {

        return (
            <div className="grouped-form">

                <IceContainer title="设置管理员" className={styles.container}>

                    <div className={styles.topFanhui}>
                        <Button type="normal" size="small" onClick={() => {
                            history.push('/admin/list');
                        }}>返回</Button>
                    </div>

                    <Form onChange={formChange}>
                        <div>
                            <div className={styles.subForm}>
                                <h3 className={styles.formTitle}>账户编辑</h3>
                                <div>

                                    {byTypeView()}

                                </div>
                            </div>

                            <FormItem label=" " {...formItemLayout}>
                                <div>
                                    <Form.Submit type="primary" validate onClick={submit}>
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
