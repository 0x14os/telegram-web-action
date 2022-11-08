import React from 'react';
import { Button} from '@alifd/next';
import styles from '../../../layouts/css/table.module.scss';
import useReactRouter from 'use-react-router';


export default function TableFilter() {

    const route = useReactRouter();
    const history = route.history;

  //route.match.params.title

  const handleHistoryPush = () => {
    history.push('/task/list');
  };



  return (
    <div className={styles.tableFilter}>
      <div className={styles.title}>{route.match.params.title ? route.match.params.title : "未知"} - 群发送列表</div>
      <div className={styles.filter}>
        <Button type="primary" size="small" onClick={handleHistoryPush} className={styles.submitButton}>
          返回
        </Button>
      </div>
    </div>
  );
}
