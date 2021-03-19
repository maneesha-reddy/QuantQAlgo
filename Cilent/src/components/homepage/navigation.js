import React from "react";
import { NavLink } from "react-router-dom";
import { Divider } from "antd";
import design1 from "./Design1.jpg";
import design2 from "./Design2.png";
import design3 from "./Design3.png";
import design4 from "./Design1.png";
import { Row, Col } from "antd";
import { Tag,Select } from "antd";
const { Option } = Select;
export const Navigation = (props) => {
  return (
    <nav id="menu" className="navbar navbar-default navbar-fixed-top">
      {/* <Row justify="center">
      
      </Row>
      <br/>
      <br/> */}
      <Row>
        <div className="container">
          <div className="navbar-header">
            <button
              type="button"
              className="navbar-toggle collapsed"
              data-toggle="collapse"
              data-target="#bs-example-navbar-collapse-1"
            >
              {" "}
              <span className="sr-only">Toggle navigation</span>{" "}
              <span className="icon-bar"></span>{" "}
              <span className="icon-bar"></span>{" "}
              <span className="icon-bar"></span>{" "}
            </button>
            <a className="navbar-brand page-scroll" href="#page-top">
              <img
                src={design4}
                style={{ marginTop: "-30px", height: "auto", width: "110px" }}
                className="img-responsive"
                alt=""
              />{" "}
            </a>{" "}
          </div>

          <div
            className="collapse navbar-collapse"
            id="bs-example-navbar-collapse-1"
          >
            <ul className="nav navbar-nav navbar-right">
              {/* <ul> */}
              <li>
                <a href="#features" className="page-scroll">
                  Home
                </a>
              </li>
              {/* <li>
              <a href="#about" className="page-scroll">
                Services
              </a>
            </li> */}
              <li>
                <a href="#services" className="page-scroll">
                  Services
                </a>
              </li>
              <li>
                {/* <a href="#about" className="page-scroll">
                  Codestrategy
                </a> */}
                <Select
                  defaultValue="Strategies"
                  style={{ width: 140,color:"black" }}
                  // onChange={handleChange}
                  bordered={false}
                >
                  <Option value="Codemystrategies">Codemystrategies</Option>
                  <Option value="Avaliable strategies">Avaliable strategies</Option>
                </Select>
              </li>
             
              {/* <li>
              <a href="#testimonials" className="page-scroll">
                Career
              </a>
            </li>
            <li>
              <a href="#team" className="page-scroll">
                Account
              </a>
            </li> */}
              <li>
                <a href="#contact" className="page-scroll">
                  Contact
                </a>
              </li>
              {/* </ul> */}
              {/* <Divider type= "vertical"/>
          <ul className="nav navbar-nav navbar-right"> */}
              {/* <li>
                <NavLink to="/SignIn">Login</NavLink>
              </li> */}
              {/* <li>
                <NavLink to="/SignUp">SignUp</NavLink>
              </li> */}
              <li>
                <Select
                  defaultValue="QQA Live"
                  style={{ width: 120,color:"black" }}
                  // onChange={handleChange}
                  bordered={false}
                >
                  <Option value="SIGNIN">SIGNIN</Option>
                  <Option value="LOGIN">LOGIN</Option>
                </Select>
              </li>
              <li>
                <a href="#portfolio" className="page-scroll">
                  Blogs & FAQ's
                </a>
              </li>
            </ul>
          </div>
        </div>
      </Row>
    </nav>
  );
};
