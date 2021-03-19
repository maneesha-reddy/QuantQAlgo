import React, { Component } from "react";
import { Card } from "antd";
import { LockTwoTone } from "@ant-design/icons";
import Button from "@material-ui/core/Button";
import CssBaseline from "@material-ui/core/CssBaseline";
import TextField from "@material-ui/core/TextField";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import Checkbox from "@material-ui/core/Checkbox";
// import Link from "@material-ui/core/Link";
import Typography from "@material-ui/core/Typography";
import { Form } from "antd";
import axios from "axios";
import { NavLink, withRouter } from "react-router-dom";
import { notification, Space } from "antd";
import Snackbar from "@material-ui/core/Snackbar";
import MuiAlert from "@material-ui/lab/Alert";
import { Layout, Menu, Breadcrumb } from "antd";
const { Header, Content } = Layout;
class SignIn extends Component {
  constructor(props) {
    super(props);
    this.state = {
      log: false,
      open: true,
    };
  }

  render() {
    const validateMessages = {
      required: "${label} is required!",
      types: {
        email: "${label} is not a valid email!",
        number: "${label} is not a valid number!",
      },
      number: {
        range: "${label} must be between ${min} and ${max}",
      },
    };
    function Alert(props) {
      return <MuiAlert elevation={6} variant="filled" {...props} />;
    }
    const handleClose = (event, reason) => {
      if (reason === "clickaway") {
        return;
      }
      this.setState({ open: false });
    };
    const onFinish = (values) => {
      console.log("Success:", values);
      // let url = "http://127.0.0.1:8000/website/signin/";
      let url = "https://quantqalgo.ddns.net/website/signin/";
      // axios.post(url, values, {}).then((res) => {
      //   console.warn(res.data["sucessful"], "sc");
      //   this.props.auth(res.data["sucessful"]);
      //   this.setState({ log: res.data["sucessful"] });
      // });
      this.props.auth(true);
      this.setState({ log: true });
      if (this.state.log == true) {
        // notification.open({
        //   // message: "Notification Title",
        //   description: (
        return (
          <Snackbar
            open={this.state.open}
            autoHideDuration={6000}
            onClose={handleClose}
          >
            <Alert onClose={handleClose} severity="success">
              sucessfully logged in!
            </Alert>
          </Snackbar>
        );
        // ;
        // ),
        // });
        history.push("/dashboard");
      } else {
        notification["error"]({
          message: "Notification Title",
          description: "error",
        });
      }
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
          <Card style={{ width: 500 }} hoverable={true} bordered={false}>
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
                validateMessages={validateMessages}
              >
                <Form.Item
                  // label="Email Address"
                  name="email"
                  rules={[
                    {
                      type: "email",
                      required: true,
                      message: "Please input your valid email!",
                    },
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
                  {/* <NavLink to="/"> */}
                  <Button
                    type="submit"
                    fullWidth
                    variant="contained"
                    color="primary"
                  >
                    Sign In
                  </Button>
                  {/* </NavLink> */}
                </Form.Item>
                {/* <NavLink to="/dashboard">Forgot password?</NavLink> */}
                <NavLink to="/SignUp">Don't have an account? Sign Up</NavLink>
              </Form>
            </div>
          </Card>
        </Content>
      </Layout>
    );
  }
}

export default withRouter(SignIn);
