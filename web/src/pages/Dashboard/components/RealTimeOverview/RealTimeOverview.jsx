import React, { Component } from 'react';
import IceContainer from '@icedesign/container';
import { Grid } from '@alifd/next';

const { Row, Col } = Grid;

export default class RealTimeOverview extends Component {
  static displayName = 'RealTimeOverview';

  static propTypes = {};

  static defaultProps = {};

  constructor(props) {
    super(props);
    this.state = {};
  }

  render() {
    return (
      <IceContainer title="实时概况">
        <Row wrap>
          <Col l="12" xxs="24">
            <div style={styles.dataItem}>
              <img
                src={require('./images/TB1iFKccamWBuNjy1XaXXXCbXXa-140-140.png')}
                alt=""
                style={styles.dataItemImg}
              />
              <div style={styles.dataItemUnit}>
                <div style={styles.unitTitle}>今日发送</div>
                <div style={styles.unitAmount}>10000</div>
                <div style={styles.unitFooter}>昨日：300</div>
              </div>
              <div style={styles.dataItemUnit}>
                <div style={styles.unitTitle}>今日失败</div>
                <div style={styles.unitAmount}>100</div>
                <div style={styles.unitFooter}>昨日：70</div>
              </div>
            </div>
          </Col>

          <Col l="12" xxs="24">
            <div style={styles.dataItem}>
              <img
                src={require('./images/TB1iFKccamWBuNjy1XaXXXCbXXa-140-140.png')}
                alt=""
                style={styles.dataItemImg}
              />
              <div style={styles.dataItemUnit}>
                <div style={styles.unitTitle}>最近7天成功</div>
                <div style={styles.unitAmount}>381</div>
              </div>
              <div style={styles.dataItemUnit}>
                <div style={styles.unitTitle}>最近7天失败</div>
                <div style={styles.unitAmount}>120</div>
              </div>
            </div>
          </Col>

          {/*<Col l="12" xxs="24">*/}
          {/*  <div style={styles.dataItem}>*/}
          {/*    <img*/}
          {/*      src={require('./images/TB1Py4_ceuSBuNjy1XcXXcYjFXa-142-140.png')}*/}
          {/*      alt=""*/}
          {/*      style={styles.dataItemImg}*/}
          {/*    />*/}
          {/*    <div style={styles.dataItemUnit}>*/}
          {/*      <div style={styles.unitTitle}>待支付</div>*/}
          {/*      <div style={styles.unitAmount}>182</div>*/}
          {/*      <div style={styles.unitFooter}>昨日：123</div>*/}
          {/*    </div>*/}
          {/*    <div style={styles.dataItemUnit}>*/}
          {/*      <div style={styles.unitTitle}>已支付</div>*/}
          {/*      <div style={styles.unitAmount}>96</div>*/}
          {/*      <div style={styles.unitFooter}>昨日：90</div>*/}
          {/*    </div>*/}
          {/*  </div>*/}
          {/*</Col>*/}

          {/*<Col l="12" xxs="24">*/}
          {/*  <div style={styles.dataItem}>*/}
          {/*    <img*/}
          {/*      src={require('./images/TB1Ni4_ceuSBuNjy1XcXXcYjFXa-142-140.png')}*/}
          {/*      alt=""*/}
          {/*      style={styles.dataItemImg}*/}
          {/*    />*/}
          {/*    <div style={styles.dataItemUnit}>*/}
          {/*      <div style={styles.unitTitle}>最近7天销售</div>*/}
          {/*      <div style={styles.unitAmount}>89</div>*/}
          {/*    </div>*/}

          {/*    <div style={styles.dataItemUnit}>*/}
          {/*      <div style={styles.unitTitle}>最近30天销售</div>*/}
          {/*      <div style={styles.unitAmount}>568.00</div>*/}
          {/*    </div>*/}
          {/*  </div>*/}
          {/*</Col>*/}
        </Row>
      </IceContainer>
    );
  }
}

const styles = {
  dataItem: {
    display: 'flex',
    flexBasis: '50%',
    padding: '20px',
    alignItems: 'center',
  },
  dataItemImg: {
    width: '58px',
    marginRight: '30px',
  },
  dataItemUnit: {
    height: '72px',
    display: 'flex',
    flexBasis: '50%',
    flexDirection: 'column',
    justifyContent: 'space-between',
  },
  unitTitle: {
    color: '#666',
    fontSize: '12px',
  },
  unitAmount: {
    color: '#333',
    fontSize: '24px',
  },
  unitFooter: {
    color: '#999',
    fontSize: '12px',
  },
};
