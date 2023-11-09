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
                        <div style={{backgroundColor: '#005fc9', position: 'relative'}}>
                            <div style={{backgroundColor: 'grey', opacity: 0.7, minHeight: '200px'}}></div>
                            <div style={{color: '#ffffff', position: 'absolute', top: 0, left: 0, right: 0}}>
                                <br/><br/><br/>
                                <h3 style={{fontWeight: 'bold'}}>
                                    How it works
                                </h3>
                            </div>
                        </div>
                        <Container>
                            <br/><br/>
                            <h6 style={{fontWeight: 'bold'}}>
                                Introduction
                            </h6>
                            <br/><br/>
                            <p style={{textAlign: 'left'}}>
                                Welcome to {Platform_Name} - the Advanced SAAS platform that revolutionizes the way you approach 
                                financial markets, primarily forex. Powered by cutting-edge AI and deep neural networks, our platform 
                                provides you with comprehensive forecast data for the next 105 minutes, enabling you to create a 
                                balanced risk-to-reward profile for favourable market directions. Here's how our system works.
                            </p>
                            <br/><br/>
                            <Row style={{margin: '0px'}}>
                                <Col sm='6'>
                                    <img src={HowItWorks1} style={{width: '100%', minHeight: '400px', backgroundColor: '#D0DFE9', border: '2px solid silver', borderRadius: '10px'}} />
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
                                    <p style={{textAlign: 'left'}}>
                                        <ul>
                                            <li>Potential max upmove and downmove forecasts.</li><br/>
                                            <li>Comprehensive risk-to-reward profile construction.</li><br/>
                                            <li>Enhanced support to existing trading strategies.</li><br/>
                                            <li>Simple, powerful metrics for savvy trading.</li><br/>
                                            <li>Regular updates every 15 minutes.</li><br/>
                                        </ul>
                                    </p>
                                </Col>
                            </Row>
                            <br/><br/>
                            <h6 style={{fontWeight: 'bold'}}>
                                Our Distinct Approach 
                            </h6>
                            <br/><br/>
                            <p style={{textAlign: 'left'}}>
                                While our process mirrors the statistical models employed in market finance, such as VaR and ER, we 
                                have a critical edge. {Platform_Name} leverages the power of deep neural networks to provide potential 
                                percentages moved in either direction. This crucial difference amplifies the effectiveness of our 
                                platform and the insight users gain. 
                            </p>
                            <br/><br/>
                            <Row style={{margin: '0px'}}>
                                <Col sm='6'>
                                    <img src={HowItWorks2} style={{width: '100%', minHeight: '400px', backgroundColor: '#D0DFE9', border: '2px solid silver', borderRadius: '10px'}} />
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
                                    <p style={{textAlign: 'left'}}>
                                        Whether you're a seasoned trading expert or a newcomer, our metrics can serve as your 
                                        standalone guide or efficiently supplement your existing trading strategy. We aim to minimize 
                                        trading risks while maximizing rewards, all at an affordable price point.
                                    </p>
                                </Col>
                            </Row>
                            <br/><br/>
                            <h6 style={{fontWeight: 'bold'}}>
                                Stay updated 
                            </h6>
                            <br/><br/>
                            <p style={{textAlign: 'left'}}>
                                At {Platform_Name}, we understand the dynamic nature of financial markets, which is why we update our 
                                data every 15 minutes. Stay in sync with the latest trends and make data-driven decisions on the go.
                            </p>
                            <br/><br/>
                            <h6 style={{fontWeight: 'bold'}}>
                                Explore {Platform_Name} today and redefine your trading experience. 
                            </h6>
                            <br/><br/>
                            <p style={{textAlign: "left"}}>
                                Sign up for a 14-day Free Trial now!
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

export default withCookies(HowItWorks);