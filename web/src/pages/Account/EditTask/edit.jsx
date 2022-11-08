import React, {useState, useEffect} from 'react';
import IceContainer from '@icedesign/container';
import {Input, Form, Button, Radio, DatePicker} from '@alifd/next';
import moment from 'moment';
import styles from '../../../layouts/css/form.module.scss';
import {http} from '../../../tool/api/request';
import {msg, lo, isNull} from '../../../tool/fun';

const los = lo();

import useReactRouter from 'use-react-router';

const FormItem = Form.Item;

const formItemLayout = {
    labelCol: {xxs: 8, s: 3, l: 3},
    wrapperCol: {s: 12, l: 10},
};

const RadioGroup = Radio.Group;

const methodList = [
    {
        value: 'interval',
        label: '间隔'
    },
    {
        value: 'date',
        label: '一次'
    },
];

export default function GroupedForm() {

    const route = useReactRouter();
    const history = route.history;


    const [pushData, setPushData] = useState({
        title: '',
        msg: '',
        timer: '',
        remark: '',
    });


    const [radioVal, setRadioVal] = useState('interval');

    const [pickerVal, setPickerVal] = useState('');


    const getLosData = () => {
        let grolos = los.get("grouplos");
        return JSON.parse(grolos);
    };

    const formChange = (values, field) => {
        setPushData(values);
    };

    const submit = (values, errors) => {
        if (!errors) {
            const push = getLosData();
            if (!values.remark) {
                values.remark = "无";
            }
            const pudata = Object.assign(push, values);
            pudata.guid = 0;
            pudata.method = "interval";
            //radioVal;

            if (pudata.method == "date") {
                pudata.timer = pickerVal;
            }


            console.log(pudata);
            pushAdd(pudata);
        } else {
            msg.error(errors);
            console.error('submit', errors);
        }
    };

    const pushAdd = (param) => {

        http.task.pushEdit(param)
            .then(res => {
                console.log("param====", param);
                if (res.code == 200) {
                    los.del("grouplos");
                    history.push('/task/list/');
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

    const onRadioGroupChange = (values) => {
        setRadioVal(values);
    };


    const onPickerChange = (value) => {
        console.log("onPickerChange", value);
    };

    const onPickerOk = (value) => {
        let time = value.format('YYYY-MM-DD HH:mm:ss');
        setPickerVal(time);
    };

    return (
        <div className="grouped-form">

            <IceContainer title="设置定时任务" className={styles.container}>

                <div className={styles.topFanhui}>
                    <Button type="normal" size="small" onClick={() => {
                        history.push('/account/list');
                    }}>返回</Button>
                </div>

                <Form onChange={formChange}>
                    <div>
                        <div className={styles.subForm}>
                            <h3 className={styles.formTitle}>任务编辑</h3>
                            <div>

                                <FormItem label="标题" {...formItemLayout} required requiredMessage="请填写标题">
                                    <Input name="title" placeholder="请输入标题"/>
                                </FormItem>


                                {/*<FormItem label="定时模式" {...formItemLayout} required requiredMessage="请填写时间">*/}
                                {/*    <RadioGroup dataSource={methodList} value={radioVal} onChange={onRadioGroupChange}/>*/}
                                {/*</FormItem>*/}

                                <FormItem label="间隔" {...formItemLayout} required requiredMessage="请填写时间">
                                    {/*{*/}
                                    {/*    radioVal == 'interval'*/}
                                    {/*        ? <Input name="timer" required placeholder="请输入时间 如:17:30"/>*/}
                                    {/*        : <DatePicker showTime onChange={onPickerChange} onOk={onPickerOk}/>*/}
                                    {/*}*/}
                                    <Input name="timer" required placeholder="请输入整数,如:60"/>
                                    <p>ps:间隔时间为秒,如60秒等于1分钟</p>
                                </FormItem>

                                <FormItem label="发送正文" {...formItemLayout} required requiredMessage="请填写发送内容">
                                    <Input.TextArea name="msg" placeholder="请填写发送内容" maxLength={1500}
                                                    rows={12}
                                                    hasLimitHint/>
                                </FormItem>

                                <FormItem label="备注" {...formItemLayout} requiredMessage="请填写备注">
                                    <Input name="remark" placeholder="请输入备注"/>
                                </FormItem>


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

}
