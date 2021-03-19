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
import LiveTrade from "./components/Livetrade/LiveTrade";
import LoginTopBar from "./components/logintopbar/loginTopbar";
import CreateStrategy from "./components/createStrategy/CreateStrategy";
import Homepage from './components/homepage/homepage'
const { Header, Content } = Layout;

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      collapsed: false,
      authen: false,
      darkmode: "darkmode",
    };
    // this.onAuthenticate = this.onAuthenticate.bind(this);
  }

  onCollapse = (collapsed) => {
    console.log(collapsed);
    this.setState({ collapsed });
  };

  onAuthenticate = (value) => {
    this.setState({ authen: value });
    console.log(value, "value");
  };

  toogleTheme = () => {
    console.log("Toogling theme!");
    this.setState(
      (prevState) => {
        return {
          darkmode:
            prevState.darkmode === "darkmode" ? "lightmode" : "darkmode",
        };
      },
      function () {
        console.log(this.state.darkmode);
      }
    );
  };

  render() {
    // console.log(this.state.authen, "hello");
    return (
      <>
        <Layout className={this.state.darkmode}>
          {this.state.authen ? (
            <>
              <TopBar
                style={{ padding: 100 }}
                toogleTheme={this.toogleTheme}
                darkmode={this.state.darkmode}
              />
              <Layout
              // style={{ minHeight: "100vh" }}
              >
                <SideBar />
                <Layout className="site-layout">
                  {/* style={{backgroundColor: "#cff6cf" } */}
                  <Header
                    className="site-layout-background"
                    style={{ padding: 0 }}
                  />
                  <Content
                  // style={{ margin: "0 16px" }}
                  >
                    <Switch>
                      <Route
                        path={["/dashboard"]}
                        component={DashBoard}
                      ></Route>
                      <Route path="/backtest" component={Backlist}></Route>
                      <Route path="/paperTrade" component={PaperTrade}></Route>
                      <Route path="/liveTrade" component={LiveTrade}></Route>
                      <Route
                        path="/createTrade"
                        component={CreateStrategy}
                      ></Route>
                    </Switch>
                  </Content>
                </Layout>
              </Layout>
            </>
          ) : (
            <>
              {/* <LoginTopBar
                toogleTheme={this.toogleTheme}
                darkmode={this.state.darkmode}
              />
              <Layout className="site-layout">
                style={{backgroundColor: "#cff6cf" }
                <Header
                  className="site-layout-background"
                  style={{ padding: 0 }}
                />
                <Content
                  style={{ margin: "0 16px" }}
                > */}
                  <Switch>
                    <Route path="/SignUp" component={SignUp}></Route>
                    <Route
                      path="/SignIn"
                      render={(props) => (
                        <SignIn {...props} auth={this.onAuthenticate} />
                      )}
                    />
                    <Route path = "/" component={Homepage}></Route>
                  </Switch>
                {/* </Content>
              </Layout> */}
            </>
          )}
        </Layout>
      </>
    );
  }
}

export default App;
