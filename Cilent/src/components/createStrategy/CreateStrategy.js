import React, { Component } from "react";
import { Form, Input, Button, Checkbox, Card } from "antd";
class CreateStrategy extends Component {
  constructor(props) {
    super(props);
    this.state = {};
  }
  render() {
    const layout = {
      labelCol: { span: 8 },
      wrapperCol: { span: 16 },
    };
    const tailLayout = {
      wrapperCol: { offset: 8, span: 16 },
    };

    const onFinish = (values) => {
      console.log("Success:", values);
    };

    const onFinishFailed = (errorInfo) => {
      console.log("Failed:", errorInfo);
    };
    const exchangeOptions = ["NSE", "NFO", "MCX", "Nasdaq", "Forex", "Crypto"];
    const segmentOptions = [
      "Cash",
      "Index features",
      "Index Options",
      "Stock futures",
      "StockOptions",
    ];
    function onChange(checkedValues) {
      console.log("checked = ", checkedValues);
    }
    return (
      <Card
        hoverable
        // title="BackTesting"
        style={{ width: 700 }}
      >
        <Form
          {...layout}
          name="basic"
          initialValues={{ remember: true }}
          onFinish={onFinish}
          onFinishFailed={onFinishFailed}
        >
          <Form.Item
            label="Email"
            name="email"
            rules={[{ required: true, message: "Please input your username!" }]}
          >
            <Input />
          </Form.Item>

          <Form.Item
            label="Your Name"
            name="yourname"
            rules={[{ required: true, message: "Please input your password!" }]}
          >
            <Input />
          </Form.Item>
          <Form.Item
            label="Mobile number"
            name="mobile"
            rules={[{ required: true, message: "Please input your password!" }]}
          >
            <Input />
          </Form.Item>

          <Form.Item
            label="What name you want to give to ur strategy"
            name="strategyname"
            rules={[{ required: true, message: "Please input your password!" }]}
          >
            <Input />
          </Form.Item>

          <Form.Item
            label="which exchange"
            name="exchange"
            valuePropName="checked"
            rules={[{ required: true, message: "Please input your password!" }]}
          >
            <Checkbox.Group
              options={exchangeOptions}
              defaultValue={["NSE"]}
              onChange={onChange}
            />
          </Form.Item>
          <Form.Item
            label="which segment"
            name="segment"
            valuePropName="checked"
            rules={[{ required: true, message: "Please input your password!" }]}
          >
            <Checkbox.Group
              options={segmentOptions}
              defaultValue={["Cash"]}
              onChange={onChange}
            />
          </Form.Item>

          <Form.Item {...tailLayout}>
            <Button type="primary" htmlType="submit">
              Submit
            </Button>
          </Form.Item>
        </Form>
      </Card>
    );
  }
}

export default CreateStrategy;
