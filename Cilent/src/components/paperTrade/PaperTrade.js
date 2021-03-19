import React, { Component } from "react";
import { HomeOutlined } from "@ant-design/icons";
import { Breadcrumb } from "antd";
import { Statistic, Slider, InputNumber, Row, Col, Card } from "antd";
import { ArrowUpOutlined, ArrowDownOutlined } from "@ant-design/icons";
import { PlusOutlined, EditOutlined } from "@ant-design/icons";
import { Input } from "antd";
// import {Select } from '@material-ui/core/Select';
// import Select  from '@material-ui/core/Select';
import { Select } from "antd";
import { Form, Button } from "antd";
import "./PaperTrade.css";
import { List, Typography, Divider } from "antd";
import axios from "axios";
import { socket } from "../dashboard/Dashboard";
import { Tag } from "antd";
import TextField from "@material-ui/core/TextField";
import { Modal } from "antd";
// import Divider from "@material-ui/core/Divider";
import Grid from "@material-ui/core/Grid";
import { TreeSelect } from "antd";

const { TreeNode } = TreeSelect;

console.log(socket, "socket-123");

// const { Option } = Select;

class PaperTrade extends Component {
  constructor(props) {
    super(props);
    this.state = {
      inputValue: 0,
      capital: 0,
      size: [],
      tradename: [],
      pnl: [],
      entryval: [],
      tradeltp: [],
      tradetoken: [],
      paper: false,
      exchange: "",
      bankstocks: ["BANKBARODA", "IDBI", "SBI", "AXISBANK"],
      it: ["WIPRO", "L&T", "TCS", "INFOSYS"],
      titles: ["Bank Sector", "IT sector"],
      ex: [
        ['"BANKBARODA"', '"HDFC"', '"HDFCBANK"', '"HDFCLIFE"'],
        ['"WIPRO"', '"LT"', '"TCS"', '"INFY"'],
      ],
      cat: "",
      isModalVisible: false,
      value: undefined,
    };
  }
  componentDidMount() {
    socket.on("paper", this.handlecapital);
    socket.on("size", this.handlesize);
    socket.on("tradename", this.handletradename);
    socket.on("pnl", this.handlepnl);
    socket.on("entryval", this.handleentryval);
    socket.on("tradeltp", this.handletradeltp);
    socket.on("tradetoken", this.handletradetoken);
  }

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
  handlecapital = (msg) => {
    this.setState({ capital: msg });
  };
  handlesize = (msg) => {
    this.setState({ size: msg });
  };
  handletradename = (msg) => {
    this.setState({ tradename: msg });
  };
  handlepnl = (msg) => {
    this.setState({ pnl: msg });
  };
  handleentryval = (msg) => {
    this.setState({ entryval: msg });
  };
  handletradeltp = (msg) => {
    this.setState({ tradeltp: msg });
  };
  handletradetoken = (msg) => {
    this.setState({ tradetoken: msg });
  };
  onCapitalChange = (value) => {
    if (isNaN(value)) {
      return;
    }
    this.setState({
      inputValue: value,
    });
  };

  onChange = (value) => {
    console.log(`selected ${value}`);
    this.setState({ exchange: value });
  };
  oncatChange = (value) => {
    this.setState({ cat: value });
  };

  ontreeChange = (value) => {
    console.log(value, "tree");
    this.setState({ value });
  };
  ontreeSelect = (value) => {
    console.log(value, "treeselect");
    // this.setState({ value });
  };
  render() {
    const { inputValue, bankstocks, it, titles, ex } = this.state;
    const { Option } = Select;
    const children = [];
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
    for (let i = 10; i < 36; i++) {
      children.push(
        <Option key={i.toString(36) + i}>{i.toString(36) + i}</Option>
      );
    }

    const children1 = [];
    for (let i = 0; i < 138; i++) {
      children1.push(<Option key={nfo[i]}>{nfo[i]}</Option>);
    }

    function handleChange(value) {
      console.log(`selected ${value}`);
    }
    const bank = [];
    for (let i = 0; i < bankstocks.length; i++) {
      bank.push(<Option key={bankstocks[i]}>{bankstocks[i]}</Option>);
    }

    const IT = [];
    const child = [0, 1, 2, 3];
    for (let i = 0; i < it.length; i++) {
      IT.push(<Option key={it[i]}>{it[i]}</Option>);
    }

    function onBlur() {
      console.log("blur");
    }

    function onFocus() {
      console.log("focus");
    }

    function onSearch(val) {
      console.log("search:", val);
    }
    const data = [
      {
        title: this.state.tradename[0],
        entry: this.state.entryval[0],
        size: this.state.size[0],
        ltp: this.state.tradeltp[0],
        pnl: this.state.pnl[0],
        tradetoken: this.state.tradetoken[0],
      },
      {
        title: this.state.tradename[1],
        entry: this.state.entryval[1],
        size: this.state.size[1],
        ltp: this.state.tradeltp[1],
        pnl: this.state.pnl[1],
        tradetoken: this.state.tradetoken[1],
      },
      {
        title: this.state.tradename[2],
        entry: this.state.entryval[2],
        size: this.state.size[2],
        ltp: this.state.tradeltp[2],
        pnl: this.state.pnl[2],
        tradetoken: this.state.tradetoken[2],
      },
      {
        title: this.state.tradename[3],
        entry: this.state.entryval[3],
        size: this.state.size[3],
        ltp: this.state.tradeltp[3],
        pnl: this.state.pnl[3],
        tradetoken: this.state.tradetoken[3],
      },
    ];

    const onFinish = (values) => {
      console.log("Success:", values);
      this.setState({ paper: true });
      let url = "https://quantqalgo.ddns.net/website/papertrade/";

      // let url = "http://127.0.0.1:8000/website/papertrade/";
      axios.post(url, values, {}).then((res) => {
        console.warn(res.data);
      });
    };
    const onModalFinish = (values) => {
      const { ex, titles } = this.state;
      this.setState({
        ex: [...ex, values.Tokens],
        titles: [...titles, values.name],
      });
      console.log("ModalSuccess:", values);
      this.setState({ isModalVisible: false });
    };

    const onFinishFailed = (errorInfo) => {
      console.log("Failed:", errorInfo);
    };

    const layout = {
      labelCol: { span: 8 },
      wrapperCol: { span: 16 },
    };
    const tailLayout = {
      wrapperCol: { offset: 8, span: 16 },
    };
    return (
      <div>
        <Breadcrumb style={{ margin: "16px 0" }}>
          <Breadcrumb.Item href="">
            <HomeOutlined /> <span>Home</span>
          </Breadcrumb.Item>
          <Breadcrumb.Item>Deployment</Breadcrumb.Item>
          <Breadcrumb.Item>PaperTrade</Breadcrumb.Item>
        </Breadcrumb>
        <Row justify="center">
          {/* <Col span={12}> */}
          <Card
            hoverable
            // title="BackTesting"
            style={{ width: 700 }}
            bordered={false}
          >
            <Form {...layout} name="basic" onFinish={onFinish}>
              <Row>
                <Col span={18}>
                  <Form.Item label="Capital" name="capital">
                    <Slider
                      style={{ left: "0%", right: "auto", width: "92.7%" }}
                      //  color="#ff9933"
                      min={0}
                      max={100000}
                      onChange={this.onCapitalChange}
                      value={typeof inputValue === "number" ? inputValue : 0}
                      step={100}
                    />
                  </Form.Item>
                </Col>
                <Col span={4}>
                  <InputNumber
                    min={0}
                    max={100000}
                    style={{ margin: "0 16px" }}
                    step={100}
                    value={inputValue}
                    onChange={this.onChange}
                  />
                </Col>
              </Row>
              <Form.Item
                // style={{ fontWeight: "bolder" }}
                name="Strategy"
                label="Strategy"
                // rules={[{ required: true, message: "" }]}
              >
                <Select
                  showSearch
                  style={{ width: 150 }}
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
                // rules={[{ required: true }]}
                label="Quantity"
              >
                <TextField
                  // style={{ width: 300 }}
                  id="outlined-basic"
                  label="Enter Quantity"
                  variant="outlined"
                  size="small"
                />
              </Form.Item>
              <Form.Item
                // style={{ fontWeight: "bolder" }}
                name="Time_frame"
                label="Time frame"
                // rules={[{ required: true, message: "" }]}
              >
                <Select
                  showSearch
                  style={{ width: 300 }}
                  placeholder="Time frame"
                  optionFilterProp="children"
                  // filterOption={(input, option) =>
                  //   option.children
                  //     .toLowerCase()
                  //     .indexOf(input.toLowerCase()) >= 0
                  // }
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

              <Form.Item label="exchange" name="Exchange">
                <Select
                  showSearch
                  style={{ width: 200 }}
                  placeholder="Select Exchange"
                  optionFilterProp="children"
                  onChange={this.onChange}
                  onFocus={onFocus}
                  onBlur={onBlur}
                  onSearch={onSearch}
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
                </Select>
              </Form.Item>
              {/* <Form.Item
          label="Categories"
          name="Categories"
          >

          <Select
              showSearch
              style={{ width: 200 }}
              placeholder="Select Exchange"
              optionFilterProp="children"
              onChange={this.oncatChange}
              onFocus={onFocus}
              onBlur={onBlur}
              onSearch={onSearch}
              filterOption={(input, option) =>
                option.children.toLowerCase().indexOf(input.toLowerCase()) >= 0
              }
            > 
              {titles.map((element) => {
                    return <Option value={element}> {element}</Option>;
                  })}
          </Select>

          </Form.Item> */}
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
                <Form name="basic" onFinish={onModalFinish}>
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
                      filterOption={(input, option) =>
                        option.children
                          .toLowerCase()
                          .indexOf(input.toLowerCase()) >= 0
                      }
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
                    value={this.state.value}
                    dropdownStyle={{ maxHeight: 400, overflow: "auto" }}
                    placeholder="Please select"
                    allowClear
                    multiple
                    treeDefaultExpandAll
                    onChange={this.ontreeChange}
                    onSelect={this.ontreeSelect}
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
                    onChange={handleChange}
                  >
                    {children}
                  </Select>
                )}
              </Form.Item>

              <Form.Item {...tailLayout}>
                <Button type="primary" htmlType="submit">
                  PaperTrade
                </Button>
              </Form.Item>
            </Form>
          </Card>
        </Row>
        <br />
        {this.state.paper && (
          <>
            <Row justify="center">
              <Col span={4}>
                <Card>
                  <Statistic
                    title="Profit/Loss"
                    value={0}
                    // precision={2}
                    valueStyle={{ color: "#3f8600" }}
                    prefix={<ArrowUpOutlined />}
                    suffix="%"
                  />
                </Card>
              </Col>
              <Col span={4} offset={2}>
                <Card>
                  <Statistic
                    title="Capital"
                    value={this.state.capital}
                    // precision={2}
                    valueStyle={{ color: "#3f8600" }}
                    // prefix={<ArrowUpOutlined />}
                    // suffix="%"
                  />
                </Card>
              </Col>
            </Row>
            <Divider />
            <Row justify="center">
              <Col span={16}>
                <Grid container spacing={2}>
                  <Grid item xs={12}>
                    <Grid container justify="center" spacing={2}>
                      {child.map((value) => (
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
                          </Card>
                        </Grid>
                      ))}
                    </Grid>
                  </Grid>
                </Grid>
              </Col>
              <Col span={8}>
                <Card title="History" style={{ width: 200 }}></Card>
              </Col>
            </Row>
          </>
        )}

        {/* </Row> */}
      </div>
    );
  }
}
export default PaperTrade;
