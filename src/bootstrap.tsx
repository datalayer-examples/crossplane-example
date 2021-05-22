import React from 'react';
import { render } from 'react-dom';
import Database from './Database';
import { setConfig } from './Config';

import './index.css';

let config = Object.create({});
const htmlConfig = document.getElementById('crossplane-example-config-data');
if (htmlConfig) {
  config = JSON.parse(htmlConfig.textContent || '') as {
    [key: string]: string;
  };
  setConfig(config);
}

render(
  <React.StrictMode>
    <Database
      formName='Create a user'
      formDescription='Data from the Postgresql database.'
      />
  </React.StrictMode>,
  document.getElementById('root')
);
