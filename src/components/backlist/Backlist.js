import React, { Component } from "react";
import InputLabel from "@material-ui/core/InputLabel";
import MenuItem from "@material-ui/core/MenuItem";
import FormControl from "@material-ui/core/FormControl";
// import Select from '@material-ui/core/Select';
import TextField from "@material-ui/core/TextField";
import "./Backlist.css";
import { DatePicker, Radio, Space } from "antd";
import { Select } from "antd";
import { Row, Col } from "antd";
import { Modal, Button } from "antd";
import { PlusCircleFilled } from "@ant-design/icons";
import InputAdornment from "@material-ui/core/InputAdornment";
// import TextField from "@material-ui/core/TextField";

const { Option } = Select;
class Backlist extends Component {
  constructor(props) {
    super(props);
    this.state = { exchange: undefined, size: "defalut", modal2Visible: false };
  }

  setModal2Visible(modal2Visible) {
    this.setState({ modal2Visible });
  }

  handleChange = (event) => {
    this.setState({
      Bank: event.target.value,
    });
  };
  handleDateChange = (event) => {
    this.setState({
      size: event.target.value,
    });
  };
  onexchangeChange = (event) => {
    console.log(event, "event");
    this.setState({
      exchange: event,
    });
  };
  render() {
    const { size } = this.state.size;
    if (this.state.exchange == "NSE" || this.state.exchange == "BSE") {
      return (
        <div style={{ backgroundColor: "white", paddingLeft: 30 }}>
          <Button
            icon={<PlusCircleFilled />}
            type="primary"
            onClick={() => this.setModal2Visible(true)}
          ></Button>
          <Modal
            title="Add to the list"
            centered
            visible={this.state.modal2Visible}
            onOk={() => this.setModal2Visible(false)}
            onCancel={() => this.setModal2Visible(false)}
            okText="Add"
            cancelText="cancel"
          >
            <Row>
              <Col span={12}>
                <label>
                  <b>Exchange :</b>{" "}
                </label>
                <Select
                  showSearch
                  style={{ width: 200 }}
                  placeholder="exchange"
                  optionFilterProp="children"
                  onChange={(event) => this.onexchangeChange(event)}
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
                <br />
                <br />
                <label>
                  <b>Segment :</b>{" "}
                </label>

                <Select
                  disabled
                  showSearch
                  style={{ width: 200 }}
                  placeholder="Segment"
                  optionFilterProp="children"
                  // onChange={onChange}
                  // onFocus={onFocus}
                  // onBlur={onBlur}
                  // onSearch={onSearch}
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

                <br />
                <br />
                <form>
                  <TextField
                    id="outlined-basic"
                    label="Enter Quantity"
                    variant="outlined"
                  />
                </form>
                <br />
                {/* <label>
                  <b>From: </b>
                </label>
                <Space direction="vertical" size={12}>
                  <DatePicker size={size} />
                </Space> */}
                <form noValidate>
                  <TextField
                    id="datetime-local"
                    label="From"
                    type="datetime-local"
                    defaultValue=""
                    InputLabelProps={{
                      shrink: true,
                    }}
                  />
                </form>
                <br />
                {/* <label style={{ marginRight: 16 }}>
                  <b>To : </b>
                </label>
                <Space direction="vertical" size={12}>
                  <DatePicker size={size} />
                </Space> */}
                <form noValidate>
                  <TextField
                    id="datetime-local"
                    label="To"
                    type="datetime-local"
                    defaultValue=""
                    InputLabelProps={{
                      shrink: true,
                    }}
                  />
                </form>
              </Col>

              <Col span={12}>
                <label>
                  <b>Symbols :</b>{" "}
                </label>

                <Select
                  showSearch
                  style={{ width: 200 }}
                  placeholder="symbols"
                  optionFilterProp="children"
                  // onChange={onChange}
                  // onFocus={onFocus}
                  // onBlur={onBlur}
                  // onSearch={onSearch}
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
                <br />
                <br />
                <label>
                  <b>Strike Price :</b>{" "}
                </label>

                <Select
                  disabled
                  showSearch
                  style={{ width: 200 }}
                  placeholder="StrikePrice"
                  optionFilterProp="children"
                  // onChange={onChange}
                  // onFocus={onFocus}
                  // onBlur={onBlur}
                  // onSearch={onSearch}
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
                <br />
                <br />
                <label>
                  <b>Strategy : </b>
                </label>

                <Select
                  showSearch
                  style={{ width: 200 }}
                  placeholder="Strategy"
                  optionFilterProp="children"
                  // onChange={onChange}
                  // onFocus={onFocus}
                  // onBlur={onBlur}
                  // onSearch={onSearch}
                  filterOption={(input, option) =>
                    option.children
                      .toLowerCase()
                      .indexOf(input.toLowerCase()) >= 0
                  }
                >
                  <Option value="Strategy 1">Strategy 1</Option>
                  <Option value="Strategy 2">Strategy 2</Option>
                  <Option value="Strategy 3">Strategy 3</Option>
                </Select>

                <br />
                <br />
                <TextField
                  id="outlined-basic"
                  label="Captital"
                  variant="outlined"
                />
              </Col>
            </Row>
          </Modal>
        </div>
      );
    } else {
      return (
        <div style={{ backgroundColor: "white", paddingLeft: 30 }}>
          <Button
            icon={<PlusCircleFilled />}
            type="primary"
            onClick={() => this.setModal2Visible(true)}
          ></Button>
          <Modal
            title="Add to the list"
            centered
            visible={this.state.modal2Visible}
            onOk={() => this.setModal2Visible(false)}
            onCancel={() => this.setModal2Visible(false)}
            okText="Add"
            cancelText="cancel"
          >
            <Row>
              <Col span={12}>
                <label>
                  <b>Exchange :</b>{" "}
                </label>
                <Select
                  showSearch
                  style={{ width: 200 }}
                  placeholder="exchange"
                  optionFilterProp="children"
                  onChange={(event) => this.onexchangeChange(event)}
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
                <br />
                <br />
                <label>
                  <b>Segment :</b>{" "}
                </label>

                <Select
                  showSearch
                  style={{ width: 200 }}
                  placeholder="Segment"
                  optionFilterProp="children"
                  // onChange={onChange}
                  // onFocus={onFocus}
                  // onBlur={onBlur}
                  // onSearch={onSearch}
                  filterOption={(input, option) =>
                    option.children
                      .toLowerCase()
                      .indexOf(input.toLowerCase()) >= 0
                  }
                >
                  <Option value="FUT">FUT</Option>
                  <Option value="OPT">OPT</Option>
                </Select>

                <br />
                <br />
                <form>
                  <TextField
                    id="outlined-basic"
                    label="Enter Quantity in LOTS"
                    variant="outlined"
                  />
                </form>
                <br />
                {/* <label>
                  <b>From: </b>
                </label>
                <Space direction="vertical" size={12}>
                  <DatePicker size={size} />
                </Space> */}
                <form noValidate>
                  <TextField
                    id="datetime-local"
                    label="From"
                    type="datetime-local"
                    defaultValue=""
                    InputLabelProps={{
                      shrink: true,
                    }}
                  />
                </form>
              </Col>

              <Col span={12}>
                <label>
                  <b>Symbols :</b>{" "}
                </label>

                <Select
                  showSearch
                  style={{ width: 200 }}
                  placeholder="symbols"
                  optionFilterProp="children"
                  // onChange={onChange}
                  // onFocus={onFocus}
                  // onBlur={onBlur}
                  // onSearch={onSearch}
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
                <br />
                <br />
                <label>
                  <b>Strike Price :</b>{" "}
                </label>

                <Select
                  showSearch
                  style={{ width: 200 }}
                  placeholder="StrikePrice"
                  optionFilterProp="children"
                  // onChange={onChange}
                  // onFocus={onFocus}
                  // onBlur={onBlur}
                  // onSearch={onSearch}
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
                <br />
                <br />
                <label>
                  <b>Strategy : </b>
                </label>

                <Select
                  showSearch
                  style={{ width: 200 }}
                  placeholder="Strategy"
                  optionFilterProp="children"
                  // onChange={onChange}
                  // onFocus={onFocus}
                  // onBlur={onBlur}
                  // onSearch={onSearch}
                  filterOption={(input, option) =>
                    option.children
                      .toLowerCase()
                      .indexOf(input.toLowerCase()) >= 0
                  }
                >
                  <Option value="Strategy-1">Strategy-1</Option>
                  <Option value="Strategy-2">Strategy-2</Option>
                  <Option value="Strategy-3">Strategy-3</Option>
                </Select>

                <br />
                <br />
                {/* <label>
                  <b>To: </b>
                </label>
                <Space direction="vertical" size={12}>
                  <DatePicker size={size} />
                </Space> */}
                <form noValidate>
                  <TextField
                    id="datetime-local"
                    label="To"
                    type="datetime-local"
                    defaultValue=" "
                    InputLabelProps={{
                      shrink: true,
                    }}
                  />
                </form>
              </Col>
            </Row>
          </Modal>
        </div>
      );
    }
  }
}

export default Backlist;
