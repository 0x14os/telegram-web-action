/* eslint react/no-string-refs:0 */
import React, {Component} from 'react';
import {withRouter} from 'react-router-dom';
import {Input, Button, Form} from '@alifd/next';
import md5 from 'md5'


import {http} from '../../tool/api/request';
import {msg, lo, jump} from '../../tool/fun';

const los = lo();
const FormItem = Form.Item;
const formItemLayout = {
    labelCol: {
        span: 6
    },
    wrapperCol: {
        span: 14
    }
};


@withRouter
class UserLogin extends Component {
    static displayName = 'UserLogin';

    static propTypes = {};

    static defaultProps = {};

    constructor(props) {
        super(props);
        this.state = {
            value: {
                email: '',
                passwd: '',
                checkbox: false,
            },
        };
    }


    handleSubmit = (values) => {
        console.log(values);
        var pattern = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
        if (!pattern.test(values.email)) {
            msg.error("邮箱格式错误");
            return;
        }

        if (values.passwd.length < 6) {
            msg.error("密码长度必须大于6.");
            return;
        }

        let md5Passwd = md5(values.passwd);

        const params = {
            email: values.email,
            passwd: md5Passwd,
        };

        // console.log("params===", params);


        http.admin.login(params)
            .then(res => {
                console.log(res.data);
                if (res.code == 200) {
                    los.add('role', res.data.role);
                    los.add('token', res.data.token);
                    los.add('user_id', res.data.user_id);
                    los.add('tgStatus', res.data.tgStatus);
                    los.add('taskStatus', res.data.taskStatus);
                    msg.success('login success');
                    jump('/');
                } else {
                    msg.error(res.msg);
                }
            })
            .catch(error => {
                // alert('login error');
                console.log('error', error);
            });

    };


    render() {
        return (
            <div style={styles.container}>
                <h4 style={styles.title}>登 录</h4>

                <Form>
                    <div style={styles.formItems}>
                        <FormItem name="email" required message="必填" label="邮箱:" style={styles.formItem}>
                            <Input
                                name="email"
                                maxLength={80}
                                placeholder="邮箱"
                                style={styles.inputCol}
                            />
                        </FormItem>

                        <FormItem name="passwd" required message="必填" label="密码:" style={styles.formItem}>
                            <Input
                                name="passwd"
                                htmlType="password"
                                placeholder="密码"
                                style={styles.inputCol}
                            />
                        </FormItem>

                        <div style={styles.footer}>
                            <Form.Submit
                                type="primary"
                                htmlType="submit"
                                onClick={this.handleSubmit}
                                style={styles.submitBtn}
                            >
                                登 录
                            </Form.Submit>
                        </div>

                    </div>
                </Form>
            </div>
        );
    }
}

const styles = {
    container: {
        width: '400px',
        padding: '40px',
        background: '#fff',
        borderRadius: '6px',
    },
    title: {
        margin: '0 0 40px',
        color: 'rgba(0, 0, 0, 0.8)',
        fontSize: '28px',
        fontWeight: '500',
        textAlign: 'center',
    },
    formItem: {
        position: 'relative',
        marginBottom: '20px',
    },
    inputIcon: {
        position: 'absolute',
        left: '10px',
        top: '8px',
        color: '#666',
    },
    inputCol: {
        width: '100%',
        paddingLeft: '1px',
    },
    submitBtn: {
        width: '100%',
    },
    tips: {
        marginTop: '20px',
        display: 'block',
        textAlign: 'center',
    },
};

export default UserLogin;
