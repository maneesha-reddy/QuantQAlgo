import React from "react";
import logo from "./logo.png";
import { Layout } from "antd";
import { NavLink } from "react-router-dom";
import { Avatar } from "antd";
import { UserOutlined ,BellOutlined} from "@ant-design/icons";

// import { Select } from 'antd';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';

const { Option } = Select;

const { Header } = Layout;
const age=' ';
function handleChange(value) {
    console.log(`selected ${value}`);
  }

function TopBar() {
  return (
     
    <Header
      className="header"
      style={{ position: "fixed", zIndex: 1, width: "100%" }}
    >
        
        <div>
          <NavLink to="">
            <img className="logo" src={logo} alt="logo"></img>
          </NavLink>
          
         
          <Avatar icon={ <BellOutlined />}
            style={{ backgroundColor: "#87d068", marginLeft: 1050 }}
            size="large"
            icon={<UserOutlined />}
          />
        
         
        {/* <FormControl>
        <InputLabel id="demo-simple-select-label">MyAccount</InputLabel>
        <Select
          labelId="demo-simple-select-label"
          id="demo-simple-select"
          value={age}
          onChange={handleChange}
        >
          <MenuItem value={10}>My profile</MenuItem>
          <MenuItem value={20}>settings</MenuItem>
          <MenuItem value={30}>Logout</MenuItem>
        </Select>
      </FormControl> */}
      </div>
    </Header>
   
  );
}




    
   
export default TopBar;
