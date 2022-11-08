/* eslint no-undef:0, no-unused-expressions:0, array-callback-return:0 */
import React, {Component} from 'react';
import {Nav} from '@alifd/next';
import {withRouter, Link} from 'react-router-dom';
import {asideMenuConfig} from '../../../../menuConfig';
import './Aside.scss';


import {msg, lo} from '../../../../tool/fun';

const los = lo();

const NavItem = Nav.Item;

@withRouter
export default class BasicLayout extends Component {

    render() {
        const {location} = this.props;
        const {pathname} = location;
        const role = los.get("role");
        let list = [];

        if (role != 1) {
            if (asideMenuConfig.length >= 1) {
                asideMenuConfig.map((nav) => {
                    if (nav.name !== "用户") {
                        list.push(nav);
                    }
                });
            }
        } else {
            list = asideMenuConfig;
        }
        return (
            <Nav
                direction="ver"
                selectedKeys={[pathname]}
                className="ice-menu-custom"
                style={{width: 100}}
            >
                {Array.isArray(list) &&
                list.length > 0 &&
                list.map((nav) => {
                    // console.log("nav.name", nav);
                    return (
                        <NavItem key={nav.path} icon={nav.icon ? nav.icon : null}>
                            <Link to={nav.path} className="ice-menu-link">
                                <span className="ice-menu-item-text">{nav.name}</span>
                            </Link>
                        </NavItem>
                    );
                })}
            </Nav>
        );
    }
}
