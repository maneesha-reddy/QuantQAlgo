import React from "react";
import { Row, Col, Divider } from "antd";
import key from "./key.jpg";

export const Services = (props) => {
  return (
    <div id="services" className="text-center">
      <div className="container">
        <div className="section-title">
          <h2>Our Services</h2>
          {/* <p>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit duis sed
            dapibus leonec.
          </p> */}
        </div>
        <div className="row">
          {props.data
            ? props.data.map((d, i) => (
                <div key={`${d.name}-${i}`} className="col-md-4">
                  {" "}
                  <i className={d.icon}></i>
                  <div className="service-desc">
                    {/* <h3>{d.name}</h3> */}
                    <li>{d.text1}</li>
                    <li>{d.text2}</li>
                    {/* <li>{d.text3}</li> */}
                  </div>
                </div>
              ))
            : "loading"}
        </div>
      </div>
      <Divider />
      <Row justify="center">
        <Col span={12}>
          <img
            src={key}
            style={{ height: "500px", width: "700px" }}
            className="img-responsive"
            alt=""
          />{" "}
        </Col>
        <Col offset={2} span={9}>
          <h2>
            <b>Key features</b>
          </h2>
          <h3 className="who"><b>
            <li>Powerful, smart &amp; ready to use strategies.</li>
            <br/>
            <li>
              Connect brokers that offer automation &amp; run your strategies in
              paper &amp; live environment.
            </li>
            <br/>
            <li> Connect &amp; trade with a few clicks -> go algo anytime. </li>
            <br/>
            <li>
              Low latency order execution, without manual intervention. Highly
              reliable system.
            </li>
            <br/>
            <li> Direct market access provided for NSE, BSE,MCX, CDS.</li>
            </b>   </h3>
        </Col>
      </Row>
    </div>
  );
};
