import React from "react";
import { Layout, Menu, Breadcrumb } from "antd";
import "./App.css";

import SideBar from "./components/sidebar/sidebar";
import TopBar from "./components/topbar/TopBar";
// import { Route, Switch } from "react-router-dom";
import { HashRouter, BrowserRouter, Route, Switch } from "react-router-dom";
import DashBoard from "./components/dashboard/Dashboard";
import HomeFilled from "@ant-design/icons";
import Backlist from "./components/backlist/Backlist";
import PaperTrade from "./components/paperTrade/PaperTrade";
import { Socket } from "socket.io-client";
import SignIn from "./components/authenticate/signIn";
import SignUp from "./components/authenticate/signUp";

import LoginTopBar from "./components/logintopbar/loginTopbar";
const { Header, Content } = Layout;

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      collapsed: false,
      authen: false,
    };
    // this.onAuthenticate = this.onAuthenticate.bind(this);
  }

  onCollapse = (collapsed) => {
    console.log(collapsed);
    this.setState({ collapsed });
  };

  onAuthenticate = (value) => {
    this.setState({ authen: value });
  };

  render() {
    console.log(this.state.authen, "hello");
    return (
      <div>
        <Layout>
          {this.state.authen ? (
            <>
              <TopBar style={{ padding: 100 }} />
            </>
          ) : (
            <>
              <LoginTopBar />

              {/* <Switch>
                  
                  <Route path="/SignUp" component={SignUp}></Route>
                 
                  <Route
                    path="/SignIn"
                    render={(props) => (
                      <SignIn {...props} auth={this.onAuthenticate} />
                    )}
                  />
                </Switch> */}
            </>
          )}
          <Layout style={{ minHeight: "100vh" }}>
            <SideBar />
            <Layout className="site-layout">
              {/* style={{backgroundColor: "#cff6cf" } */}
              <Header
                className="site-layout-background"
                style={{ padding: 0 }}
              />
              <Content style={{ margin: "0 16px" }}>
                <Switch>
                  <Route path="/dashboard" component={DashBoard}></Route>
                  <Route path="/backtest" component={Backlist}></Route>
                  <Route path="/paperTrade" component={PaperTrade}></Route>
                  <Route path="/SignUp" component={SignUp}></Route>
                  {/* <Route path="/SignIn" component={SignIn}></Route> */}
                  <Route
                    path="/SignIn"
                    render={(props) => (
                      <SignIn {...props} auth={this.onAuthenticate} />
                    )}
                  />
                </Switch>
              </Content>
            </Layout>
          </Layout>
        </Layout>
      </div>
    );
  }
}

export default App;
