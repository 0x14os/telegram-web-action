import React from 'react';

const LoginIntro = () => {
  return (
    <div style={styles.container}>
      <div style={styles.content}>
        <div style={styles.title}>Web电报</div>
      </div>
    </div>
  );
};

const styles = {
  container: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    position: 'relative',
  },
  content: {
    width: '400px',
    color: '#333',
  },
  title: {
    marginBottom: '20px',
    fontWeight: '700',
    fontSize: '38px',
    lineHeight: '1.5',
  },
  description: {
    margin: '0',
    fontSize: '16px',
    color: '#333',
    letterSpacing: '0.45px',
    lineHeight: '40px',
  },
};

export default LoginIntro;
