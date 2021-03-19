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
import axios from "axios";
import { NavLink, withRouter } from "react-router-dom";
import { Layout, Menu, Breadcrumb } from "antd";
const { Header, Content } = Layout;

class SignUp extends Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  render() {
    const onFinish = (values) => {
      console.log("Success:", values);
      // let url = "http://127.0.0.1:8000/website/signup/";
      let url = "https://quantqalgo.ddns.net/website/signup/";

      axios.post(url, values, {}).then((res) => {
        console.warn(res.data);
      });
      history.push("/SignIn");
    };

    const onFinishFailed = (errorInfo) => {
      console.log("Failed:", errorInfo);
    };
    const { location, history } = this.props;
    return (
      <Layout className="site-layout">
        {/* style={{backgroundColor: "#cff6cf"  */}
        <Header className="site-layout-background" style={{ padding: 0 }} />
        <Content style={{ margin: "0 16px" }}>
          <Card
            style={{ width: 500, alignContent: "center" }}
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
                Sign Up
              </Typography>
              <Form
                name="basic"
                initialValues={{ remember: true }}
                onFinish={onFinish}
                onFinishFailed={onFinishFailed}
              >
                <Form.Item
                  name="firstName"
                  rules={[
                    { required: true, message: "Please input your firstname!" },
                  ]}
                >
                  <TextField
                    autoComplete="fname"
                    name="firstName"
                    variant="outlined"
                    required
                    fullWidth
                    id="firstName"
                    label="First Name"
                    autoFocus
                  />
                </Form.Item>

                <Form.Item
                  name="lastName"
                  rules={[
                    { required: true, message: "Please input your lastname!" },
                  ]}
                >
                  <TextField
                    variant="outlined"
                    required
                    fullWidth
                    id="lastName"
                    label="Last Name"
                    name="lastName"
                    autoComplete="lname"
                  />
                </Form.Item>

                <Form.Item
                  name="email"
                  rules={[
                    { required: true, message: "Please input your email!" },
                  ]}
                >
                  <TextField
                    variant="outlined"
                    required
                    fullWidth
                    id="email"
                    label="Email Address"
                    name="email"
                    autoComplete="email"
                  />
                </Form.Item>

                <Form.Item
                  name="password"
                  rules={[
                    { required: true, message: "Please input your password!" },
                  ]}
                >
                  <TextField
                    variant="outlined"
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
                  control={
                    <Checkbox value="allowExtraEmails" color="primary" />
                  }
                  label="I want to receive inspiration, marketing promotions and updates via email."
                />

                <Form.Item>
                  <Button
                    type="submit"
                    fullWidth
                    variant="contained"
                    color="primary"
                  >
                    {/* <NavLink to="/SignIn"> Sign Up</NavLink> */}
                    Sign Up
                  </Button>
                </Form.Item>
                <NavLink to="/SignIn">
                  {" "}
                  Already have an account? Sign in
                </NavLink>
              </Form>
            </div>
          </Card>
        </Content>
      </Layout>
    );
  }
}

export default withRouter(SignUp);
