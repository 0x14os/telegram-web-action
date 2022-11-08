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

export default function GroupedForm() {

    const route = useReactRouter();
    const history = route.history;

    const [urlParams, setUrlParams] = useState({
        "tid": '',
        "to": 0,
        "name": '',
        "type": "group",
        "tgid": '',
    });

    const [detail, setDetail] = useState({
        uid: '',
        tid: '',
        to: 0,
        msg: '',
    });

    useEffect(() => {
        if (isNull(route.match.params.tid) == false) {
            setUrlParams({
                "tid": route.match.params.tid,
                "to": route.match.params.to,
                "name": route.match.params.name,
                "type": route.match.params.type,
                "tgid": route.match.params.tgid,
            });
        }
    }, []);


    const formChange = (values, field) => {
        setDetail(values);
    };

    const submit = (values, errors) => {

        let user_id = los.get("user_id");

        values.uid = user_id;
        values.tid = urlParams.tid;
        values.to = urlParams.to;

        console.log('value', values);

        if (!errors) {
            postMsg(values);
        } else {
            msg.error(errors);
            console.error('submit', errors);
        }
    };


    const postMsg = (param) => {
        msg.loading("正在发送..");

        if (urlParams.type == "group") {
            http.account.pushGroupMsg(param)
                .then(res => {
                    msg.hide();
                    if (res.code == 200) {
                        history.push('/account/group/list/' + urlParams.tid);
                    } else {
                        msg.error("请求错误..");
                        console.error('error', error);
                    }
                })
                .catch(error => {
                    msg.error("请求错误..");
                    console.log('error', error);
                });
        } else if (urlParams.type == "private") {
            //privatePushMsg
            http.account.privatePushMsg(param)
                .then(res => {
                    msg.hide();
                    if (res.code == 200) {
                        console.log(res);
                        history.push('/account/group/user/' + urlParams.tgid);
                    } else {
                        msg.error("请求错误..");
                        console.error('error', error);
                    }
                })
                .catch(error => {
                    msg.error("请求错误..");
                    console.log('error', error);
                });
        }

    };



    const view = () => {

        console.log(urlParams);

        return (
            <div className="grouped-form">

                <IceContainer title={"发送消息 [至] " + urlParams.name} className={styles.container}>

                    <div className={styles.topFanhui}>
                        <Button type="normal" size="small" onClick={() => {
                            history.push('/account/group/list/' + urlParams.tid);
                        }}>返回</Button>
                    </div>

                    <Form onChange={formChange}>
                        <div>
                            <div className={styles.subForm}>
                                <div>


                                    <FormItem label="消息正文：" {...formItemLayout} required requiredMessage="请填写想要发送的消息">
                                        <Input.TextArea
                                            name="msg"
                                            placeholder="请填写想要发送的消息"
                                            aria-label="auto height"
                                            autoHeight={{minRows: 10, maxRows: 15}}
                                        />
                                    </FormItem>

                                </div>
                            </div>

                            <FormItem label=" " {...formItemLayout}>
                                <div>
                                    <Form.Submit type="primary" htmlType="submit" validate onClick={submit}>
                                        发送消息
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
