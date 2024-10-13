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
import AboutUs1 from '../images/about_us_1.jpg'
import AboutUs2 from '../images/about_us_2.jpg'
import AboutUs3 from '../images/about_us_3.jpg'
import AboutUs4 from '../images/about_us_4.jpg'
import AboutUs5 from '../images/about_us_5.jpg'

class AboutUs extends Component{
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
                    <title>About Us | {Platform_Name}</title>
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
                                About us
                            </h3>
                        </div>
                        <Container>
                            <br/><br/>
                            <h6 style={{fontWeight: 'bold'}}>
                                {Platform_Name}
                            </h6>
                            <br/><br/>
                            <p style={{textAlign: 'justify'}}>
                                Welcome to {Platform_Name} - Your Intelligent Forex Trading Partner. We leverage Artificial Intelligence to 
                                perform deep analysis of financial markets, particularly the forex markets. 
                            </p>
                            <br/><br/>
                            <Row>
                                <Col sm='6'>
                                    <div style={{position: 'relative', overflow: 'hidden', width: '100%', height: '400px', backgroundColor: '#D0DFE9', border: '1px solid #F9C961', borderRadius: '20px'}}>
                                        <div style={{position: 'absolute', top: '170px', left: 0, right: 0}}>
                                            Loading image...
                                        </div>
                                        <img src={AboutUs1} onError={(e) => e.target.src = AboutUs1} style={{position: 'absolute', right: 0, width: 'auto', minWidth: '100%', height: 'auto', minHeight: '400px'}} />
                                    </div>
                                    <br/><br/><br/>
                                </Col>
                                <Col>
                                    <p style={{textAlign: 'justify'}}>
                                        Our SAAS platform employs sophisticated AI models to provide high probability trading signals. Our AI continuously 
                                        analyses the current market dynamics in search of good trading opportunities, and alerts 
                                        our users if it finds any.
                                    </p>
                                    <p style={{textAlign: 'justify'}}>
                                        Taking a cue from established price action and technical analysis methods, we’ve upped the game by 
                                        implementing machine learning. This approach provides more precision in selecting reliable entry points.
                                    </p>
                                    <br/>
                                    <p style={{textAlign: 'justify'}}>
                                        Whether you're deciding to use the provided trades as sole guides, or you're integrating them with 
                                        existing trading strategies, our goal remains the same - to simplify the analysis of vast amounts of 
                                        complex data, and provide traders with simplified high probability trading signals, offering them a 
                                        reliable edge in the financial markets. Our vision is to aid traders in minimizing risk and maximizing 
                                        rewards, all in an affordable manner. {' '}
                                        <a href='/ai-performance' style={{color: 'inherit'}}>Click here</a> for more insight on the performance 
                                        of our AI models.
                                    </p>
                                    <br/><br/><br/>
                                </Col>
                            </Row>
                            <h6 style={{fontWeight: 'bold', color: '#005fc9'}}>
                                Explore {Platform_Name} today and redefine your trading experience. 
                            </h6>
                            <br/><br/>
                            <p style={{textAlign: 'left'}}>
                                Join {Platform_Name} today and optimize your Forex Trading with the ultimate support of AI-powered 
                                analysis. We believe that technology and analytics should be affordable, simple, and impactful, 
                                offering each of our users more control over their trades.
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

export default withCookies(AboutUs);