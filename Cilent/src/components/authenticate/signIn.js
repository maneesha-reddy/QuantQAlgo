import React, { Component } from "react";
import { Card } from "antd";
import { LockTwoTone } from "@ant-design/icons";
import Button from "@material-ui/core/Button";
import CssBaseline from "@material-ui/core/CssBaseline";
import TextField from "@material-ui/core/TextField";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import Checkbox from "@material-ui/core/Checkbox";
import Link from "@material-ui/core/Link";
import Typography from "@material-ui/core/Typography";
import { Form } from "antd";

import { NavLink } from "react-router-dom";

class SignIn extends Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  render() {
    const onFinish = (values) => {
      console.log("Success:", values);
      // this.props.hello();
      this.props.auth(true);
    };

    const onFinishFailed = (errorInfo) => {
      console.log("Failed:", errorInfo);
    };
    return (
      <Card
        style={{ width: 500, alignContent: "center", left: 400, top: 120 }}
        hoverable={true}
        bordered={true}
      >
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
          }}
        >
          <CssBaseline />
          <LockTwoTone
            twoToneColor="#eb2f96"
            size="large"
            style={{ alignContent: "center" }}
          />

          <Typography component="h1" variant="h5">
            Sign in
          </Typography>
          <Form
            name="basic"
            initialValues={{ remember: true }}
            onFinish={onFinish}
            onFinishFailed={onFinishFailed}
          >
            <Form.Item
              // label="Email Address"
              name="email"
              rules={[
                { required: true, message: "Please input your username!" },
              ]}
            >
              <TextField
                variant="outlined"
                margin="normal"
                required
                fullWidth
                id="email"
                label="Email Address"
                name="email"
                autoComplete="email"
                autoFocus
              />
            </Form.Item>
            <Form.Item
              // label="Password"
              name="password"
              rules={[
                { required: true, message: "Please input your password!" },
              ]}
            >
              <TextField
                variant="outlined"
                margin="normal"
                required
                fullWidth
                name="password"
                label="Password"
                type="password"
                id="password"
                autoComplete="current-password"
              />
            </Form.Item>
            <FormControlLabel
              control={<Checkbox value="remember" color="primary" />}
              label="Remember me"
            />
            <Form.Item>
              <Button
                type="submit"
                fullWidth
                variant="contained"
                color="primary"
              >
                <NavLink to="/dashboard">Sign In</NavLink>
              </Button>
            </Form.Item>
            <NavLink to="/dashboard">Forgot password?</NavLink>
            <NavLink to="/SignUp">Don't have an account? Sign Up</NavLink>
          </Form>
        </div>
      </Card>
    );
  }
}

export default SignIn;
