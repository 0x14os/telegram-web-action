import React from 'react';
import {Button} from '@alifd/next';
import styles from '../../../layouts/css/table.module.scss';
import useReactRouter from 'use-react-router';

import {msg, lo} from '../../../tool/fun';

const los = lo();

export default function TableFilter() {

    const routeResult = useReactRouter();
    const history = routeResult.history;
    const role = los.get("role");

    const handleHistoryPush = () => {
        history.push('/admin/edit/add/0');
    };

    return (
        <div className={styles.tableFilter}>
            <div className={styles.title}>用户管理</div>
            <div className={styles.filter}>
                {role == 1 ? (
                    <Button type="primary" size="small" onClick={handleHistoryPush} className={styles.submitButton}>
                        添加
                    </Button>) : ''}

            </div>
        </div>
    );
}
