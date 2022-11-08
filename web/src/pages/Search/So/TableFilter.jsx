import React from 'react';
import {Button} from '@alifd/next';
import styles from '../../../layouts/css/table.module.scss';
import useReactRouter from 'use-react-router';


export default function TableFilter() {

    const route = useReactRouter();
    const history = route.history;


    const handleHistoryPush = () => {
        // console.log(route);
        // console.log(route.match.params);
        // if (route.match.params.id != '0') {
        //     history.push('/account/group/list/' + route.match.params.id);
        // }
    };

    return (
        <div className={styles.tableFilter}>
            <div className={styles.title}>群成员</div>
            {/*<div className={styles.filter}>*/}
            {/*    <Button type="primary" size="small" onClick={handleHistoryPush} className={styles.submitButton}>*/}
            {/*        返回*/}
            {/*    </Button>*/}
            {/*</div>*/}
        </div>
    );
}
