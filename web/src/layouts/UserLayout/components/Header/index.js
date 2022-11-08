import React from 'react';
import { Link } from 'react-router-dom';
import './index.scss';

export default () => {
  return (
    <div style={styles.container}>
      <Link to="/" style={styles.logoLink}>
        Web电报群控
      </Link>
    </div>
  );
};

const styles = {
  container: {
    height: '60px',
    borderBottom: '1px solid rgba(255, 255, 255, 0.3)',
    display: 'flex',
    justifyContent: 'space-between',
  },
  logoLink: {
    display: 'flex',
    alignItems: 'center',
    fontSize: '24px',
    fontWeight: 'bold',
    paddingLeft: '20px',
    color: '#fff',
  },
  navs: {
    display: 'flex',
  },
  navMenu: {
    position: 'relative',
  },
  navLink: {
    display: 'block',
    height: '60px',
    lineHeight: '60px',
    padding: '0 20px',
    fontSize: '15px',
    color: '#fff',
    textDecoration: 'none',
  },
  NavIconLink: {
    padding: '0 30px',
  },
  subNavs: {
    position: 'absolute',
    left: '0',
    width: '140px',
    background: '#272B2F',
  },
  subNavMenu: {
    height: '38px',
    lineHeight: '38px',
  },
  subNavLink: {
    paddingLeft: '12px',
    display: 'block',
    color: '#fff',
    fontSize: '14px',
  },
  internationalImg: {
    width: '16px',
    height: '16px',
    position: 'absolute',
    left: '10px',
    top: '22px',
  },
};
