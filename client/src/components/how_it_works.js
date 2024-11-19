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
import HowItWorks1 from '../images/how_it_works_1.jpg'
import HowItWorks2 from '../images/how_it_works_2.jpg'
import HowItWorks3 from '../images/how_it_works_3.jpg'
import HowItWorks4 from '../images/how_it_works_4.jpg'
import HowItWorks5 from '../images/how_it_works_5.jpg'

class HowItWorks extends Component{
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
                    <title>How It Works | {Platform_Name}</title>
                    {/* <meta name="description" content="" /> */}
                </Helmet>
                <ToastContainer />
                {
                    this.state.loading === true
                    ? <LoadingScreen />
                    : this.state.network_error_screen === true
                    ? <NetworkErrorScreen error_message={this.state.network_error_message} retryFunction={this.state.retry_function} />
                    : <div>
                        <div style={{backgroundColor: '#005fc9', color: '#ffffff', minHeight: '200px', borderBottom: '1px solid #F9C961'}}>
                            <br/><br/><br/>
                            <h3 style={{fontWeight: 'bold'}}>
                                How it works
                            </h3>
                        </div>
                        <Container>
                            <br/><br/>
                            <h6 style={{fontWeight: 'bold'}}>
                                Introduction
                            </h6>
                            <br/><br/>
                            <p style={{textAlign: 'justify'}}>
                                Welcome to {Platform_Name} - the Advanced SAAS platform that revolutionizes the way you approach 
                                financial markets, primarily forex. Powered by cutting-edge AI, our platform provides you with high quality 
                                trades that have a maximum recommended holding time of {Maximum_Holding_Time}, addable to any trading arsenal 
                                you may already have. Here's how our system works:
                            </p>
                            <br/><br/>
                            <Row style={{margin: '0px'}}>
                                <Col sm='6'>
                                    <div style={{position: 'relative', overflow: 'hidden', width: '100%', height: '400px', backgroundColor: '#D0DFE9', border: '1px solid #F9C961', borderRadius: '20px'}}>
                                        <div style={{position: 'absolute', top: '170px', left: 0, right: 0}}>
                                            Loading image...
                                        </div>
                                        <img src={HowItWorks1} onError={(e) => e.target.src = HowItWorks1} style={{position: 'absolute', right: 0, width: 'auto', minWidth: '100%', height: 'auto', minHeight: '400px'}} />
                                        <a href='https://unsplash.com/photos/faEfWCdOKIg?utm_source=unsplash&utm_medium=referral&utm_content=creditShareLink'
                                            style={{position: 'absolute', bottom: '10px', right: '10px', color: '#ffffff', fontSize: '13px'}} target='_blank'  rel='noreferrer'
                                        >
                                            Image by Christina @ wocintechchat.com on Unsplash
                                        </a>
                                    </div>
                                </Col>
                                <Col>
                                    {
                                        this.state.on_mobile === true
                                        ? <><br/><br/></>
                                        : <><br/><br/></>
                                    }
                                    <h6 style={{fontWeight: 'bold'}}>
                                        What We Offer
                                    </h6>
                                    <br/><br/>
                                    <p style={{textAlign: 'justify'}}>
                                        <ul>
                                            <li>Predicted buy and sell trade entries.</li><br/>
                                            <li>Recommended stoploss percentages.</li><br/>
                                            <li>Recommended takeprofit percentages.</li><br/>
                                            <li>Reliable risk-to-reward ratios, sticking to a minimum of 1:2.</li><br/>
                                            <li>Trade alerts via the {Platform_Name} platform.</li><br/>
                                            <li>Trade alerts via Telegram.</li><br/>
                                        </ul>
                                    </p>
                                </Col>
                            </Row>
                            <br/><br/>
                            <h6 style={{fontWeight: 'bold'}}>
                                Our Distinct Approach 
                            </h6>
                            <br/><br/>
                            <p style={{textAlign: 'justify'}}>
                                While our process mirrors multitimeframe price action analysis, and various other technical analysis methods, we 
                                have a critical edge. {Platform_Name} leverages the power of machine learning to go through huge amounts of data 
                                and learn from it, inorder to make predictions based on the gained knowledge. This crucial difference amplifies 
                                the effectiveness of our platform and the quality of the trades it gives. {' '}
                                <a href='/ai-performance' style={{color: 'inherit'}}>Click here</a> for more insight on the performance of our 
                                AI models.
                            </p>
                            <br/><br/>
                            <Row style={{margin: '0px'}}>
                                <Col sm='6'>
                                    <div style={{position: 'relative', overflow: 'hidden', width: '100%', height: '400px', backgroundColor: '#D0DFE9', border: '1px solid #F9C961', borderRadius: '20px'}}>
                                        <div style={{position: 'absolute', top: '170px', left: 0, right: 0}}>
                                            Loading image...
                                        </div>
                                        <img src={HowItWorks2} onError={(e) => e.target.src = HowItWorks2} style={{position: 'absolute', right: 0, width: 'auto', minWidth: '100%', height: 'auto', minHeight: '400px'}} />
                                        <a href='https://unsplash.com/photos/MkxWUzCuYkE?utm_source=unsplash&utm_medium=referral&utm_content=creditShareLink'
                                            style={{position: 'absolute', bottom: '10px', right: '10px', color: '#ffffff', fontSize: '13px'}} target='_blank'  rel='noreferrer'
                                        >
                                            Image by Christina @ wocintechchat.com on Unsplash
                                        </a>
                                    </div>
                                </Col>
                                <Col>
                                    {
                                        this.state.on_mobile === true
                                        ? <><br/><br/></>
                                        : <><br/><br/><br/></>
                                    }
                                    <h6 style={{fontWeight: 'bold'}}>
                                        Empower Your Trading 
                                    </h6>
                                    <br/><br/>
                                    <p style={{textAlign: 'justify'}}>
                                        Whether you're a seasoned trading expert or a newcomer, our signals can serve as your 
                                        standalone guide or efficiently supplement your existing trading strategy. We aim to minimize 
                                        trading risks while maximizing rewards, all at an affordable price point.
                                    </p>
                                </Col>
                            </Row>
                            <br/><br/><br/><br/>
                            <h6 style={{fontWeight: 'bold', color: '#005fc9'}}>
                                Explore {Platform_Name} today and redefine your trading experience. 
                            </h6>
                            <br/><br/>
                            <p style={{textAlign: "left"}}>
                                Join a world where complex financial market navigations can be made simpler, smarter, and more profitable. Your 
                                journey to informed trading starts here.
                            </p>
                            <br/>
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

export default withCookies(HowItWorks);