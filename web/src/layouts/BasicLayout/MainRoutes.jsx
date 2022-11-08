import React, { Component } from 'react';
import { Switch, Route, Redirect } from 'react-router-dom';
import NotFound from '../../components/NotFound';
import routerData from '../../routerConfig';
import { statusToken,jump } from '../../tool/fun';

const token = statusToken();

class MainRoutes extends Component {
  /**
   * 渲染路由组件
   */
  renderNormalRoute = (item, index) => {
    return item.component ? (
      <Route
        key={index}
        path={item.path}
        component={item.component}
        exact={item.exact}
      />
    ) : null;
  };

  is_token(auth, token) {
    // console.log('auth', auth);
    // console.log('token', token);
    if (auth && token) {
      return true;
    } else {
      return false;
    }
  }

  re() {
    return (
      <Switch>
        {/* 渲染路由表 */}
        {routerData.map((item, index) => {
          return this.is_token(item.auth, token) == false  ? (jump("/#/public/login")) : (
            <Route
              key={index}
              path={item.path}
              component={item.component}
              exact={item.exact}
            />
          );
        })}

        {/* 根路由默认重定向到 /dashboard */}
        <Redirect from="/" to="/dashboard" />

        {/* 未匹配到的路由重定向到 NotFound */}
        <Route component={NotFound}/>
      </Switch>
    );
  }

  render() {

    return this.re();

  }
}

export default MainRoutes;
