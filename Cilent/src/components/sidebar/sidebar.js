import React, { Component } from "react";
import { Layout, Menu} from 'antd';
import 'antd/dist/antd.css';


import {
  DesktopOutlined,
  PieChartOutlined,
  BarsOutlined,
  FileOutlined,
  TeamOutlined,
  UserOutlined,
  HomeFilled,
  QuestionCircleFilled,
  RocketFilled,

} from '@ant-design/icons';
import { NavLink } from "react-router-dom";
const { Sider } = Layout;
const { SubMenu } = Menu;
class SideBar extends Component {
  constructor(props) {
    super(props);
    this.state = {};
  }
  render() {
    return (
      <Sider
        breakpoint="lg"
        collapsedWidth="0"
        onBreakpoint={(broken) => {
          console.log(broken);
        }}
        onCollapse={(collapsed, type) => {
          console.log(collapsed, type);
        }}
        style={{
            marginTop: 64,
          }}
      >
        <Menu theme="dark" defaultSelectedKeys={["1"]} mode="inline">
          <Menu.Item key="1" icon={<HomeFilled />}>
            
            <NavLink to ="/dashboard" >Dashboard</NavLink>
          </Menu.Item>

          <SubMenu key="sub1" icon={<RocketFilled />} title="Deployment">
            <Menu.Item key="2">
            <NavLink to ="/backtest" > BackTest</NavLink>
                 </Menu.Item>
            <Menu.Item key="3">
            <NavLink to ="/paperTrade" >Paper Trade</NavLink>
              </Menu.Item>
            <Menu.Item key="4">Optimise</Menu.Item>
            <Menu.Item key="5">Live Trade</Menu.Item>
          </SubMenu>
          <SubMenu key="sub2" icon={<TeamOutlined />} title="Subscribe">
            <Menu.Item key="6">Team 1</Menu.Item>
            <Menu.Item key="8">Team 2</Menu.Item>
          </SubMenu>
          <Menu.Item key="9" icon={<BarsOutlined />}>
            contact
          </Menu.Item>
          <Menu.Item key="10" icon={<DesktopOutlined />}>
            Blog & Videos
          </Menu.Item>
          <Menu.Item key="11" icon={<QuestionCircleFilled />}>
            FAQ
          </Menu.Item>
          {/* <Menu.Item key="9" icon={<FileOutlined />} /> */}
        </Menu>
      </Sider>
    );
  }
}

export default SideBar;
