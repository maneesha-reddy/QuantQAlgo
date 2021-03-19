import React from "react";
import { Row, Col } from "antd";
import adobe1 from "./adobe1.png";
import adobe2 from "./adobe2.png";
import adobe3 from "./adobe3.png";
export const About = (props) => {
  return (
    <div id="about">
      <div className="container">
        <Row>
          <Col span={12}></Col>
          <Col span={12}>
            <img src={adobe1}  alt="" />{" "}
          </Col>
        </Row>
        <Row>
          <Col span={12}>
            <img src={adobe2} className="img-responsive" alt="" />{" "}
          </Col>
          <Col span={12}></Col>
        </Row>
        <Row>
          <Col span={12}></Col>
          <Col span={12}>
            <img src={adobe3} className="img-responsive" alt="" />{" "}
          </Col>
        </Row>
      </div>
    </div>
  );
};
