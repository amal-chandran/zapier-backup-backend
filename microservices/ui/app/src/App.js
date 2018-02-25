import React, { Component } from 'react';
import { Login_Signup, Home } from "./views";
import { store, history } from "./helper";
import { Provider, connect } from "react-redux";
import { PrivateRoute, Notifi } from "./components";
import { ConnectedRouter } from 'react-router-redux';

import {
  Route, Switch, Redirect
} from "react-router-dom";

class App extends Component {
  render() {
    return (
      <Provider store={store}>
        <ConnectedRouter history={history}>
          <div>
            <Notifi />
            <Switch>
              <PrivateRoute path="/home" component={Home} />
              <Route exact path="/" component={Login_Signup} />
            </Switch>
          </div>
        </ConnectedRouter>
      </Provider >
    );
  }
}

export default App;
