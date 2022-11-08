import React, {useState, useEffect} from 'react';
import {Table, Pagination, Collapse, Icon, Button, Dialog} from '@alifd/next';
import styles from '../../../layouts/css/table.module.scss';
import {http} from '../../../tool/api/request';
import {msg, lo} from '../../../tool/fun';
import useReactRouter from 'use-react-router';
import {Link} from 'react-router-dom';

const los = lo();


export default function Home() {

    const [dataSource, setData] = useState([]);

    const route = useReactRouter();
    const history = route.history;

    const getList = (param) => {
        msg.loading("load list..");
        http.msg.list(param)
            .then(res => {
                msg.hide();
                if (res.code == 200) {
                    if (res.data.length > 0) {
                        let data = res.data;
                        console.log(data);
                        let ilist = [];
                        for (let i = 0; i < data.length; i++) {
                            let v = data[i];
                            let tmp = {};
                            let jdat = JSON.parse(v.content);
                            tmp.title = v.title;
                            tmp.content = <Link to={{pathname: jdat.uri}}><span>{jdat.text}</span></Link>;
                            tmp.key = v.guid;
                            ilist.push(tmp);
                        }
                        setData(ilist);
                    } else {
                        setData([]);
                    }

                } else {
                    alert(res.message);
                    console.error('login error');
                }
            })
            .catch(error => {
                // alert('login error');
                console.log('error', error);
            });
    };

    useEffect(() => {
        getList({});
    }, []);


    const read = (msgId) => {
        //read
        http.msg.read({guid: msgId})
            .then(res => {
                if (res.code == 200) {
                    let noticeNum = los.get("noticeNum");
                    if (!isNaN(noticeNum)) {
                        let num = noticeNum - 1;
                        los.add("noticeNum", num);
                        console.log(los.get("noticeNum"));
                    }
                } else {
                    msg.error(res.message);
                    console.error('login error');
                }
            })
            .catch(error => {
                // alert('login error');
                console.log('error', error);
            });
    };

    const onExpand = (val) => {
        read(val);
        console.log(val);
    };

    return (
        <div>
            <Collapse accordion onExpand={onExpand} dataSource={dataSource}/>
        </div>
    );
}

