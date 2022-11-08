import React, {useState, useEffect} from 'react';
import IceContainer from '@icedesign/container';
import {Input, Form, Button, Radio} from '@alifd/next';
import styles from '../../../layouts/css/form.module.scss';
import {http} from '../../../tool/api/request';
import {msg, lo, isNull} from '../../../tool/fun';

import useReactRouter from 'use-react-router';

const FormItem = Form.Item;
const los = lo();
const RadioGroup = Radio.Group;

const formItemLayout = {
    labelCol: {xxs: 8, s: 3, l: 3},
    wrapperCol: {s: 12, l: 10},
};

export default function GroupedForm() {

    const route = useReactRouter();
    const history = route.history;

    const [guid, setGuid] = useState("0");
    const [mode, setMode] = useState("2");
    const [detail, setDetail] = useState({
        guid: '',
        phone: '',
        username: '',
        api_id: '',
        api_hash: '',
        api_name: '',
        api_certificate: '',
        user_id: '',
        mode: "2",
    });


    useEffect(() => {
        // console.log(isNull(route.match.params.id));
        // console.log(route.match.params.id);
        // console.log(typeof (route.match.params.id));
        // console.log(mode);

        if (isNull(route.match.params.id) == false) {
            getDetail({guid: route.match.params.id});
        }


        console.log(route.match.params.id);

    }, []);


    const formChange = (values, field) => {
        setDetail(values);
    };

    const submit = (values, errors) => {

        // console.log(values);
        // let user_id = los.get("user_id");
        // console.log(user_id);
        // values.user_id = user_id;
        // console.log('value', values);

        if (!errors) {
            values.mode = mode;
            if (isNull(route.match.params.id) == true) {
                values.guid = "0";
                console.log('value', values);
                pushAdd(values);
            } else {
                console.log('edit', values);
                values.guid = guid;
                pushEdit(values);
            }

        } else {
            msg.error(errors);
            console.error('submit', errors);
        }
    };

    const getDetail = (param) => {

        msg.loading('locaing..');

        http.account.detail(param)
            .then(res => {
                msg.hide();
                if (res.code == 200) {
                    var type = res.data.type;
                    console.log(res.data);
                    setGuid(res.data.guid);
                    let i = res.data;

                    let info = {
                        guid: i.guid,
                        phone: isNull(i.phone) ? "" : i.phone,
                        username: isNull(i.username) ? "" : i.username,
                        api_id: isNull(i.api_id) ? "" : i.api_id,
                        api_hash: isNull(i.api_hash) ? "" : i.api_hash,
                        api_name: isNull(i.api_name) ? "" : i.api_name,
                        api_certificate: isNull(i.api_certificate) ? "" : i.api_certificate,
                        mode: isNull(i.mode) ? "" : i.mode,
                    };
                    console.log(info.mode);
                    if (info.mode == 1){
                        setMode("1");
                    }else if(info.mode == 2){
                        setMode("2");
                    }
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
        http.account.edit(params)
            .then(res => {
                if (res.code == 200) {
                    history.push('/account/list');
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
        http.account.edit(param)
            .then(res => {
                if (res.code == 200) {
                    history.push('/account/list');
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

    const formRadioChange = (values, field) => {
        console.log("formRadioChange", values);
        setMode(values);
    };


    const view = () => {

        return (
            <div className="grouped-form">

                <IceContainer title="设置用户" className={styles.container}>

                    <div className={styles.topFanhui}>
                        <Button type="normal" size="small" onClick={() => {
                            history.push('/account/list');
                        }}>返回</Button>
                    </div>

                    <Form onChange={formChange}>
                        <div>
                            <div className={styles.subForm}>
                                <h3 className={styles.formTitle}>账户编辑</h3>
                                <div>

                                    {/*// onChange={formRadioChange} aria-labelledby="groupId" */}
                                    <FormItem label="账号类型：" {...formItemLayout} required>
                                        <RadioGroup  onChange={formRadioChange} value={mode}>
                                            <Radio value="1">群发</Radio>
                                            <Radio value="2">1v1</Radio>
                                        </RadioGroup>
                                    </FormItem>

                                    <FormItem label="手机号码：" {...formItemLayout} required requiredMessage="请填写手机号码">
                                        <Input name="phone" placeholder="请输入手机号码:8613686861212" value={detail.phone}/>
                                    </FormItem>

                                    <FormItem label="用户名：" {...formItemLayout} required requiredMessage="请填写用户名">
                                        <Input name="username" placeholder="请输入用户名" value={detail.username}/>
                                    </FormItem>

                                    <FormItem label="APP 名称：" {...formItemLayout} required requiredMessage="请填写app名称">
                                        <Input name="api_name" placeholder="请输入App Title" value={detail.api_name}/>
                                    </FormItem>

                                    <FormItem label="App Api Id：" {...formItemLayout} required
                                              requiredMessage="请填写api-id">
                                        <Input name="api_id" placeholder="请输入api_id" value={detail.api_id}/>
                                    </FormItem>

                                    <FormItem label="App Api Hash：" {...formItemLayout} required
                                              requiredMessage="请填写api-hash">
                                        <Input name="api_hash" placeholder="请输入api_hash" value={detail.api_hash}/>
                                    </FormItem>

                                    <FormItem label="APP API公钥：" {...formItemLayout} required
                                              requiredMessage="请填写API公钥">
                                        <Input.TextArea
                                            name="api_certificate"
                                            placeholder="请输入API公钥"
                                            value={detail.api_certificate}
                                            aria-label="auto height"
                                            autoHeight={{minRows: 10, maxRows: 15}}
                                        />
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
