import React, { Component } from "react";
import { Form, InputNumber, Button } from "antd";
import { Row, Col, List } from "antd";
import { HomeOutlined } from "@ant-design/icons";
import { Breadcrumb, Input } from "antd";
import { Select, Divider } from "antd";
import { Steps, message } from "antd";
import { Card } from "antd";
import Grid from "@material-ui/core/Grid";
import Paper from "@material-ui/core/Paper";
import { Tag } from "antd";
import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableCell from "@material-ui/core/TableCell";
import TableContainer from "@material-ui/core/TableContainer";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import { Statistic } from "antd";
import { Modal } from "antd";
import { Switch, notification } from "antd";
import { TreeSelect } from "antd";
import { PlusOutlined } from "@ant-design/icons";
import { socket } from "../dashboard/Dashboard";
import axios from "axios";

// import Alert from "@material-ui/lab/Alert";
import { Alert } from "antd";

const { Step } = Steps;
const { TreeNode } = TreeSelect;

class Livetrade extends Component {
  constructor(props) {
    super(props);
    this.state = {
      capital: undefined,
      order: undefined,
      product: undefined,
      leverage: undefined,
      company: undefined,
      exchange: undefined,
      button: undefined,
      runstrategy: false,
      current: 0,
      setCurrent: 0,
      slot: 4,
      isModalVisible: false,
      auto: false,
      strategy: undefined,
      size: [],
      tradename: [],
      pnl: [],
      entryval: [],
      tradeltp: [],
      tradetoken: [],
      pcapital: 0,
      titles: ["Bank Sector", "IT sector"],
      ex: [
        ['"BANKBARODA"', '"HDFC"', '"HDFCBANK"', '"HDFCLIFE"'],
        ['"WIPRO"', '"LT"', '"TCS"', '"INFY"'],
      ],
      cat: "",
    };
  }
  componentDidMount() {
    socket.on("paper", (e) => this.handle("pcapital", e));
    socket.on("size", (e) => this.handle("size", e));
    socket.on("tradename", (e) => this.handle("tradename", e));
    socket.on("pnl", (e) => this.handle("pnl", e));
    socket.on("entryval", (e) => this.handle("entryval", e));
    socket.on("tradeltp", (e) => this.handle("tradeltp", e));
    socket.on("tradetoken", (e) => this.handle("tradetoken", e));
  }
  handle = (form, value) => {
    // console.log(this.state[`${form}`], value);
    this.setState({ [form]: value }, function () {
      // console.log(this.state[`${form}`]);
    });
  };

  // onExchangeChange = (value) => {
  //   console.log(`selected ${value}`);
  //   this.setState({ exchange: value });
  // };
  oncatChange = (value) => {
    this.setState({ cat: value });
  };
  onButtonChange = () => {
    console.log("button");
    this.setState({ button: "divide" });
  };
  onStrategyChange = () => {
    // console.log("button");
    this.setState({ runstrategy: "strategy" });
  };
  showModal = () => {
    this.setState({ isModalVisible: true });
  };
  handleOk = (values) => {
    console.log("ModalSuccess:", values);
    this.setState({ isModalVisible: false });
  };

  handleCancel = () => {
    this.setState({ isModalVisible: false });
  };

  onSwitchChange = (checked) => {
    console.log(`switch to ${checked}`);

    const close = () => {
      this.setState({ auto: true });
      console.log(
        "Notification was closed. Either the close button was clicked or duration time elapsed."
      );
    };

    if (checked == true) {
      const key = `open${Date.now()}`;
      const btn = (
        <Button
          type="primary"
          size="small"
          onClick={() => {
            this.setState({ auto: true });
            notification.close(key);
            console.log(`switch to ${checked}`);
          }}
        >
          Confirm
        </Button>
      );

      notification.open({
        // message: "Notification Title",
        description: (
          <Alert
            message="Warning"
            description="This is a warning notice about going Live"
            type="warning"
            showIcon
            // closable
          />
        ),
        btn,
        key,
        onClose: close,
      });
    }
  };

  render() {
    const { titles, ex } = this.state;
    const children1 = [];
    const { Option } = Select;
    for (let i = 10; i < 36; i++) {
      children1.push(
        <Option key={i.toString(36) + i}>{i.toString(36) + i}</Option>
      );
    }
    const steps = [
      {
        title: "First",
        content: "first",
      },
      {
        title: "Second",
        content: "Second-content",
      },
      {
        title: "Last",
        content: "Last-content",
      },
    ];
    function onBlur() {
      console.log("blur");
    }

    function onFocus() {
      console.log("focus");
    }

    function onSearch(val) {
      console.log("search:", val);
    }
    const children = [];
    const data = [];

    if (this.state.tradetoken.length >= this.state.slot) {
      console.log(this.state.tradetoken.length >= this.state.slot, "trade");
      for (let i = 1; i <= this.state.slot; i++) {
        children.push(i - 1);
        data.push({
          title: this.state.tradename[i],
          entry: this.state.entryval[i],
          size: this.state.size[i],
          ltp: this.state.tradeltp[i],
          pnl: this.state.pnl[i],
          tradetoken: this.state.tradetoken[i],
        });
      }
      console.log(data, "slot");
    }
    if (this.state.tradetoken.length < this.state.slot) {
      console.log(this.state.tradetoken.length >= this.state.slot, "trade");
      for (let i = 1; i <= this.state.tradetoken.length; i++) {
        children.push(i - 1);
        data.push({
          title: this.state.tradename[i],
          entry: this.state.entryval[i],
          size: this.state.size[i],
          ltp: this.state.tradeltp[i],
          pnl: this.state.pnl[i],
          tradetoken: this.state.tradetoken[i],
        });
      }
      for (
        let i = 1;
        i <= this.state.slot - this.state.tradetoken.length;
        i++
      ) {
        children.push(this.state.tradetoken.length + i - 1);
        data.push({
          title: i,
          entry: i,
          size: i,
          ltp: i,
          pnl: i,
          tradetoken: i,
        });
      }
      console.log(data, "slot");
    }
    function createData(date, symbol, amount, pnl) {
      return { date, symbol, amount, pnl };
    }
    const formdata = {
      strategy: this.state.strategy,
      leverage: this.state.leverage,
      slot: this.state.slot,
      exchange: this.state.exchange,
      Stocks: this.state.company,
      order: this.state.order,
      product: this.state.product,
      capital: this.state.capital,
    };
    const rows = [
      createData("21/07/2020", "NIFTI", 12000, 45.8),
      createData("21/07/2021", "NIFTI", 12000, 45.8),
      createData("21/07/2019", "NIFTI", 12000, 45.8),
      createData("21/07/2018", "NIFTI", 12000, 45.8),
      createData("22/07/2021", "NIFTI", 12000, 45.8),
    ];

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
    const onFinish = (values) => {
      console.log(values);
      message.success("Processing complete!");
    };
    // const onCapitalChange = (value) => {
    //   console.log("changed", value);
    // };
    // const onSlotChange = (value) => {
    //   this.setState({ slot: value });
    // };
    const onClick = () => {
      message.success("Processing complete!");
      this.setState({ runstrategy: true });
      let url = "http://127.0.0.1:8000/website/livetrade/";
      axios.post(url, formdata, {}).then((res) => {
        console.warn(res.data);
      });
    };

    const nfo = [
      '"ACC"',
      '"ADANIENT"',
      '"ADANIPORTS"',
      '"AMARAJABAT"',
      '"AMBUJACEM"',
      '"APOLLOHOSP"',
      '"APOLLOTYRE"',
      '"ASHOKLEY"',
      '"ASIANPAINT"',
      '"AUROPHARMA"',
      '"AXISBANK"',
      '"BAJAJ-AUTO"',
      '"BAJAJFINSV"',
      '"BAJFINANCE"',
      '"BALKRISIND"',
      '"BANDHANBNK"',
      '"BANKBARODA"',
      '"BATAINDIA"',
      '"BEL"',
      '"BERGEPAINT"',
      '"BHARATFORG"',
      '"BHARTIARTL"',
      '"BHEL"',
      '"BIOCON"',
      '"BOSCHLTD"',
      '"BPCL"',
      '"BRITANNIA"',
      '"CADILAHC"',
      '"CANBK"',
      '"CHOLAFIN"',
      '"CIPLA"',
      '"COALINDIA"',
      '"COFORGE"',
      '"COLPAL"',
      '"CONCOR"',
      '"CUMMINSIND"',
      '"DABUR"',
      '"DIVISLAB"',
      '"DLF"',
      '"DRREDDY"',
      '"EICHERMOT"',
      '"ESCORTS"',
      '"EXIDEIND"',
      '"FEDERALBNK"',
      '"GAIL"',
      '"GLENMARK"',
      '"GMRINFRA"',
      '"GODREJCP"',
      '"GODREJPROP"',
      '"GRASIM"',
      '"HAVELLS"',
      '"HCLTECH"',
      '"HDFC"',
      '"HDFCBANK"',
      '"HDFCLIFE"',
      '"HEROMOTOCO"',
      '"HINDALCO"',
      '"HINDPETRO"',
      '"HINDUNILVR"',
      '"IBULHSGFIN"',
      '"ICICIBANK"',
      '"ICICIGI"',
      '"ICICIPRULI"',
      '"IDEA"',
      '"IDFCFIRSTB"',
      '"IGL"',
      '"INDIGO"',
      '"INDUSINDBK"',
      '"INFRATEL"',
      '"INFY"',
      '"IOC"',
      '"ITC"',
      '"JINDALSTEL"',
      '"JSWSTEEL"',
      '"JUBLFOOD"',
      '"KOTAKBANK"',
      '"L&TFH"',
      '"LICHSGFIN"',
      '"LT"',
      '"LUPIN"',
      '"M&M"',
      '"M&MFIN"',
      '"MANAPPURAM"',
      '"MARICO"',
      '"MARUTI"',
      '"MCDOWELL-N"',
      '"MFSL"',
      '"MGL"',
      '"MINDTREE"',
      '"MOTHERSUMI"',
      '"MRF"',
      '"MUTHOOTFIN"',
      '"NATIONALUM"',
      '"NAUKRI"',
      '"NESTLEIND"',
      '"NMDC"',
      '"NTPC"',
      '"ONGC"',
      '"PAGEIND"',
      '"PEL"',
      '"PETRONET"',
      '"PFC"',
      '"PIDILITIND"',
      '"PNB"',
      '"POWERGRID"',
      '"PVR"',
      '"RAMCOCEM"',
      '"RBLBANK"',
      '"RECLTD"',
      '"RELIANCE"',
      '"SAIL"',
      '"SBILIFE"',
      '"SBIN"',
      '"SHREECEM"',
      '"SIEMENS"',
      '"SRF"',
      '"SRTRANSFIN"',
      '"SUNPHARMA"',
      '"SUNTV"',
      '"TATACHEM"',
      '"TATACONSUM"',
      '"TATAMOTORS"',
      '"TATAPOWER"',
      '"TATASTEEL"',
      '"TCS"',
      '"TECHM"',
      '"TITAN"',
      '"TORNTPHARM"',
      '"TORNTPOWER"',
      '"TVSMOTOR"',
      '"UBL"',
      '"ULTRACEMCO"',
      '"UPL"',
      '"VEDL"',
      '"VOLTAS"',
      '"WIPRO"',
      '"ZEEL"',
    ];

    const next = () => {
      this.setState({ current: this.state.current + 1 });
    };

    const prev = () => {
      this.setState({ current: this.state.current - 1 });
    };
    // const { Option } = Select;

    const onModalFinish = (values) => {
      console.log("ModalSuccess:", values);
      this.setState({ isModalVisible: false });
    };
    const onFormChange = (form, value) => {
      console.log(this.state[`${form}`], value);
      this.setState({ [form]: value }, function () {
        console.log(formdata);
      });
    };
    const layout = {
      labelCol: { span: 8 },
      wrapperCol: { span: 16 },
    };
    const tailLayout = {
      wrapperCol: { offset: 8, span: 16 },
    };
    const onModalFinish1 = (values) => {
      const { ex, titles } = this.state;
      this.setState({
        ex: [...ex, values.Tokens],
        titles: [...titles, values.name],
      });
      console.log("ModalSuccess:", values);
      this.setState({ isModalVisible: false });
    };

    const FirstData = (value) => {
      const { ex, titles } = this.state;
      // console.log("hello");
      if (value == 0) {
        return (
          <>
            <Divider />
            <Form.Item name={["user", "Strategy"]} label="Strategy">
              <Select
                showSearch
                style={{ width: 150 }}
                placeholder="Strategy"
                optionFilterProp="children"
                filterOption={(input, option) =>
                  option.children.toLowerCase().indexOf(input.toLowerCase()) >=
                  0
                }
                onChange={(e) => onFormChange("strategy", e)}
              >
                {["Strategy 1"].map((element) => {
                  return <Option value={element}> {element}</Option>;
                })}
              </Select>
            </Form.Item>
            <Divider />
          </>
        );
      }
      if (value == 1) {
        return (
          <div>
            <Divider />
            <Row>
              <Col span={12}>
                <Button style={{ backgroundColor: "#9ECB35" }} shape="round">
                  Set capital after
                </Button>
              </Col>
              <Col span={12}>
                <Button
                  style={{ backgroundColor: "#9ECB35" }}
                  onClick={this.onButtonChange}
                  shape="round"
                >
                  Divide the capital into slots
                </Button>
              </Col>
            </Row>
            <Divider />
            <Row>
              {this.state.button == "divide" && (
                <div>
                  <Form.Item
                    name={["user", "capital"]}
                    label="Capital"
                    // rules={[{ required: true }]}
                  >
                    <InputNumber
                      size="small"
                      min={1}
                      max={10000000}
                      onChange={(e) => onFormChange("capital", e)}
                    />
                  </Form.Item>

                  <Form.Item
                    name={["user", "leverage"]}
                    label="Leverage"
                    // rules={[{ required: true }]}
                  >
                    <Select
                      showSearch
                      style={{ width: 150 }}
                      placeholder="Leverage"
                      optionFilterProp="children"
                      filterOption={(input, option) =>
                        option.children
                          .toLowerCase()
                          .indexOf(input.toLowerCase()) >= 0
                      }
                      onChange={(e) => onFormChange("leverage", e)}
                    >
                      {["2", "3", "4"].map((element) => {
                        return <Option value={element}> {element}</Option>;
                      })}
                    </Select>
                  </Form.Item>
                  <Form.Item
                    name={["user", "slots"]}
                    label="slots"
                    // rules={[{ required: true }]}
                  >
                    <Select
                      showSearch
                      style={{ width: 150 }}
                      placeholder="Slots"
                      optionFilterProp="children"
                      onChange={(e) => onFormChange("slot", e)}
                    >
                      {["1", "2", "3", "4", "5"].map((element) => {
                        return <Option value={element}> {element}</Option>;
                      })}
                    </Select>
                  </Form.Item>
                </div>
              )}
            </Row>
          </div>
        );
      }
      if (value == 2) {
        return (
          <>
            <Divider />
            <Form.Item name="exchange" label="Exchange">
              <Select
                showSearch
                style={{ width: 150 }}
                placeholder="Exchange"
                optionFilterProp="children"
                onChange={(e) => onFormChange("exchange", e)}
                filterOption={(input, option) =>
                  option.children.toLowerCase().indexOf(input.toLowerCase()) >=
                  0
                }
              >
                {["NSE", "NFO"].map((element) => {
                  return <Option value={element}> {element}</Option>;
                })}
              </Select>
            </Form.Item>

            <Button
              style={{ color: "#9ECB35", float: "right" }}
              icon={<PlusOutlined style={{ color: "white" }} />}
              size="medium"
              shape="round"
              type="primary"
              onClick={this.showModal}
            ></Button>
            <Modal
              title="Add"
              visible={this.state.isModalVisible}
              onOk={this.handleOk}
              onCancel={this.handleCancel}
            >
              <Form name="basic" onFinish={onModalFinish1}>
                <Form.Item label="Name" name="name">
                  <Input placeholder="Enter the name" />
                </Form.Item>
                <Form.Item label="Tokens" name="Tokens">
                  <Select
                    showSearch
                    mode="multiple"
                    style={{ width: 200 }}
                    placeholder="Select Stocks"
                    optionFilterProp="children"
                    onChange={this.oncatChange}
                    onFocus={onFocus}
                    onBlur={onBlur}
                    onSearch={onSearch}
                    // filterOption={(input, option) =>
                    //   option.children
                    //     .toLowerCase()
                    //     .indexOf(input.toLowerCase()) >= 0
                    // }
                  >
                    {nfo.map((element) => {
                      return <Option value={element}> {element}</Option>;
                    })}
                  </Select>
                </Form.Item>

                <Form.Item {...tailLayout}>
                  <Button type="primary" htmlType="submit">
                    Submit
                  </Button>
                </Form.Item>
              </Form>
            </Modal>
            <Form.Item label="Stocks" name="Stocks">
              {this.state.exchange == "NSE" ? (
                <TreeSelect
                  showSearch
                  style={{ width: "60%" }}
                  treeDataSimpleMode={true}
                  // value={this.state.value}
                  dropdownStyle={{ maxHeight: 400, overflow: "auto" }}
                  placeholder="Please select"
                  allowClear
                  multiple
                  treeDefaultExpandAll
                  onChange={(e) => onFormChange("company", e)}
                  // onChange={this.ontreeChange}
                  // onSelect={this.ontreeSelect}
                >
                  {titles.map((element, idx) => {
                    return (
                      <TreeNode value={ex[idx]} title={element}>
                        {ex[idx].map((item) => {
                          return <TreeNode value={item} title={item} />;
                        })}
                      </TreeNode>
                    );
                  })}
                </TreeSelect>
              ) : (
                <Select
                  mode="tags"
                  style={{ width: "60%" }}
                  placeholder="Stocks"
                  onChange={(e) => onFormChange("company", e)}
                >
                  {children1}
                </Select>
              )}
            </Form.Item>
            <Form.Item
              name="OrderType"
              label="Order Type"
              // rules={[{ required: true }]}
            >
              <Select
                showSearch
                style={{ width: 150 }}
                placeholder="Order Type"
                optionFilterProp="children"
                onChange={(e) => onFormChange("order", e)}
              >
                {["market order", "limit order", "stopless order"].map(
                  (element) => {
                    return <Option value={element}> {element}</Option>;
                  }
                )}
              </Select>
            </Form.Item>

            <Form.Item
              name="product"
              label="Product"
              // rules={[{ required: true }]}
            >
              <Select
                showSearch
                style={{ width: 150 }}
                placeholder="Product"
                optionFilterProp="children"
                onChange={(e) => onFormChange("product", e)}
              >
                {["CNC", "MIS"].map((element) => {
                  return <Option value={element}> {element}</Option>;
                })}
              </Select>
            </Form.Item>
            <Form.Item
              name="golive"
              label="Go Live"
              // rules={[{ required: true }]}
            >
              <Switch onChange={this.onSwitchChange} />
            </Form.Item>
            <Divider />
          </>
        );
      }
    };

    return (
      <div>
        <Breadcrumb style={{ margin: "16px 0" }}>
          <Breadcrumb.Item href="">
            <HomeOutlined /> <span>Home</span>
          </Breadcrumb.Item>
          <Breadcrumb.Item>Deployment</Breadcrumb.Item>
          <Breadcrumb.Item>Livetrade</Breadcrumb.Item>
        </Breadcrumb>
        {/* <Row>
          <Col> */}
        {!this.state.runstrategy && (
          <Card hoverable style={{ width: 700 }}>
            <Steps current={this.state.current}>
              {steps.map((item) => (
                <Step key={item.title} title={item.title} />
              ))}
            </Steps>
            <Form
              name="nest-messages"
              onFinish={onFinish}
              validateMessages={validateMessages}
            >
              <div className="steps-content">
                {FirstData(this.state.current)}
              </div>
              <div className="steps-action">
                {this.state.current === steps.length - 1 && (
                  <Button
                    type="primary"
                    // htmlType="submit"
                    onClick={onClick}
                  >
                    Run Strategy
                  </Button>
                )}

                {this.state.current < steps.length - 1 &&
                  this.state.current == 0 && (
                    <Button type="primary" onClick={() => next()}>
                      Deploy Strategy
                    </Button>
                  )}
                {this.state.current < steps.length - 1 &&
                  this.state.current != 0 && (
                    <Button type="primary" onClick={() => next()}>
                      Next
                    </Button>
                  )}

                {this.state.current > 0 && (
                  <Button style={{ margin: "0 8px" }} onClick={() => prev()}>
                    Previous
                  </Button>
                )}
              </div>
            </Form>
          </Card>
        )}

        {this.state.runstrategy == true && (
          <>
            {/* <Card hoverable style={{ width: 1200 }}> */}
            <Row>
              <Col span={6}>
                <Card hoverable>
                  <Statistic
                    title="Capital"
                    value={this.state.capital}
                    valueStyle={{ color: "#3f8600" }}
                  />
                </Card>
              </Col>
              <Col span={6}>
                <Card hoverable>
                  <Statistic
                    title="Strategy"
                    value={this.state.strategy}
                    precision={"running"}
                    valueStyle={{ color: "#3f8600" }}
                  />
                </Card>
              </Col>
              <Col span={6}>
                <Card hoverable>
                  <Statistic
                    title="Leverage"
                    value={this.state.leverage}
                    valueStyle={{ color: "#3f8600" }}
                  />
                </Card>
              </Col>
              <Col span={6}>
                <Card hoverable>
                  <Statistic
                    title="Slots"
                    value={this.state.slot}
                    valueStyle={{ color: "#3f8600" }}
                  />
                </Card>
              </Col>
            </Row>
            {/* </Card> */}
            <Divider />
            <Row>
              <Col span={16}>
                <Grid container spacing={2}>
                  <Grid item xs={12}>
                    <Grid container justify="center" spacing={2}>
                      {children.map((value) => (
                        <Grid key={value} item>
                          <Card
                            hoverable
                            style={{ width: 200 }}
                            title={data[value].title}
                          >
                            <List>
                              <List.Item>
                                <Tag color="#2db7f5" style={{ width: 80 }}>
                                  LTP :
                                </Tag>
                                {data[value].ltp}
                              </List.Item>
                              <List.Item>
                                <Tag color="#87d068" style={{ width: 80 }}>
                                  LotSize :
                                </Tag>
                                {data[value].size}
                              </List.Item>
                              <List.Item>
                                <Tag color="#108ee9" style={{ width: 80 }}>
                                  EntryValue :
                                </Tag>
                                {data[value].entry}
                              </List.Item>
                              <List.Item>
                                <Tag color="gold" style={{ width: 80 }}>
                                  Profit/loss :
                                </Tag>
                                {data[value].pnl}
                              </List.Item>
                              <List.Item>
                                <Tag color="purple" style={{ width: 80 }}>
                                  Token :
                                </Tag>
                                {data[value].tradetoken}
                              </List.Item>
                            </List>
                            <div>
                              <Button
                                size="medium"
                                type="primary"
                                onClick={this.showModal}
                                disabled={
                                  this.state.auto == true ? true : false
                                }
                              >
                                Place Order
                              </Button>
                            </div>
                          </Card>
                          <Paper />
                        </Grid>
                      ))}
                    </Grid>
                  </Grid>
                </Grid>

                <Modal
                  title="Place order"
                  visible={this.state.isModalVisible}
                  onOk={this.handleOk}
                  onCancel={this.handleCancel}
                >
                  <Form name="basic" onFinish={onModalFinish}>
                    <Form.Item
                      name="OrderType"
                      label="Order Type"
                      rules={[{ required: true }]}
                    >
                      <Select
                        showSearch
                        style={{ width: 150 }}
                        placeholder="Order Type"
                        optionFilterProp="children"
                      >
                        {["market order", "limit order", "stopless order"].map(
                          (element) => {
                            return <Option value={element}> {element}</Option>;
                          }
                        )}
                      </Select>
                    </Form.Item>

                    <Form.Item
                      name="product"
                      label="Product"
                      rules={[{ required: true }]}
                    >
                      <Select
                        showSearch
                        style={{ width: 150 }}
                        placeholder="Product"
                        optionFilterProp="children"
                      >
                        {["CNC", "MIS"].map((element) => {
                          return <Option value={element}> {element}</Option>;
                        })}
                      </Select>
                    </Form.Item>
                  </Form>
                </Modal>
              </Col>
              <Col span={8}>
                <TableContainer component={Paper}>
                  <Table aria-label="simple table">
                    <TableHead>
                      <TableRow>
                        <TableCell>Date</TableCell>
                        <TableCell align="right">Symbol</TableCell>
                        <TableCell align="right">amount</TableCell>
                        <TableCell align="right">PNL</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {rows.map((row) => (
                        <TableRow key={row.date}>
                          <TableCell component="th" scope="row">
                            {row.date}
                          </TableCell>
                          <TableCell align="right">{row.symbol}</TableCell>
                          <TableCell align="right">{row.amount}</TableCell>
                          <TableCell align="right">{row.pnl}</TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              </Col>
            </Row>
          </>
        )}
        {/* </Col>
        </Row> */}
      </div>
    );
  }
}

export default Livetrade;
