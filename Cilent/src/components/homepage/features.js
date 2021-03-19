import React from "react";
import { Row, Col } from "antd";
import who from "./who.jpg";
import who1 from "./who1.jpg";
import who2 from "./who2.png";
export const Features = (props) => {
  return (
    <div id="features">
      {/* <div className="container"> */}
      <Row>
        <Col span={12}>
          <img
            src={who2}
            style={{ height: "auto", width: "700px" }}
            className="img-responsive"
            alt=""
          />{" "}
          {/* <img className="who" src={who} alt="who"></img> ?style={{ color: "black",fontFamily:"'Courier New', monospace" }}*/}
        </Col>
        <Col offset={2} span={9}>
          <h3 className="who"  >
            {/* <br /> */}
            For leveraging market potential to yeild high returns, startegic
            investment with adequate risk management is inevitable. Algorithmic
            trading provides a platform to generate optimum return with real
            time emotionless trade execution while reducing manual intervention
            to minimize human errors.
            <br /> <br />
            QuantQalgo helps to turn your financialdreams into reality by
            letting you choose from a wide range of strategies curated by
            market.
            <br /> <br />
            If you want to trade with your own strategy but unsure how to
            implement the same, then look no further. Out friendly and highly
            qualified team can customize your strategy to meet the desired
            functionality.
            <br /> <br />
            You can also advertise your strategy and generate revenue based on
            the number of subscriptions on your customized strategy
         </h3>
        </Col>
      </Row>
      {/* </div> */}
    </div>
    // <div id="features" className="text-center">
    //   {/* <div className="container"> */}
    //     <Row>
    //       <Col span={12}>
    //         <img src={who2} className="img-responsive" alt="" />{" "}
    //         {/* <img className="who" src={who} alt="who"></img> */}
    //       </Col>
    //       <Col span={12}>
    //         <p>
    //           Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed nonne
    //           merninisti licere mihi ista probare, quae sunt a te dicta? Refert
    //           tamen, quo modo.
    //         </p>
    //       </Col>
    //     </Row>
    //   {/* </div> */}
    // </div>
  );
};
