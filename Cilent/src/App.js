import React from "react";
import { Layout, Menu, Breadcrumb } from "antd";
import "./App.css";

import SideBar from "./components/sidebar/sidebar";
import TopBar from "./components/topbar/TopBar";
import { Route, Switch } from "react-router-dom";
import DashBoard from "./components/dashboard/Dashboard";
import HomeFilled from "@ant-design/icons";
import Backlist from "./components/backlist/Backlist";
import PaperTrade from "./components/paperTrade/PaperTrade"
import { Socket } from "socket.io-client";
const { Header, Content } = Layout;
class App extends React.Component {
  state = {
    collapsed: false,
  };

  onCollapse = (collapsed) => {
    console.log(collapsed);
    this.setState({ collapsed });
  };

  render() {
    return (
      <Layout >
        <TopBar style={{ padding: 100 }} />
        <Layout style={{ minHeight: "100vh"}}>
          <SideBar />
          <Layout className="site-layout" >
          {/* style={{backgroundColor: "#cff6cf" } */}
            <Header className="site-layout-background" style={{ padding: 0 }} />
            <Content style={{ margin: "0 16px"}}>
              {/* <Breadcrumb style={{ margin: "16px 0" }}>
                <Breadcrumb.Item icon={<HomeFilled twoToneColor="#eb2f96"/>}>Home</Breadcrumb.Item>
                <Breadcrumb.Item>Dashboard</Breadcrumb.Item>
              </Breadcrumb> */}
              <Switch>
                <Route path="/dashboard" component={DashBoard}></Route>
                <Route path="/backtest" component={Backlist}></Route>
                <Route path="/paperTrade" component={PaperTrade}></Route>
               
              </Switch>
            </Content>
          </Layout>
        </Layout>
      </Layout>
    );
  }
}

export default App;
