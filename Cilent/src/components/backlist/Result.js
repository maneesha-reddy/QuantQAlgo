import React, { Component } from "react";
import { Spin } from "antd";
import { Tag, Table, Space } from "antd";
import { Statistic, Row, Col, Button } from "antd";
import "./Result.css";
import { Card } from "@material-ui/core";

class Result extends Component {
  constructor(props) {
    super(props);
    this.state = { trade: false };
    this.handleTrade = this.handleTrade.bind(this);
  }
  handleTrade = (e) => {
    this.setState({ trade: true });
    // this.props.handleWidth();
  };
  render() {
    console.log(this.props.results, this.props.props, "RESUTS");
    const columns = [
      {
        title: "Entry",
        dataIndex: "name",
        key: "name",
        fixed: 'left',
        //   render: text => <a>{text}</a>,
      },
      {
        title: "Date",
        dataIndex: "date",
        key: "date",
        fixed: 'left',
      },
      {
        title: "Price",
        dataIndex: "price",
        key: "VALUES",
      },
      {
        title: "Exit",
        dataIndex: "exit",
        key: "VALUES",
      },
      {
        title: "ExDate",
        dataIndex: "exdate",
        key: "VALUES",
      },
      {
        title: "% Change",
        dataIndex: "change",
        key: "VALUES",
      },
      {
        title: "Profit",
        dataIndex: "profit",
        key: "VALUES",
      },
      {
        title: "% Profit",
        dataIndex: "perprofit",
        key: "VALUES",
      },
      {
        title: "Position value",
        dataIndex: "position_value",
        key: "VALUES",
      },
      {
        title: "Cumm Profit",
        dataIndex: "cumm_profit",
        key: "VALUES",
      },
      {
        title: "MAE",
        dataIndex: "mae",
        key: "VALUES",
      },
      {
        title: "MFE",
        dataIndex: "mfe",
        key: "VALUES",
      },
      {
        title: "Scale In / Scale Out",
        dataIndex: "SS",
        key: "VALUES",
      },
    ];

    const data = [];
    for (let i = 0; i < 20; i++) {
      data.push({
        key: i,
        name: this.props.results != undefined && this.props.results["Entry"][i],
        date: this.props.results != undefined && this.props.results["Date"][i],
        price:
          this.props.results != undefined && this.props.results["Price"][i],
        exit: this.props.results != undefined && this.props.results["Exit"][i],
        exdate:
          this.props.results != undefined && this.props.results["ExDate"][i],
        change:
          this.props.results != undefined && this.props.results["change"][i],
        profit:
          this.props.results != undefined && this.props.results["Profit"][i],
        perprofit:
          this.props.results != undefined && this.props.results["perprofit"][i],
        position_value:
          this.props.results != undefined &&
          this.props.results["position_value"][i],
        cumm_profit:
          this.props.results != undefined &&
          this.props.results["cumm_profit"][i],
        mae: this.props.results != undefined && this.props.results["MAE"][i],
        mfe: this.props.results != undefined && this.props.results["MFE"][i],
        SS: this.props.results != undefined && this.props.results["SS"][i],
      });
    }

    return this.props.props == false ? (
      // <div>
      this.state.trade ? (
        <Table columns={columns} dataSource={data} pagination={false} scroll={{ x: 1000,y:500 }} />
      ) : (
        <div className="site-statistic-demo-card">
          <Row gutter={16}>
            <Col span={8}>
              <Card style={{ width: "30vh" }}>
                <Statistic
                  style={{ textAlign: "center" }}
                  title="Trade_start_date"
                  valueStyle={{ color: "#3f8600" }}
                  value={
                    this.props.results != undefined &&
                    this.props.results["Trade_start_date"]
                  }
                />
              </Card>
              <br />
              {/* </Tag> */}
              <Card style={{ width: "30vh" }}>
                <Statistic
                  style={{ textAlign: "center" }}
                  title="Initial_Capital"
                  valueStyle={{ color: "#3f8600" }}
                  value={
                    this.props.results != undefined &&
                    this.props.results["Initial_Capital"]
                  }
                />
              </Card>
              <br />

              <Card style={{ width: "30vh" }}>
                <Statistic
                  style={{ textAlign: "center" }}
                  title="Total_no_trades"
                  valueStyle={{ color: "#3f8600" }}
                  value={
                    this.props.results != undefined &&
                    this.props.results["Total_no_trades"]
                  }
                />
                <Button size="small" onClick={this.handleTrade}>
                  view Details
                </Button>
              </Card>

              <br />
              <Card style={{ width: "30vh" }}>
                <Statistic
                  style={{ textAlign: "center" }}
                  title="Negative_trades"
                  valueStyle={{ color: "#3f8600" }}
                  value={
                    this.props.results != undefined &&
                    this.props.results["Negative_trades"]
                  }
                />
              </Card>
              <br />
            </Col>
            <Col span={8}>
              <Card style={{ width: "30vh" }}>
                <Statistic
                  style={{ textAlign: "center" }}
                  valueStyle={{ color: "#3f8600" }}
                  title="Trade end date"
                  value={
                    this.props.results != undefined &&
                    this.props.results["Trade_end_date"]
                  }
                  precision={2}
                />
              </Card>
              <br />
              <Card style={{ width: "30vh" }}>
                <Statistic
                  style={{ textAlign: "center" }}
                  valueStyle={{ color: "#3f8600" }}
                  title="Ending_Capital"
                  value={
                    this.props.results != undefined &&
                    this.props.results["Ending_Capital"]
                  }
                  precision={2}
                />
              </Card>
              <br />
              <Card style={{ width: "30vh" }}>
                <Statistic
                  style={{ textAlign: "center" }}
                  valueStyle={{ color: "#3f8600" }}
                  title="Positive_trades"
                  value={
                    this.props.results != undefined &&
                    this.props.results["Positive_trades"]
                  }
                  precision={2}
                />
              </Card>
              <br />
              <Card style={{ width: "30vh" }}>
                <Statistic
                  style={{ textAlign: "center" }}
                  valueStyle={{ color: "#3f8600" }}
                  title="Total_loss"
                  value={
                    this.props.results != undefined &&
                    this.props.results["Total_loss"]
                  }
                  precision={2}
                />
              </Card>
              <br />
            </Col>
            <Col span={8}>
              <Card style={{ width: "30vh" }}>
                <Statistic
                  style={{ textAlign: "center" }}
                  valueStyle={{ color: "#3f8600" }}
                  title="Net_Profit"
                  value={
                    this.props.results != undefined &&
                    this.props.results["Net_Profit"]
                  }
                />
              </Card>
              <br />
              <Card style={{ width: "30vh" }}>
                <Statistic
                  style={{ textAlign: "center" }}
                  valueStyle={{ color: "#3f8600" }}
                  title="CAGR"
                  value={
                    this.props.results != undefined &&
                    this.props.results["CAGR"]
                  }
                />
              </Card>
              <br />
              <Card style={{ width: "30vh" }}>
                <Statistic
                  style={{ textAlign: "center" }}
                  valueStyle={{ color: "#3f8600" }}
                  title="Sharpe_ratio"
                  value={
                    this.props.results != undefined &&
                    this.props.results["Sharpe_ratio"]
                  }
                  precision={2}
                />
              </Card>
              <br />
              <Card style={{ width: "30vh" }}>
                <Statistic
                  style={{ textAlign: "center" }}
                  valueStyle={{ color: "#3f8600" }}
                  title="Maximum_Drawdown"
                  value={
                    this.props.results != undefined &&
                    this.props.results["Maximum_Drawdown"]
                  }
                />
              </Card>
            </Col>
          </Row>
        </div>
      )
    ) : (
      // </div>
      <Spin tip="Loading..."></Spin>
    );
  }
}
export default Result;
