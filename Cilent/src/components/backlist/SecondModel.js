import React, { Component } from "react";
import TextField from "@material-ui/core/TextField";
import { Select } from "antd";
import { Row, Col } from "antd";
import { Modal, Button } from "antd";

import { Input, Form } from "antd";
const { Option } = Select;

function SecondModel(Component) {
  return function WrappedComponent(props) {
    const [form] = Form.useForm();
    return <Component {...props} myHook={form} />;
  };
}

class ClassSecondModel extends Component {
  constructor(props) {
    super(props);
    this.state = { ex: undefined };
  }
  onExchange = (value) => {
    console.log(value);
    this.setState({ ex: value });
  };

  render() {
    if (this.props.operation === "edit")
      this.props.myHook.setFieldsValue({
        name: this.props.autofill.name,
        exchange: this.props.autofill.exchange,
        symbols: this.props.autofill.symbols,
        StrikePrice: this.props.autofill.StrikePrice,
        segment: this.props.autofill.segment,
        Strategy: this.props.autofill.Strategy,
      });
    return (
      <div>
        <Modal
          title="Add to the list"
          centered
          visible={this.props.isVisible}
          onOk={
            () => {
              this.props.myHook
                .validateFields()
                .then((values) => {
                  this.props.myHook.resetFields();
                  this.props.handleModalValues(values);
                })
                .catch((info) => {
                  console.log("Validate Failed:", info);
                });
              this.props.setModal2Visible(false);
            }
            // () => this.setModal2Visible(false)
          }
          onCancel={() => this.props.setModal2Visible(false)}
          okText="Add"
          cancelText="cancel"
        >
          <Form form={this.props.myHook}>
            <Row>
              <Col span={12}>
                <Form.Item
                  style={{ fontWeight: "bolder" }}
                  name="name"
                  label="Name"
                  // rules={[{ required: true, message: "pls help me" }]}
                >
                  <Input
                    disabled={this.props.operation === "edit" ? true : false}
                    placeholder="Name"
                  />
                </Form.Item>
                <Form.Item
                  style={{ fontWeight: "bolder" }}
                  name="exchange"
                  label="exchange"
                  rules={[{ required: true, message: "" }]}
                >
                  <Select
                    // defaultValue={this.props.name}
                    showSearch
                    style={{ width: 200 }}
                    placeholder="exchange"
                    optionFilterProp="children"
                    onChange={this.onExchange}
                    filterOption={(input, option) =>
                      option.children
                        .toLowerCase()
                        .indexOf(input.toLowerCase()) >= 0
                    }
                  >
                    <Option value="NSE">NSE</Option>
                    <Option value="BSE">BSE</Option>
                    <Option value="NFO">NFO</Option>
                    <Option value="MCX">MCX</Option>
                    <Option value="CDS">CDS</Option>
                    <Option value="NSE_INDEX">NSE_INDEX</Option>
                  </Select>
                </Form.Item>

                <Form.Item
                  style={{ fontWeight: "bolder" }}
                  name="segment"
                  label="segment"
                  // rules={[{ required: true, message: "" }]}
                >
                  <Select
                    showSearch
                    disabled={
                      this.state.ex === "NSE" || this.state.ex === "BSE"
                        ? true
                        : false
                    }
                    style={{ width: 200 }}
                    placeholder="Segment"
                    optionFilterProp="children"
                    filterOption={(input, option) =>
                      option.children
                        .toLowerCase()
                        .indexOf(input.toLowerCase()) >= 0
                    }
                  >
                    <Option value="FUT">FUT</Option>
                    <Option value="OPT">OPT</Option>
                  </Select>
                </Form.Item>
              </Col>

              <Col span={12}>
                <Form.Item
                  style={{ fontWeight: "bolder" }}
                  name="symbols"
                  label="symbols"
                  rules={[{ required: true, message: "" }]}
                >
                  <Select
                    showSearch
                    style={{ width: 200 }}
                    placeholder="symbols"
                    optionFilterProp="children"
                    filterOption={(input, option) =>
                      option.children
                        .toLowerCase()
                        .indexOf(input.toLowerCase()) >= 0
                    }
                  >
                    <Option value="IDBI">IDBI</Option>
                    <Option value="SBI">SBI</Option>
                    <Option value="AXISBANK">AXISBANK</Option>
                  </Select>
                </Form.Item>

                <Form.Item
                  style={{ fontWeight: "bolder" }}
                  name="StrikePrice"
                  label="StrikePrice"
                  // rules={[{ required: true, message: "" }]}
                >
                  <Select
                    showSearch
                    disabled={
                      this.state.ex === "NSE" || this.state.ex === "BSE"
                        ? true
                        : false
                    }
                    style={{ width: 200 }}
                    placeholder="StrikePrice"
                    optionFilterProp="children"
                    filterOption={(input, option) =>
                      option.children
                        .toLowerCase()
                        .indexOf(input.toLowerCase()) >= 0
                    }
                  >
                    <Option value="IDBI">IDBI</Option>
                    <Option value="SBI">SBI</Option>
                    <Option value="AXISBANK">AXISBANK</Option>
                  </Select>
                </Form.Item>
              </Col>
            </Row>
          </Form>
        </Modal>
      </div>
    );
  }
}

export default SecondModel(ClassSecondModel);
