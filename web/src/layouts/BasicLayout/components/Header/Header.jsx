import React, {useState, useEffect} from 'react';
import {Notification, Button} from '@alifd/next';
import {Link} from 'react-router-dom';
import Logo from '../Logo';
import './Header.scss';
import {logout, lo, msg, jump, isNull} from '../../../../tool/fun';

import {http} from '../../../../tool/api/request';
import useReactRouter from 'use-react-router';

const los = lo();

export default function Header() {

    const [number, setNumber] = useState(0);

    const routeResult = useReactRouter();
    const history = routeResult.history;

    const clickOut = () => {
        msg.loading("正在退出..");
        http.admin.out({})
            .then(res => {
                msg.hide();
                if (res.code == 200) {
                    if (logout()) {
                        jump('/');
                    }
                } else {
                    msg.error(res.message);
                    // console.error('login error');
                }
            }).catch(error => {
            msg.error("退出错误。。");
            // alert('login error');
            console.log('error', error);
        });
    };

    const openNotification = (dat) => {
        console.log(dat.content);
        let jdat = JSON.parse(dat.content);
        Notification.open({
            title: dat.title,
            content: jdat.text,
            onClick: () => {
                // console.log("Notification Clicked!");
                history.push(jdat.uri);
            }
        });
    };

    const handleJumpNotice = () => {
        history.push('/notice');
    };


    const getCount = () => {
        http.msg.count({})
            .then(res => {
                if (res.code == 200) {
                    let data = res.data
                    console.log(data);
                    los.add("noticeNum", data.count);
                    setNumber(data.count);
                    if (data.count > 0) {
                        let dat = data.dat;
                        let noticeDat = los.get("notice");
                        //is not eq
                        if (isNull(noticeDat)) {
                            los.add("notice", dat.guid);
                            openNotification(dat);
                        } else if (noticeDat !== dat.guid) {
                            los.add("notice", dat.guid);
                            openNotification(dat);
                        }
                    }
                } else {
                    // msg(res.message);
                    console.error('login error');
                }
            }).catch(error => {
            // alert('login error');
            console.log('error', error);
        });
    };


    ///notice
    const not = () => {
        getCount();
        setInterval(function () {
            let token = los.get("token")
            if (token) {
                getCount();
            }
        }, 90000);
    };


    let userId = los.get('user_id');


    const view = () => {
        not();
        return (
            <div className="header-container">
                <div className="header-content">
                    <Logo isDark/>

                    <div className="header-navbar">

                        <div className="user-profile">
                            <a className="user-name" onClick={handleJumpNotice}
                               style={{fontSize: '13px', marginRight: '5px'}}>
                                消息通知<span style={{color: '#FF0000'}}>({number})</span>
                            </a>
                        </div>

                        <div className="user-profile">
                            <Link to={{pathname: "/admin/edit/passwd/" + userId}}>
                                <span className="user-name"
                                      style={{fontSize: '13px', marginRight: '5px'}}>
                                  修改密码
                                </span>
                            </Link>
                        </div>

                        <div className="user-profile">
                            <span className="user-name" onClick={clickOut} style={{fontSize: '13px'}}>
                              退出
                            </span>
                        </div>

                    </div>
                </div>
            </div>
        );
    };
    return (view());
}
