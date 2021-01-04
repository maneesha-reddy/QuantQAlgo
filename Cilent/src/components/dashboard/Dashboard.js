import React, { Component } from "react";
import axios from "axios";
import io from "socket.io-client";
import Graph from "./graph";
import TopTable from "./toptable";
import { Statistic, Card, Row, Col } from "antd";
import { ArrowUpOutlined, ArrowDownOutlined } from "@ant-design/icons";
import { Layout, Menu, Breadcrumb } from "antd";
import { HomeOutlined } from "@ant-design/icons";
// export const socket=io('http://localhost:8000', {transports: ['websocket']});
export const socket = io("http://18.220.64.132:8000", {
  transports: ["websocket"],
});
class DashBoard extends Component {
  constructor(props) {
    super(props);
    this.state = {
      lablesnifti: [],
      datanifti: [],
      nltp: [],
      lablessensex: [],
      datasensex: [],
      sltp: [],
      lablesbank: [],
      databank: [],
      bltp: [],
      lablesindia: [],
      dataindia: [],
      iltp: [],
      loosersName: [],
      gainersName: [],
      loosersltp: [],
      gainersltp: [],
    };
  }
  componentDidMount() {
    const socket = io("http://18.220.64.132:8000", {
      transports: ["websocket"],
    });
    console.log(socket, "socket");
    socket.on("niftidata", this.handleniftiData);
    socket.on("niftitime", this.handleniftiLabel);
    socket.on("nltp", this.handleniftiltp);

    socket.on("sensexdata", this.handlesensexData);
    socket.on("sensextime", this.handlesensexLabel);
    socket.on("sltp", this.handlesensexltp);

    socket.on("bankdata", this.handlebankData);
    socket.on("banktime", this.handlebankLabel);
    socket.on("bltp", this.handlebankltp);

    socket.on("indiadata", this.handleindiaData);
    socket.on("indiatime", this.handleindiaLabel);
    socket.on("iltp", this.handleindialtp);

    socket.on("loosers", this.handleloosers);
    socket.on("gainers", this.handlegainers);
    socket.on("loosersltp", this.handleloosersltp);
    socket.on("gainersltp", this.handlegainersltp);

    socket.on("connect", () => {
      console.log("connected");
    });
    socket.on("disconnect", () => {
      console.log(socket.connected);
    });
  }
  handleniftiData = (msg) => {
    this.setState({ datanifti: msg });
  };
  handleniftiLabel = (msg) => {
    this.setState({ lablesnifti: msg });
  };
  handleniftiltp = (msg) => {
    // console.log(msg);
    this.setState({ nltp: msg });
  };

  handlesensexData = (msg) => {
    this.setState({ datasensex: msg });
  };
  handlesensexLabel = (msg) => {
    this.setState({ lablessensex: msg });
  };
  handlesensexltp = (msg) => {
    // console.log(msg);
    this.setState({ sltp: msg });
  };

  handlebankData = (msg) => {
    this.setState({ databank: msg });
  };
  handlebankLabel = (msg) => {
    this.setState({ lablesbank: msg });
  };
  handlebankltp = (msg) => {
    // console.log(msg);
    this.setState({ bltp: msg });
  };

  handleindiaData = (msg) => {
    this.setState({ dataindia: msg });
  };
  handleindiaLabel = (msg) => {
    this.setState({ lablesindia: msg });
  };
  handleindialtp = (msg) => {
    // console.log(msg);
    this.setState({ iltp: msg });
  };
  handlegainers = (msg) => {
    this.setState({ gainers: msg });
  };
  handleloosers = (msg) => {
    this.setState({ loosers: msg });
  };
  handlegainersltp = (msg) => {
    // console.log("gainers",msg)
    this.setState({ gainersltp: msg });
  };
  handleloosersltp = (msg) => {
    this.setState({ loosersltp: msg });
  };

  render() {
    return (
      <div>
        <Breadcrumb style={{ margin: "16px 0" }}>
          <Breadcrumb.Item href="">
            <HomeOutlined /> <span>Home</span>
          </Breadcrumb.Item>
          <Breadcrumb.Item>Dashboard</Breadcrumb.Item>
        </Breadcrumb>
        <Row gutter={16}>
          <Col span={6}>
            {/* <Card style={{ width: "45vh",height:"35vh" }}> */}
            <Statistic
              title="NIFTI 50"
              value={this.state.nltp[0]}
              valueStyle={{ color: "#3f8600" }}
              // prefix={<ArrowUpOutlined />}
            />
            {this.state.nltp[1] > 0 ? (
              <Statistic
                value={this.state.nltp[1]}
                precision={2}
                valueStyle={{ color: "#006600" }}
                suffix="%"
                prefix={<ArrowUpOutlined />}
              />
            ) : (
              <Statistic
                value={this.state.nltp[1]}
                precision={2}
                valueStyle={{ color: "#cf1322" }}
                suffix="%"
                prefix={<ArrowDownOutlined />}
              />
            )}

            <Graph
              labels={this.state.lablesnifti}
              data={this.state.datanifti}
              title="nifti"
              grad="#3399ff"
              border="#4d94ff"
            />
            {/* </Card> */}
          </Col>
          <Col span={6}>
            {/* <Card style={{ width: "45vh",height:"35vh" }}> */}

            <Statistic
              title="SENSEX"
              value={this.state.sltp[0]}
              valueStyle={{ color: "#3f8600" }}
              // prefix={<ArrowUpOutlined />}
              // suffix="%"
            />
            {this.state.sltp[1] > 0 ? (
              <Statistic
                value={this.state.sltp[1]}
                precision={2}
                valueStyle={{ color: "#006600" }}
                suffix="%"
                prefix={<ArrowUpOutlined />}
              />
            ) : (
              <Statistic
                value={this.state.sltp[1]}
                precision={2}
                valueStyle={{ color: "#cf1322" }}
                suffix="%"
                prefix={<ArrowDownOutlined />}
              />
            )}
            <Graph
              labels={this.state.lablessensex}
              data={this.state.datasensex}
              title="sensex"
              grad="#99e699"
              border="#29a329"
            />
            {/* </Card> */}
          </Col>
          <Col span={6}>
            {/* <Card style={{ width: "45vh",height:"35vh" }}> */}
            <Statistic
              title="NIFTY Bank"
              value={this.state.bltp[0]}
              valueStyle={{ color: "#3f8600" }}
              // prefix={<ArrowUpOutlined />}
              // suffix="%"
            />
            {this.state.bltp[1] > 0 ? (
              <Statistic
                value={this.state.bltp[1]}
                precision={2}
                valueStyle={{ color: "#006600" }}
                suffix="%"
                prefix={<ArrowUpOutlined />}
              />
            ) : (
              <Statistic
                value={this.state.bltp[1]}
                precision={2}
                valueStyle={{ color: "#cf1322" }}
                suffix="%"
                prefix={<ArrowDownOutlined />}
              />
            )}
            <Graph
              labels={this.state.lablesbank}
              data={this.state.databank}
              title="NIFTI Bank"
              grad="#ff66ff"
              border="#ff4dff"
            />
            {/* </Card> */}
          </Col>
          <Col span={6}>
            {/* <Card style={{ width: "45vh",height:"35vh" }}> */}
            <Statistic
              title="INDIA VIX"
              value={this.state.iltp[0]}
              // value={this.state.iltp[1]}
              // precision={2}
              valueStyle={{ color: "#3f8600" }}

              // suffix="%"
            />
            {this.state.iltp[1] > 0 ? (
              <Statistic
                value={this.state.iltp[1]}
                precision={2}
                valueStyle={{ color: "#006600" }}
                suffix="%"
                prefix={<ArrowUpOutlined />}
              />
            ) : (
              <Statistic
                value={this.state.iltp[1]}
                precision={2}
                valueStyle={{ color: "#cf1322" }}
                suffix="%"
                prefix={<ArrowDownOutlined />}
              />
            )}
            <Graph
              labels={this.state.lablesindia}
              data={this.state.dataindia}
              title="INDIA vix"
              grad="#ff9933"
              border="#ff6600"
            />
            {/* </Card> */}
          </Col>
        </Row>
        <Row gutter={16}>
          <Col span={12}>
            <TopTable
              Name={this.state.gainers}
              data={this.state.gainersltp}
              label="gain"
            />
          </Col>
          <Col span={12}>
            <TopTable
              Name={this.state.loosers}
              data={this.state.loosersltp}
              label="loss"
            />
          </Col>
        </Row>
      </div>
    );
  }
}
// export {socket};
export default DashBoard;
