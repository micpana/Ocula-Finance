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

class Pricing extends Component{
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
                    <title>Pricing | {Platform_Name}</title>
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
                                Pricing
                            </h3>
                            <br/>
                            <h5>Uncover the Value of {Platform_Name}</h5>
                        </div>
                        <Container>
                            <br/><br/>
                            <h6>Discover our affordable plans that position your trading decisions for success.</h6>
                            <br/><br/>
                            <p style={{textAlign: 'justify'}}>
                                Welcome to the {Platform_Name} pricing page. Our advanced AI-powered platform provides high quality trade entries 
                                at cost-effective rates, empowering traders to enhance their trading strategies with decisive data. Analyzing 
                                mostly forex markets, our system provides trades accompanied by their stoploss and takeprofit percentages, with 
                                a maximum recommended holding time of 3.5 hours. Our AI uses reliable risk-to-reward ratios, sticking to a minimum 
                                of 1:2, ensuring that you remain profitable in the longrun.
                            </p>
                            <br/><br/><br/>
                            <Row style={{margin: '0px'}}>
                                <Col sm='4'>
                                    <Row style={{margin: '0px', minHeight: '178px', backgroundColor: '#D0DFE9', borderTopLeftRadius: '20px', borderTopRightRadius: '20px'}}>
                                        <Container style={{textAlign: 'left'}}>
                                            <br/><br/>
                                            <h6 style={{fontWeight: 'bolder'}}>
                                                FREE TRIAL
                                            </h6>
                                            <br/>
                                            <Row style={{margin: '0px'}}>
                                                <h3 style={{fontWeight: 'bold'}}>
                                                    $ 0.00
                                                </h3>
                                                For only 7 days
                                            </Row>
                                            <br/><br/>
                                        </Container>
                                    </Row>
                                    <Row style={{margin: '0px', minHeight: '437px', backgroundColor: '#EEECEC', borderBottomLeftRadius: '20px', borderBottomRightRadius: '20px'}}>
                                        <Container style={{textAlign: 'left'}}>
                                            <br/><br/><br/>
                                            <ul>
                                                <li>Predicted buy and sell trade entries.</li><br/>
                                                <li>Recommended stoploss percentages.</li><br/>
                                                <li>Recommended takeprofit percentages.</li><br/>
                                                <li>Reliable risk-to-reward ratios, sticking to a minimum of 1:2.</li><br/>
                                                <li>Trade alerts via the {Platform_Name} platform.</li><br/>
                                                <li>Trade alerts via Telegram.</li><br/>
                                            </ul>
                                            <br/><br/><br/>
                                            <div style={{textAlign: 'center'}}>
                                                <Button href=''
                                                    style={{border: '1px solid #005fc9', borderRadius: '20px', backgroundColor: '#ffffff', color: 'inherit'}}
                                                >
                                                    Subscribe now
                                                </Button>
                                            </div>
                                            <br/><br/>
                                        </Container>
                                    </Row>
                                    <br/><br/>
                                </Col>
                                <Col sm='4'>
                                    <Row style={{margin: '0px', minHeight: '178px', backgroundColor: '#005fc9', color: '#ffffff', borderTopLeftRadius: '20px', borderTopRightRadius: '20px'}}>
                                        <Container style={{textAlign: 'left'}}>
                                            <br/><br/>
                                            <h6 style={{fontWeight: 'bolder'}}>
                                                MONTHLY
                                            </h6>
                                            <br/>
                                            <Row style={{margin: '0px'}}>
                                                <h3 style={{fontWeight: 'bold'}}>
                                                    $ 10.00
                                                </h3>
                                                /Month
                                            </Row>
                                            <br/><br/>
                                        </Container>
                                    </Row>
                                    <Row style={{margin: '0px', minHeight: '437px', backgroundColor: '#EEECEC', borderBottomLeftRadius: '20px', borderBottomRightRadius: '20px'}}>
                                        <Container style={{textAlign: 'left'}}>
                                            <br/><br/><br/>
                                            <ul>
                                                <li>Predicted buy and sell trade entries.</li><br/>
                                                <li>Recommended stoploss percentages.</li><br/>
                                                <li>Recommended takeprofit percentages.</li><br/>
                                                <li>Reliable risk-to-reward ratios, sticking to a minimum of 1:2.</li><br/>
                                                <li>Trade alerts via the {Platform_Name} platform.</li><br/>
                                                <li>Trade alerts via Telegram.</li><br/>
                                            </ul>
                                            <br/><br/><br/>
                                            <div style={{textAlign: 'center'}}>
                                                <Button href=''
                                                    style={{border: '1px solid #005fc9', borderRadius: '20px', backgroundColor: '#005fc9', color: '#ffffff'}}
                                                >
                                                    Subscribe now
                                                </Button>
                                            </div>
                                            <br/><br/>
                                        </Container>
                                    </Row>
                                    <br/><br/>
                                </Col>
                                <Col sm='4'>
                                    <Row style={{margin: '0px', minHeight: '178px', backgroundColor: '#D0DFE9', borderTopLeftRadius: '20px', borderTopRightRadius: '20px'}}>
                                        <Container style={{textAlign: 'left'}}>
                                            <br/><br/>
                                            <h6 style={{fontWeight: 'bolder'}}>
                                                YEARLY
                                            </h6>
                                            <br/>
                                            <Row style={{margin: '0px'}}>
                                                <h3 style={{fontWeight: 'bold'}}>
                                                    $ 96.00
                                                </h3>
                                                /Year
                                            </Row>
                                            <br/><br/>
                                        </Container>
                                    </Row>
                                    <Row style={{margin: '0px', minHeight: '437px', backgroundColor: '#EEECEC', borderBottomLeftRadius: '20px', borderBottomRightRadius: '20px'}}>
                                        <Container style={{textAlign: 'left'}}>
                                            <br/><br/><br/>
                                            <ul>
                                                <li>Predicted buy and sell trade entries.</li><br/>
                                                <li>Recommended stoploss percentages.</li><br/>
                                                <li>Recommended takeprofit percentages.</li><br/>
                                                <li>Reliable risk-to-reward ratios, sticking to a minimum of 1:2.</li><br/>
                                                <li>Trade alerts via the {Platform_Name} platform.</li><br/>
                                                <li>Trade alerts via Telegram.</li><br/>
                                            </ul>
                                            <br/><br/><br/>
                                            <div style={{textAlign: 'center'}}>
                                                <Button href=''
                                                    style={{border: '1px solid #005fc9', borderRadius: '20px', backgroundColor: '#ffffff', color: 'inherit'}}
                                                >
                                                    Subscribe now
                                                </Button>
                                            </div>
                                            <br/><br/>
                                        </Container>
                                    </Row>
                                    <br/><br/>
                                </Col>
                            </Row>
                            <br/>
                            <p style={{textAlign: 'justify'}}>
                                Our goal is to equip traders with a simple yet powerful tool in an affordable manner, and that’s 
                                reflected in our pricing structure. {Platform_Name}’s pricing is designed to accommodate traders of all 
                                scales - from budding enthusiasts to seasoned professionals. We have designed a straightforward and 
                                transparent pricing system that ensures you get the most out of your trading experience. We invite you 
                                to explore our versatile pricing options to find a plan that suits your trading needs best. Please note that 
                                all our pricing plans offer full access to our AI-driven forecasts.
                            </p>
                        </Container>
                    </div>
                }
                <br/><br/><br/>
            </div>
        );
    }

};

export default withCookies(Pricing);