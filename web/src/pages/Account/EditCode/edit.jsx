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

    const [guid, setGuid] = useState('0');
    const [detail, setDetail] = useState({
        guid: '',
        code: '',
    });


    useEffect(() => {
        if (isNull(route.match.params.id) == false) {
            getDetail({guid: route.match.params.id});
        }
    }, []);


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

    const formChange = (values, field) => {
        setDetail(values);
    };

    const submit = (values, errors) => {
        let user_id = los.get("user_id");

        values.uid = user_id;
        console.log('value', values);

        if (!errors) {
            if (isNull(guid) == false) {
                values.guid = guid;
                console.log('value', values);
                activation(values);
            }
        } else {
            msg.error(errors);
            console.error('submit', errors);
        }
    };

    const activation = (param) => {
        msg.loading("激活中..");
        // param.code = new Number(param.code);
        // console.log("=======code:",typeof param.code);
        http.account.activation(param)
            .then(res => {
                msg.hide();
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

    const view = () => {

        return (
            <div className="grouped-form">

                <IceContainer title="授权TG账号" className={styles.container}>

                    <div className={styles.topFanhui}>
                        <Button type="normal" size="small" onClick={() => {
                            history.push('/account/list');
                        }}>返回</Button>
                    </div>

                    <Form onChange={formChange}>
                        <div>
                            <div className={styles.subForm}>
                                <div>

                                    <FormItem label="Code：" {...formItemLayout} required requiredMessage="请填写Code">
                                        <Input name="code" placeholder="请输入Code" htmlType="number" trim={true}/>
                                    </FormItem>

                                </div>
                            </div>

                            <FormItem label=" " {...formItemLayout}>
                                <div>
                                    <Form.Submit type="primary" htmlType="submit" validate onClick={submit}>
                                        激活
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
