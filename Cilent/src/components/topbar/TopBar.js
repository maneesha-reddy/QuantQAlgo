import React from "react";
import logo from "./logo.png";
import { Layout } from "antd";
import { NavLink } from "react-router-dom";
import { Avatar } from "antd";
import { UserOutlined, BellOutlined, BellFilled } from "@ant-design/icons";
import "./TopBar.css";
import { Select, Button } from "antd";

// import { Select } from 'antd';
// import InputLabel from '@material-ui/core/InputLabel';
// import MenuItem from '@material-ui/core/MenuItem';
// import FormControl from '@material-ui/core/FormControl';
// import Select from "@material-ui/core/Select";
import { Badge } from "antd";

const { Option } = Select;

const { Header } = Layout;

function handleChange(value) {
  console.log(`selected ${value}`);
}

function TopBar(props) {
  // toggleTheme () {

  // }
  return (
    <Header
      className="header"
      style={{ position: "fixed", zIndex: 1, width: "100%" }}
    >
      <div>
        <NavLink to="">
          <img className="logo" src={logo} alt="logo"></img>
        </NavLink>

        <Badge
          className="site-badge-count-109"
          count={1}
          style={{
            backgroundColor: "#f50",
          }}
        >
          <BellFilled
            style={{
              fontSize: "25px",
              color: "#52c41a",
            }}
          />
        </Badge>
        {/* <div> */}
        <Avatar
          style={{
            backgroundColor: "#87d068",
            position: "absolute",
            right: "2vh",
            top: "2vh",
          }}
          size="large"
          icon={<UserOutlined />}
        />
        <Select
          defaultValue="My Account"
          className="dropdown"
          style={{
            position: "absolute",
            top: "2.5vh",
            right: "6vh",
            backgroundColor: "transparent",
            border: "transparent",
            // color: "white",
          }}
          onChange={handleChange}
        >
          <Option value="My Profile">My Profile</Option>
          <Option value="Settings">Settings</Option>
          <Option value="Logout">Logout</Option>
        </Select>
        <Button
          type={props.darkmode ? "dashed" : "primary"}
          onClick={props.toogleTheme}
          style={{ position: "absolute", top: "2.5vh" }}
        >
          Dark
        </Button>
        {/* </div> */}
        {/* <Button onClick = {toogleTheme}>Dark mode</Button> */}
      </div>
    </Header>
  );
}

export default TopBar;
