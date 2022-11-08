import React, {useState, useEffect} from 'react';
import {Table, Button, Icon, Select, Form, Input, Pagination} from '@alifd/next';
import IceContainer from '@icedesign/container';

import styles from './index.module.scss';
import {http} from '../../../tool/api/request';
import {msg, lo} from '../../../tool/fun';

import useReactRouter from 'use-react-router';


const los = lo();

export default function Home() {

    const route = useReactRouter();
    const history = route.history;
    const button = <Button  style={{height:"32px" }}>search</Button>;

    // useEffect(() => {}, []);

    return (

        <div className={`${styles.selectableTable} selectable-table`}>

            <IceContainer className={styles.IceContainer}>
                <div>
                    {/* className={styles.GroupName}*/}
                    <Input.Group addonAfter={button} >
                       <Input
                            hasClear
                            // defaultValue="abc"
                            style={{ width: "600px",height:"30px" }}
                            placeholder="请搜索需要的电报公开群"
                        />
                    </Input.Group>
                </div>
            </IceContainer>

            <IceContainer>
                <div>
                    <Input.TextArea placeholder="搜索内容" style={{ width: "600px" }} aria-label="TextArea" />
                </div>
            </IceContainer>
        </div>
    );
}

