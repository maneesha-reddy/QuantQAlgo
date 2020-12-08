import React, { Component } from 'react';
import { HomeOutlined} from '@ant-design/icons';
import {Breadcrumb } from "antd";
import {Statistic, Slider, InputNumber, Row, Col, Card } from 'antd';
import { ArrowUpOutlined, ArrowDownOutlined } from '@ant-design/icons';
import { Select } from 'antd';
import { Form,Button } from 'antd';
import "./PaperTrade.css"
import { List} from 'antd';
import axios from "axios";
import {socket} from '../dashboard/Dashboard'
import { Tag, Divider } from 'antd';
console.log(socket,"socket-123");

class PaperTrade extends Component {
    constructor(props) {
        super(props);
        this.state = {
            inputValue: 0,
            capital:0,
            size:[],
            tradename:[],
            pnl:[],
            entryval:[],
            tradeltp:[],
            tradetoken:[],
            paper:false,
          };
    }
    componentDidMount() {
        socket.on('paper',this.handlecapital);
        socket.on('size',this.handlesize);
        socket.on('tradename',this.handletradename);
        socket.on('pnl',this.handlepnl);
        socket.on('entryval',this.handleentryval);
        socket.on('tradeltp',this.handletradeltp);
        socket.on('tradetoken',this.handletradetoken);

    }
    handlecapital= (msg) => {
      this.setState({capital:msg});
    };
    handlesize= (msg) => {
      this.setState({size:msg});
    };
    handletradename= (msg) => {
      this.setState({tradename:msg});
    };
    handlepnl= (msg) => {
      this.setState({pnl:msg});
    };
    handleentryval= (msg) => {
      this.setState({entryval:msg});
    };
    handletradeltp= (msg) => {
      this.setState({tradeltp:msg});
    };
    handletradetoken= (msg) => {
      this.setState({tradetoken:msg});
    };
    onChange = value => {
        if (isNaN(value)) {
          return;
        }
        this.setState({
          inputValue: value,
        });
      };
     

    
    render() { 
        const { inputValue } = this.state;
        const { Option } = Select;
        const data = [
            {
              title:this.state.tradename[0] ,
              entry:this.state.entryval[0],
              size:this.state.size[0],
              ltp:this.state.tradeltp[0],
              pnl:this.state.pnl[0],
              tradetoken:this.state.tradetoken[0]
            },
            {
              title:this.state.tradename[1] ,
              entry:this.state.entryval[1],
              size:this.state.size[1],
              ltp:this.state.tradeltp[1],
              pnl:this.state.pnl[1],
              tradetoken:this.state.tradetoken[1]
            },
            {
              title:this.state.tradename[2] ,
              entry:this.state.entryval[2],
              size:this.state.size[2],
              ltp:this.state.tradeltp[2],
              pnl:this.state.pnl[2],
              tradetoken:this.state.tradetoken[2]
            },
            {
              title:this.state.tradename[3] ,
              entry:this.state.entryval[3],
              size:this.state.size[3],
              ltp:this.state.tradeltp[3],
              pnl:this.state.pnl[3],
              tradetoken:this.state.tradetoken[3]
            },
          ];
          
        const onFinish = values => {
              console.log('Success:', values);
              this.setState({paper:true});
              let url = "http://127.0.0.1:8000/papertrade/";
                axios.post(url, values, {}).then((res) => {
                console.warn(res.data);
             });
        };
        const onFinishFailed = errorInfo => {
            console.log('Failed:', errorInfo);
        }
        return ( 
        <div>
        <Breadcrumb style={{ margin: "16px 0" }}>
            <Breadcrumb.Item href=""><HomeOutlined /> <span>Home</span></Breadcrumb.Item>
            <Breadcrumb.Item>Deployment</Breadcrumb.Item>
            <Breadcrumb.Item>PaperTrade</Breadcrumb.Item>
         </Breadcrumb>
         <Row>
             
         <Col span={12}>
         <Form
            name="basic"
             onFinish={onFinish}
        >
         <Form.Item
            label="Capital"
            name="capital">
           <Slider
             style={{left: "0%" , right: "auto" , width: "92.7%"}}
            //  color="#ff9933"
             min={0}
             max={100000}
             onChange={this.onChange}
             value={typeof inputValue === 'number' ? inputValue : 0}
             step={100}
           />
           </Form.Item>
           <Form.Item >
                <Button type="primary" htmlType="submit">
                     PaperTrade
                 </Button>
            </Form.Item>
           </Form>
         </Col>
         <Col span={4}>
           <InputNumber
             min={0}
             max={100000}
             style={{ margin: '0 16px' }}
             step={100}
             value={inputValue}
             onChange={this.onChange}
           />
         </Col>
         <Col  >
         <Card>
          <Statistic
            title="Profit/Loss"
            value={0}
            // precision={2}
            valueStyle={{ color: '#3f8600' }}
            prefix={<ArrowUpOutlined />}
            suffix="%"
          />
        </Card>
        
        </Col>
        <Col offset={1} >
         <Card >
          <Statistic
            title="Capital"
            value={this.state.capital}
            // precision={2}
            valueStyle={{ color: '#3f8600' }}
            // prefix={<ArrowUpOutlined />}
            // suffix="%"
          />
        </Card>
        
        </Col>
       </Row>
       {/* <Row> */}
       <br/>
      {this.state.paper ?(
       <List
            grid={{ gutter:16, column: 4 }}
            dataSource={data}
            renderItem={item => (
            <List.Item>
                <Card hoverable={true} title={item.title}>
                <Tag color="#2db7f5">LTP        :</Tag>{item.ltp}
                <br/>
                <Tag color="#87d068">LotSize    :</Tag> {item.size}
                <br/>
                <Tag color="#108ee9">EntryValue :</Tag>   {item.entry}
                <br/>
                <Tag color="gold">Profit/loss :</Tag>   {item.pnl}
                <br/>
                <Tag color="purple">Token :</Tag>   {item.tradetoken}
                </Card>
            </List.Item>
            )}

        />):
        (
            <></>
        )}

       {/* </Row> */}
      
       </div>
         );
    }
}
export default PaperTrade;




  