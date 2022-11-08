import React, { Component } from 'react';
import SelectableTable from './components/SelectableTable';

export default function() {
  return (
    <div className="Test-page">
      {/* 可批量操作的表格 */}
      <SelectableTable />
    </div>
  );
}
