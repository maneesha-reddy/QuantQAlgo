import React, { Component } from "react";
// import Select from '@material-ui/core/Select';
import TextField from "@material-ui/core/TextField";
import "./Backlist.css";
import { DatePicker, Radio, Space } from "antd";
import { Select } from "antd";
import { Row, Col } from "antd";
import { Modal, Button } from "antd";
import { PlusOutlined, EditOutlined } from "@ant-design/icons";
// import FirstModel from "./FirstModel";
import SecondModel from "./SecondModel";
import Result from "./Result";
// import Edit from "./Edit";
import axios from "axios";
import { Input, Form } from "antd";
import { Card } from "antd";
import { Layout, Menu, Breadcrumb } from "antd";
// import HomeFilled from "@ant-design/icons";
import { HomeOutlined} from '@ant-design/icons';
// import TextField from "@material-ui/core/TextField";
const { Option } = Select;
class Backlist extends Component {
  constructor(props) {
    super(props);
    this.state = {
      stocks: {},
      results: {},
      size: "default",
      operation: undefined,
      Date: undefined,
      modal2Visible: false,
      activeName: null,
      spinner: true,
      table: false,
      resultTable: false,
      width:1000,
    };
    this.handleModalValues = this.handleModalValues.bind(this);
    this.handleWidth = this.handleWidth.bind(this);
    this.setModal2Visible = this.setModal2Visible.bind(this);
    // this.onFinish = this.onFinish(this);
  }

  setModal2Visible(isVisible, op) {
    this.setState({ modal2Visible: isVisible, operation: op });
  }
  handleWidth = () => {
    this.setState({ width: 1000 });
  };
  showModal = () => {
    this.setState({
      resultTable: true,
    });
  };

  handleOk = (e) => {
    console.log(e);
    this.setState({
      resultTable: false,
    });
  };

  handleCancel = (e) => {
    console.log(e);
    this.setState({
      resultTable: false,
    });
  };

  handleDateChange = (event) => {
    console.log("hi");
    console.log(event);
    this.setState({ Date: event });
  };
  handleModalValues(values) {
    console.log(values);
    if (values.name != undefined) {
      this.setState(
        (prevState) => {
          return {
            ...prevState,

            stocks: {
              ...prevState.stocks,
              [values.name]: {
                name: values.name,
                exchange: values.exchange,
                symbols: values.symbols,
                StrikePrice: values.StrikePrice,
                segment: values.segment,
              },
            },
          };
        },
        function () {
          console.log(this.state.stocks);
        }
      );
    } else {
      this.setState(
        (prevState) => {
          return {
            ...prevState,

            stocks: {
              ...prevState.stocks,
              [values.symbols]: {
                name: values.name,
                exchange: values.exchange,
                symbols: values.symbols,
                StrikePrice: values.StrikePrice,
                segment: values.segment,
              },
            },
          };
        },
        function () {
          console.log(this.state.stocks);
        }
      );
    }
  }
  handleName = (e) => {
    console.log(e);
    this.setState({ activeName: e });
  };

  onFinish = (values) => {
    // console.log("hiiiiiiii");
    this.setState({ table: true });
    console.log(values);
    console.log(this.state.stocks[this.state.activeName]);
    console.log(this.state.activeName);
    const data = new FormData();
    data.append("symbol", this.state.stocks[this.state.activeName]["symbols"]);
    data.append("from_date", values.FromDate);
    data.append("to_date", values.ToDate);
    data.append("Quantity", values.Quantity);
    data.append("Initial_Capital", values.Initial_Capital);
    // data.append("Time_frame", values.Time_frame);
    for (var key of data.entries()) {
      console.log(key[0] + ", " + key[1]);
    }
    let url = "http://127.0.0.1:8000/create/";
    axios.post(url, data, {}).then((res) => {
      console.warn(res.data);
      // console.warn(res.data);
      this.setState({ spinner: false });
      this.setState((prevState) => {
        return {
          ...prevState,
          results: {
            ...prevState.results,
            hello: {
              Trade_start_date: res.data["output"]["Trade start date"],
              Trade_end_date: res.data["output"]["Trade end date"],
              Initial_Capital: res.data["output"]["Initial_Capital"],
              Ending_Capital: res.data["output"]["Ending_Capital"],
              Total_no_trades: res.data["output"]["Total no trades"],
              Positive_trades: res.data["output"]["Positive_trades"],
              Negative_trades: res.data["output"]["Negative_trades"],
              Total_loss: res.data["output"]["Total_loss"],
              Net_Profit: res.data["output"]["Net Profit"],
              Sharpe_ratio: res.data["output"]["Sharpe ratio"],
              CAGR: res.data["output"]["CAGR (%)"],
              Maximum_Drawdown: res.data["output"]["Maximum Drawdown (%)"],
              Entry:res.data["trade"]["Entry"],
              Date:res.data["trade"]["Date"],
              Price:res.data["trade"]["Price"],
              Exit:res.data["trade"]["Exit"],
              ExDate:res.data["trade"]["ExDate"],
              ExPrice:res.data["trade"]["ExPrice"],
              change:res.data["trade"]["% Change"],
              Profit:res.data["trade"]["Profit"],
              perprofit:res.data["trade"]["% Profit"],
              position_value:res.data["trade"]["Position value"],
              cumm_profit:res.data["trade"]["Cumm Profit"],
              MAE:res.data["trade"]["MAE"],
              MFE:res.data["trade"]["MFE"],
              SS:res.data["trade"]["Scale In / Scale Out"]
            },
          },
        };
      });

      console.log(this.state.spinner);
    });
    // axios.get("http://127.0.0.1:8000/create/").then((res) => {
    //   console.log(res.data);
    // });
  };

  render() {
    const layout = {
      labelCol: { span: 8 },
      wrapperCol: { span: 16 },
    };
    const tailLayout = {
      wrapperCol: { offset: 8, span: 16 },
    };
    const { size } = this.state.size;
    return (
      
      // <div id="border" style={{ backgroundColor: "white", paddingLeft: 100 }} backgroundColor:"#EDFBED">
      <div>
      <Breadcrumb style={{ margin: "16px 0" }}>
        <Breadcrumb.Item href=""><HomeOutlined /> <span>Home</span></Breadcrumb.Item>
        <Breadcrumb.Item>Deployment</Breadcrumb.Item>
        <Breadcrumb.Item>BackTest</Breadcrumb.Item>
      </Breadcrumb>
      <Row justify={"center"}>
        <Col>
          <Card
            hoverable
            // title="BackTesting"
            style={{ width: 700 }}
          >
            <div>
              <Button
                style={{ color: "#9ECB35", float: "right" }}
                icon={<PlusOutlined style={{ color: "white" }} />}
                size="medium"
                shape="round"
                type="primary"
                // style={{ marginLeft: 20 }}
                onClick={() => this.setModal2Visible(true, "add")}
              ></Button>
              <Button
                style={{ color: "#9ECB35", float: "right" }}
                icon={<EditOutlined />}
                size="medium"
                shape="round"
                disabled={
                  Object.keys(this.state.stocks).length >= 1 &&
                  this.state.activeName != null
                    ? false
                    : true
                }
                type="primary"
                onClick={() => {
                  this.setModal2Visible(true, "edit");
                }}
              ></Button>
            </div>
            <br />
            <br />
            <Form
              {...layout}
              onFinish={this.onFinish}
              style={{ justifyContent: "left" }}
            >
              {/* <Col span={12}> */}
              {/* <Row>
                <Col span={20}> */}
              <Form.Item name="name" rules={[{ required: true }]} label="Name">
                {/* <Row gutter={8}>
                  <Col span={15}> */}

                <Select
                  showSearch
                  // bordered={false}
                  style={{ width: 300 }}
                  placeholder="Name"
                  optionFilterProp="children"
                  onChange={this.handleName}
                  filterOption={(input, option) =>
                    option.children
                      .toLowerCase()
                      .indexOf(input.toLowerCase()) >= 0
                  }
                >
                  {Object.entries(this.state.stocks).map(([key, item]) => {
                    // console.log(item.name, "eorkgj");
                    return (
                      <Option key={key} value={key}>
                        {key}
                      </Option>
                    );
                  })}
                </Select>
              </Form.Item>
              {/* </Col> */}

              {/* <Col span={4}> */}

              {/* </Col>
              </Row> */}

              <SecondModel
                autofill={
                  this.state.operation === "edit"
                    ? this.state.stocks[this.state.activeName]
                    : null
                }
                operation={this.state.operation}
                handleModalValues={this.handleModalValues}
                isVisible={this.state.modal2Visible}
                setModal2Visible={this.setModal2Visible}
              />

              <Form.Item
                style={{ fontWeight: "bolder" }}
                name="Strategy"
                label="Strategy"
                rules={[{ required: true, message: "" }]}
              >
                <Select
                  showSearch
                  style={{ width: 300 }}
                  placeholder="Strategy"
                  optionFilterProp="children"
                  filterOption={(input, option) =>
                    option.children
                      .toLowerCase()
                      .indexOf(input.toLowerCase()) >= 0
                  }
                >
                  {["1", "2", "3"].map((element) => {
                    return <Option value={element}> {element}</Option>;
                  })}
                </Select>
              </Form.Item>

              <Form.Item
                name="Quantity"
                rules={[{ required: true }]}
                label="Quantity"
              >
                <TextField
                  style={{ width: 300 }}
                  id="outlined-basic"
                  label="Enter Quantity"
                  variant="outlined"
                  size="small"
                />
              </Form.Item>
              {/* </Col> */}
              {/* <Col span={12}> */}
              <Form.Item
                name="Initial_Capital"
                rules={[{ required: true }]}
                label="Initial Capital"
              >
                <TextField
                  style={{ width: 300 }}
                  id="outlined-basic"
                  label="Initial Capital"
                  variant="outlined"
                  size="small"
                />
              </Form.Item>
              <Form.Item
                style={{ fontWeight: "bolder" }}
                name="Time_frame"
                label="Time_frame"
                rules={[{ required: true, message: "" }]}
              >
                <Select
                  showSearch
                  style={{ width: 300 }}
                  placeholder="Time_frame"
                  optionFilterProp="children"
                  filterOption={(input, option) =>
                    option.children
                      .toLowerCase()
                      .indexOf(input.toLowerCase()) >= 0
                  }
                >
                  {[
                    "1min",
                    "5min",
                    "10min",
                    "15min",
                    "30min",
                    "1hour",
                    "4hours",
                    "1day",
                    "1 week",
                  ].map((element) => {
                    return <Option value={element}> {element}</Option>;
                  })}
                </Select>
              </Form.Item>
              <Form.Item
                name="FromDate"
                rules={[{ required: true }]}
                label="From"
              >
                <TextField
                  style={{ width: 300 }}
                  id="datetime-local"
                  type="datetime-local"
                  defaultValue=""
                  InputLabelProps={{
                    shrink: true,
                  }}
                />
              </Form.Item>
              <Form.Item name="ToDate" rules={[{ required: true }]} label="To">
                <TextField
                  style={{ width: 300 }}
                  id="datetime-local-2"
                  type="datetime-local"
                  defaultValue=""
                  InputLabelProps={{
                    shrink: true,
                  }}
                />
              </Form.Item>
              <Form.Item {...tailLayout}>
                <Button
                  type="primary"
                  htmlType="submit"
                  ghost="true"
                  onClick={this.showModal}
                >
                  BackTest
                </Button>
                {/* <Button type="primary" onClick={this.showModal}>
                  Open Modal
                </Button> */}
                <Modal
                  title="Basic Modal"
                  width={this.state.width}
                  visible={this.state.resultTable}
                  onOk={this.handleOk}
                  onCancel={this.handleCancel}
                >
                  {this.state.table == true && (
                    <Result
                      results={this.state.results["hello"]}
                      props={this.state.spinner}
                      handleWidth={this.handleWidth}
                    />
                  )}
                </Modal>
              </Form.Item>
            </Form>
          </Card>
        </Col>
      </Row>
      </div>
    );
  }
}

export default Backlist;
