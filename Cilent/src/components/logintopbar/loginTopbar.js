import React from "react";
import { Layout } from "antd";
import { NavLink } from "react-router-dom";
import { Button } from "antd";

// const { Option } = Select;

const { Header } = Layout;

function handleChange(value) {
  console.log(`selected ${value}`);
}

function LoginTopBar(props) {
  return (
    <Header
      className="header"
      style={{ position: "fixed", zIndex: 1, width: "100%" }}
    >
      <Button type="primary" ghost style={{ float: "right" }}>
        <NavLink to="/SignIn">Login</NavLink>
      </Button>
      <Button type="primary" style={{ float: "right" }} ghost>
        <NavLink to="/SignUp">SignUp</NavLink>
      </Button>

      <Button
        type={props.darkmode ? "dashed" : "primary"}
        onClick={props.toogleTheme}
      >
        Dark
      </Button>
    </Header>
  );
}

export default LoginTopBar;
