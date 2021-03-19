import React, { Component } from "react";
import { Table, Tag, Space } from "antd";
class TopTable extends Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  render() {
    // console.log(this.props.data)
    const columns = [
      {
        title: "StockName",
        dataIndex: "name",
        key: "tags",
        render: (tags) => (
          <Tag color={tags[1]} key={tags[0]}>
            {tags[0].toUpperCase()}
          </Tag>
        ),
      },
      {
        title: this.props.label,
        dataIndex: "gain",
        key: "gain",
      },
      {
        title: "LTP",
        dataIndex: "ltp",
        key: "ltp",
      },
      {
        title: "Prev Close",
        dataIndex: "PC",
        key: "PC",
      },
    ];

    // const names = Object.values(this.props.Name);
    // const handlecolor={
    //   this.setState({color:'green'});
    // }
    const data = [];
    if (this.props.data != undefined) {
      // console.log(this.props.data.length);

      if (this.props.Name != undefined) {
        let c = "#87d068";
        for (let i = 0; i < 5; i++) {
          if (this.props.data[i] != undefined) {
            // console.log(this.props.data[i].length);

            if (this.props.data[i][0] < 0) {
              c = "red";
            } else {
              c = "#87d068";
            }
            data.push({
              key: i,
              name: [this.props.Name[i], c],
              gain: this.props.data[i][0],
              ltp: this.props.data[i][1],
              PC: this.props.data[i][2],
            });
          }
        }
      }
    }

    return (
      <Table
        className="table"
        columns={columns}
        dataSource={data}
        pagination={false}
        size="small"
        style={{ width: "70vh", backgroundColor: "black", color: "white" }}
      />
    );
  }
}

export default TopTable;
