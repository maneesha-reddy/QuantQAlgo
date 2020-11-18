import React, { Component } from 'react';
import { Table, Tag, Space } from 'antd';
class TopTable extends Component {
    constructor(props) {
        super(props);
        this.state = { 
         }
    }
   
render() { 
      
const columns = [
  {
    title: 'StockName',
    dataIndex: 'name',
    key: 'tags',
    render: (tags) => (
      <Tag color={tags[1]} key={tags[0]}>
             {tags[0].toUpperCase()}
      </Tag>
    ),      
  },
  {
    title: this.props.label,
    dataIndex: 'ltp',
    key: 'ltp',
  },


  
];

// const names = Object.values(this.props.Name);
// const handlecolor={
//   this.setState({color:'green'});
// }
const data = [];
if(this.props.Name!=undefined)
{
  // console.log(this.props.Name[0]);
  let c="blue"
  for (let i = 0; i < 5; i++) {
    if(this.props.data[i]<0){
      c='red'
    }
    else{
      c="blue"
    }
    data.push({
        key:i,
        name:[this.props.Name[i],c],
        ltp:this.props.data[i],
    });
}
}

   
   
        return( <Table columns={columns} dataSource={data}  pagination={false}  size="small" style={{width:"70vh"}}/>);
    }
}
 
export default TopTable;