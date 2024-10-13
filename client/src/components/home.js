import React, { Component, useReducer } from 'react';
import {
    Collapse, 
    Nav, NavItem, NavLink, 
    UncontrolledDropdown, Dropdown, DropdownToggle, DropdownMenu, DropdownItem, 
    Input, InputGroup, InputGroupText,
    Button, Row, Col, Form, Container, Label
} from "reactstrap";
import { withCookies, Cookies } from 'react-cookie';
import { instanceOf } from 'prop-types';
import { Helmet } from 'react-helmet'
import {
    Audio,
    BallTriangle,
    Bars,
    Circles,
    Grid,
    Hearts,
    Oval,
    Puff,
    Rings,
    SpinningCircles,
    TailSpin,
    ThreeDots,
} from '@agney/react-loading';
import { ToastContainer, toast } from 'react-toastify';
import { Platform_Name } from '../platform_name';
import { Backend_Server_Address } from '../backend_server_url';
import { Access_Token_Cookie_Name } from '../access_token_cookie_name';
import { Maximum_Holding_Time } from './maximum_holding_time'
import { Unknown_Non_2xx_Message, Network_Error_Message, No_Network_Access_Message } from '../network_error_messages';
import LoadingScreen from './loading_screen';
import InputErrors from './input_errors';
import Notification from './notification_alert';
import NetworkErrorScreen from './network_error_screen';
import Jumbotron1 from '../images/jumbotron_1.jpg'
import Home1 from '../images/home_1.jpg'
import Home2 from '../images/home_2.jpg'
import Home3 from '../images/home_3.jpg'

class Home extends Component{
    static propTypes = {
        cookies: instanceOf(Cookies).isRequired
    };
    constructor(props) { 
        super(props);
        this.state = {
            loading: false,
            network_error_screen: false,
            network_error_message: '',
            retry_function: null,
            input_errors: {},
            on_mobile: false
        };

        this.HandleChange = (e) => {
            this.setState({[e.target.name]: e.target.value});
        };

        this.SetInputError = (field, error) => { // error -> required / invalid
            // existing errors
            var existing_errors = this.state.input_errors

            // existing errors modified
            existing_errors[field] = error

            // update state
            this.setState({input_errors: existing_errors})
        }

        this.ClearInputErrors = () => {
            // existing errors
            var existing_errors = this.state.input_errors
            // array of existing error field names
            var existing_error_fields = Object.keys(existing_errors)
            // set existing error fields to undefined, clearing them
            existing_error_fields.map((item, index) => {
                existing_errors[item] = undefined
            })
            this.setState({input_errors: existing_errors})
        }

        this.LoadingOn = () => {
            this.setState({loading: true})
        }

        this.LoadingOff = () => {
            this.setState({loading: false})
        }

        this.NetworkErrorScreenOn = (error_message, retry_function) => {
            this.setState({network_error_screen: true, network_error_message: error_message, retry_function: retry_function})
        }

        this.NetworkErrorScreenOff = () => {
            this.setState({network_error_screen: false, network_error_message: '', retry_function: null})
        }
    }

    componentDidMount() {
        if( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
            this.setState({
                on_mobile: true
            })
        }
    }

    render() {
        return (
            <div>
                <Helmet>
                    <title>Home | {Platform_Name}</title>
                    {/* <meta name="description" content="" /> */}
                </Helmet>
                <ToastContainer />
                {
                    this.state.loading === true
                    ? <LoadingScreen />
                    : this.state.network_error_screen === true
                    ? <NetworkErrorScreen error_message={this.state.network_error_message} retryFunction={this.state.retry_function} />
                    : <div>
                        <Row style={{color: '#ffffff', height: '550px', margin: '0px'}}>
                            <div style={{position: 'relative', overflow: 'hidden', width: '100%', height: '550px', backgroundColor: '#005fc9'}}>
                                <img src={Jumbotron1} onError={(e) => e.target.src = Jumbotron1} style={{position: 'absolute', opacity: 0.4, right: 0, width: 'auto', minWidth: '100%', height: 'auto', minHeight: '550px'}} />
                                <Container style={{position: 'absolute', top: '135px', left: '10px'}}>
                                    <h1 style={{color: '#ffffff', fontWeight: 'bold', textAlign: 'left'}}>
                                        Maximize Your Trading Potential with AI-Driven Analysis
                                    </h1>
                                    <h3 style={{color: '#FEF6DF', marginTop: '50px', textAlign: 'left'}}>
                                        Unlock Profitable Trading Opportunities Through The Use Of High-Grade Financial Market Analysis. 
                                    </h3>
                                    <Row style={{marginRight: '0px', marginTop: '70px', textAlign: 'left'}}>
                                        <Col sm='6'>
                                            <Button href='/signup' style={{backgroundColor: '#ffffff', color: '#005fc9', fontWeight: 'bold', border: 'none', width: '180px'}}>
                                                Get started
                                            </Button>
                                            <br/><br/>
                                        </Col>
                                    </Row>
                                </Container>
                            </div>
                        </Row>
                        <Container>
                            <Row style={{margin: '0px', minHeight: '300px'}}>
                                <Col sm='6'>
                                    {
                                        this.state.on_mobile === true
                                        ? <><br/><br/><br/></>
                                        : <><br/><br/><br/><br/></>
                                    }
                                    <div style={{position: 'relative', overflow: 'hidden', width: '100%', height: '400px', backgroundColor: '#D0DFE9', border: '1px solid #F9C961', borderRadius: '20px'}}>
                                        <div style={{position: 'absolute', top: '170px', left: 0, right: 0}}>
                                            Loading image...
                                        </div>
                                        <img src={Home1} onError={(e) => e.target.src = Home1} style={{position: 'absolute', right: 0, width: 'auto', minWidth: '100%', height: 'auto', minHeight: '400px'}} />
                                    </div>
                                    {
                                        this.state.on_mobile === true
                                        ? <></>
                                        : <><br/><br/><br/><br/></>
                                    }
                                </Col>
                                <Col>
                                    {
                                        this.state.on_mobile === true
                                        ? <><br/><br/><br/></>
                                        : <><br/><br/><br/></>
                                    }
                                    <h6 style={{fontWeight: 'bold'}}>
                                        Analyze, Predict, and Profit.
                                    </h6>
                                    <br/><br/>
                                    <p style={{textAlign: "justify"}}>
                                        {Platform_Name} is designed to deliver data-driven trade entries with a maximum holding time of {Maximum_Holding_Time}. 
                                        Every trade comes with recommended takeprofit and stoploss percentages, sticking to a minimum risk-to-reward 
                                        ratio of 1:2. Although it may not catch every market move, every trade our revolutionary AI gives 
                                        comes after a careful examination of market dynamics, ensuring that you only get high probability trades.
                                        Each instrument our AI analyses has its own seperate AI model, with its own win rate. For all the AI models, 
                                        win rates range above 80%. <a href='/ai-performance' style={{color: 'inherit'}}>Click here</a> for more 
                                        insight on the performance of our AI models.
                                        <br/><br/>
                                        Our goal is clear - to arm traders with easily accessible and effective tools that facilitate risk 
                                        minimization and reward maximization during trading. We have ensured that this AI powerhouse is 
                                        available to you at an affordable price point, democratizing high-grade financial market analysis.
                                    </p>
                                </Col>
                            </Row>
                        </Container>
                        <div style={{backgroundColor: '#005fc9', color: '#ffffff'}}>
                            <Container>
                                <Row style={{margin: '0px', minHeight: '300px'}}>
                                    {
                                        this.state.on_mobile === true
                                        ? <Col>
                                            <br/><br/><br/><br/>
                                            <div style={{position: 'relative', overflow: 'hidden', width: '100%', height: '400px', backgroundColor: '#D0DFE9', border: '1px solid #F9C961', borderRadius: '20px'}}>
                                                <div style={{position: 'absolute', top: '170px', left: 0, right: 0}}>
                                                    Loading image...
                                                </div>
                                                <img src={Home2} onError={(e) => e.target.src = Home2} style={{position: 'absolute', right: 0, width: 'auto', minWidth: '100%', height: 'auto', minHeight: '400px'}} />
                                            </div>
                                        </Col>
                                        : <></>
                                    }
                                    <Col sm='6'>
                                        {
                                            this.state.on_mobile === true
                                            ? <><br/><br/><br/></>
                                            : <><br/><br/><br/><br/><br/><br/><br/></>
                                        }
                                        <h6 style={{fontWeight: 'bold'}}>
                                            Maximise Your Gains, Minimise Your Risks.
                                        </h6>
                                        <br/><br/>
                                        <p style={{textAlign: "justify"}}>
                                            We help traders take the guesswork out of trading decisions. {Platform_Name} is an affordable, and 
                                            powerful tool that complements your existing strategies to give you a well-rounded trading 
                                            perspective. Whether you're a seasoned trader or a beginner, the analysis provided by {Platform_Name} {' '}
                                            can form the bedrock of your investment decisions. The provided predictions can either act as 
                                            standalone trading decisions or they can complement your existing trading strategies by providing 
                                            an additional, robust, statistics based analytical layer. {' '}
                                            <a href='/ai-performance' style={{color: 'inherit'}}>Click here</a> for more insight on the 
                                            performance of our AI models.
                                        </p>
                                        {
                                            this.state.on_mobile === true
                                            ? <><br/><br/><br/><br/></>
                                            : <><br/><br/><br/><br/></>
                                        }
                                    </Col>
                                    {
                                        this.state.on_mobile == false
                                        ? <Col>
                                            <br/><br/><br/><br/>
                                            <div style={{position: 'relative', overflow: 'hidden', width: '100%', height: '400px', backgroundColor: '#D0DFE9', border: '1px solid #F9C961', borderRadius: '20px'}}>
                                                <div style={{position: 'absolute', top: '170px', left: 0, right: 0}}>
                                                    Loading image...
                                                </div>
                                                <img src={Home2} onError={(e) => e.target.src = Home2} style={{position: 'absolute', right: 0, width: 'auto', minWidth: '100%', height: 'auto', minHeight: '400px'}} />
                                            </div>
                                            <br/><br/><br/><br/>
                                        </Col>
                                        : <></>
                                    }
                                </Row>
                            </Container>
                        </div>
                        <Container>
                            <Row style={{margin: '0px', minHeight: '300px'}}>
                                <Col sm='6'>
                                    {
                                        this.state.on_mobile === true
                                        ? <><br/><br/><br/></>
                                        : <><br/><br/><br/><br/></>
                                    }
                                    <div style={{position: 'relative', overflow: 'hidden', width: '100%', height: '400px', backgroundColor: '#D0DFE9', border: '1px solid #F9C961', borderRadius: '20px'}}>
                                        <div style={{position: 'absolute', top: '170px', left: 0, right: 0}}>
                                            Loading image...
                                        </div>
                                        <img src={Home3} onError={(e) => e.target.src = Home3} style={{position: 'absolute', right: 0, width: 'auto', minWidth: '100%', height: 'auto', minHeight: '400px'}} />
                                    </div>
                                </Col>
                                <Col>
                                    {
                                        this.state.on_mobile === true
                                        ? <><br/><br/><br/></>
                                        : <><br/><br/><br/><br/><br/><br/><br/><br/></>
                                    }
                                    <h6 style={{fontWeight: 'bold'}}>
                                        Advanced Tools, Simplified Trading.
                                    </h6>
                                    <br/><br/>
                                    <p style={{textAlign: "justify"}}>
                                        With an operational method akin to technical analysis, {Platform_Name} stands apart by employing AI 
                                        models, taking on the burden of analysing vast amounts of multitimeframe data and indicators 
                                        in a matter of seconds to come up with simple buy or sell trading decisions that traders can act on. 
                                        Our strategic utilization of AI gives traders a remarkable statistical edge that keeps them profitable 
                                        in the longrun. <a href='/ai-performance' style={{color: 'inherit'}}>Click here</a> for more insight on 
                                        the performance of our AI models.
                                    </p>
                                    {
                                        this.state.on_mobile === true
                                        ? <></>
                                        : <><br/><br/><br/><br/></>
                                    }
                                </Col>
                            </Row>
                            {
                                this.state.on_mobile === true
                                ? <><br/><br/><br/></>
                                : <><br/><br/><br/><br/></>
                            }
                            <h6 style={{fontWeight: 'bold', color: '#005fc9'}}>
                                Join {Platform_Name} Today.
                            </h6>
                            <br/>
                            <p style={{textAlign: "left"}}>
                                Gain a competitive edge in the market with our affordable, AI-driven forex market analysis. 
                                Sign up now and experience the next-level of trading insight.
                            </p>
                            <Row style={{margin: '0px'}}>
                                <Col sm='4'></Col>
                                <Col sm='4'></Col>
                                <Col sm='4'>
                                    <Button href='/signup' style={{backgroundColor: '#005fc9', color: '#ffffff', fontWeight: 'bold', border: '1px solid #005fc9', width: '180px'}}>
                                        Sign up
                                    </Button>
                                </Col>
                            </Row>
                        </Container>
                    </div>
                }
                <br/><br/><br/>
            </div>
        );
    }

};

export default withCookies(Home);