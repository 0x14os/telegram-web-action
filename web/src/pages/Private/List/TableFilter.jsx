import React from 'react';
import { Button} from '@alifd/next';
import styles from '../../../layouts/css/table.module.scss';
import useReactRouter from 'use-react-router';


export default function TableFilter() {

  const routeResult = useReactRouter();
  const history = routeResult.history;


  const handleHistoryPush = () => {
    history.push('/private/edit/0');
  };

  return (
    <div className={styles.tableFilter}>
      <div className={styles.title}>私信任务</div>
      <div className={styles.filter}>
        <Button type="primary" size="small" onClick={handleHistoryPush} className={styles.submitButton}>
          添加
        </Button>
      </div>
    </div>
  );
}
