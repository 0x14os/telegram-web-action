import React, { Component } from 'react';
import { Switch, Route, Redirect } from 'react-router-dom';
import { Grid } from '@alifd/next';
import Footer from './components/Footer';
import Intro from './components/Intro';
import bj from './components/img/bj.jpeg';
import routerData from '../../routerConfig';

const { Row, Col } = Grid;

import { statusToken, jump } from '../../tool/fun';

const token = statusToken();


export default class UserLayout extends Component {

  is_token(auth, token) {
    // console.log('auth', auth);
    // console.log('token', token);
    if (auth && token) {
      return true;
    } else {
      return false;
    }
  }


  render() {
    return (
      <div style={styles.container}>
        <div style={styles.mask}/>
        <Row wrap style={styles.row}>
          <Col l="12">
            <Intro />
          </Col>

          <Col l="12">
            <div style={styles.form}>
              <Switch>
                {routerData.map((item, index) => {
                  return this.is_token(item.auth, token) == true ? (jump('/')) : (
                    <Route
                      key={index}
                      path={item.path}
                      component={item.component}
                      exact={item.exact}
                    />
                  );
                })}

                <Redirect exact to="/login"/>
              </Switch>
            </div>
          </Col>
        </Row>
        <Footer/>
      </div>
    );
  }
}

const styles = {
  container: {
    position: 'relative',
    width: '100wh',
    minWidth: '1200px',
    height: '100vh',
    backgroundImage: `url(${bj})`,
    backgroundSize: 'cover',
    display: 'flex',
    flexDirection: 'column',
  },
  mask: {
    position: 'absolute',
    top: '0',
    right: '0',
    bottom: '0',
    left: '0',
    background: 'rgba(255, 255, 255, 0.3)',
  },
  row: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    flex: '1',
  },
  form: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
};
