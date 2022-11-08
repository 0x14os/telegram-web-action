import React from 'react';
import { Button} from '@alifd/next';
import styles from '../../../layouts/css/table.module.scss';
import useReactRouter from 'use-react-router';


export default function TableFilter() {

  const routeResult = useReactRouter();
  const history = routeResult.history;


  const handleHistoryPush = () => {
    history.push('/private/list');
  };

  return (
    <div className={styles.tableFilter}>
      <div className={styles.title}>发送列表</div>
      <div className={styles.filter}>
        <Button type="primary" size="small" onClick={handleHistoryPush} className={styles.submitButton}>
          返回
        </Button>
      </div>
    </div>
  );
}
