import React, { Component, useReducer } from 'react';
import {
    Collapse, 
    Table, 
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
import axios from 'axios';
import { Unknown_Non_2xx_Message, Network_Error_Message, No_Network_Access_Message } from '../network_error_messages';
import LoadingScreen from './loading_screen';
import InputErrors from './input_errors';
import Notification from './notification_alert';
import NetworkErrorScreen from './network_error_screen';
import { IsEmailStructureValid, IsPasswordStructureValid } from './input_syntax_checks'

class TermsOfService extends Component{
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
                    <title>Terms Of Service | {Platform_Name}</title>
                    {/* <meta name="description" content="" /> */}
                </Helmet>
                <ToastContainer />
                {
                    this.state.loading === true
                    ? <LoadingScreen />
                    : this.state.network_error_screen === true
                    ? <NetworkErrorScreen error_message={this.state.network_error_message} retryFunction={this.state.retry_function} />
                    : <Container>
                        <br/><br/>
                        <h3 style={{color: '#00539C'}}>
                            Terms Of Service
                        </h3>
                        <br/><br/><br/>
                        <div style={{textAlign: 'left'}}>
                            <p>
                                Thank you for choosing Ocula Finance. These Terms of Service constitute a legal agreement
                                between you and Ocula Finance. <span style={{fontWeight: 'bold'}}>You</span> means you as an individual or any other entity you
                                represent on Ocula Finance, if any. <span style={{fontWeight: 'bold'}}>Us</span> or <span style={{fontWeight: 'bold'}}>we</span> or <span style={{fontWeight: 'bold'}}>this platform</span> refers to Ocula Finance. If
                                you are accepting these terms on behalf of your employer or any other entity you may represent,
                                you warrant that you have full legal authority to bind that entity to this agreement, and you are
                                agreeing to these Terms of Service on behalf of yourself and the entity you represent. If you do not
                                have the legal authority to bind the entity to this agreement then do not proceed with signing up
                                unless you choose to signup as an individual. If you have the legal authority to bind the entity,
                                please note that <span style={{fontWeight: 'bold'}}>you</span> will refer to yourself and that entity, jointly. By accepting this agreement
                                (proceeding with signup), you acknowledge that your have read and understood all the terms stated
                                in this agreement.
                            </p>
                            <p>
                                If you signup and Ocula Finance changes these Terms of Service, you will be notified via the Ocula
                                Finance platform, as well as via email, and you will be required to review and accept or reject the
                                new terms. If you accept the new terms, you can proceed with using the platform.
                            </p>
                            <br/><br/>
                            <h6 style={{fontWeight: 'bold'}}>1. Services.</h6>
                            <br/>
                            <p>
                                <span style={{fontWeight: 'bold'}}>1.1</span> <u>Services we provide.</u> Ocula Finance is a technology brand focused on using Artificial
                                Intelligence in analysing the financial markets. Our service comprises of a web based software
                                product that provides the user with detailed risk-to-reward profiles on a range of financial assets
                                supported by the software. Our software has been trained with years of historical market data to
                                determine potential maximum moves to be taken by the market in either direction. In addition to
                                that, our software continues to learn as it comes across new market data.
                            </p>
                            <br/>
                            <p style={{fontWeight: 'bold'}}>
                                IMPORTANT: Ocula Finance is not a broker, hedgefund or trading firm, therefore we do not
                                by any means accept investments from any entities, nor will we ever ask you for money
                                promising returns on our website or on any social media platform. The money users pay is a
                                subscription fee for them to access our services, and all transactions are done on our website
                                (oculafinance.com) only. Our business is a SAAS (Software As A Service) that provides
                                market insights through the use of Artificial Intelligence.
                            </p>
                            <br/>
                            <p>
                                <span style={{fontWeight: 'bold'}}>1.2</span> <u>Access and use of our services.</u> In order to use our services, you must signup using a valid email
                                address which our software will send a verification link to inorder to verify that the email address
                                that you have provided truly belongs to you. Once you have completed the email verification
                                process, you will be able to signin using the details you provided during signup. By default, every
                                new user is given 7 days of free access to our paid package, which means they’ll be able to fully
                                access all analysis done by our AI for all financial assets available on Ocula Finance. After you have
                                completed the 7 days free trial, for all the financial assets available on our platform, analysis done
                                by our AI will only be available if you have an active subscription.
                            </p>
                            <br/><br/>
                            <h6 style={{fontWeight: 'bold'}}>2. User requirements and conduct.</h6>
                            <br/>
                            <p>
                                <span style={{fontWeight: 'bold'}}>2.1</span> <u>User requirements.</u> Before signing up to use Ocula Finance, you should have at least a basic
                                knowledge of what forex trading is, what cryptocurrency trading is, how risky they both are, how to
                                open and close trades, how to place a stoploss and take profit, what a risk-to-reward ratio is, and
                                what a timeframe is. If you do not possess the stated knowledge, we advise that you seek basic
                                knowledge or any higher level of knowledge you may see fit, from the numerous reliable free or
                                paid educational sites such as Baby Pips.
                            </p>
                            <br/>
                            <p>
                                <span style={{fontWeight: 'bold'}}>2.2</span> <u>User conduct.</u> Market analysis done by our software is meant to be received and used by entities
                                registered on Ocula Finance, via their accounts. <span style={{fontWeight: 'bold'}}>Reselling or even redistributing our AI’s analysis
                                to outside entities is strictly prohibited and will result in the termination of your account even
                                if it has an active subscription.</span>
                            </p>
                            <br/><br/>
                            <h6 style={{fontWeight: 'bold'}}>3. Data Privacy</h6>
                            <br/>
                            <p>
                                To understand what data we collect from you, how we collect it, and why we collect it, refer to our
                                Privacy Policy.
                            </p>
                            <br/><br/>
                            <h6 style={{fontWeight: 'bold'}}>4. Disclaimer</h6>
                            <br/>
                            <p>
                                Ocula Finance is not a financial advisor, our software gives you market analysis based on
                                mathematical probabilities calculated by our Artificial Intelligence using market data. Section 2.1 of
                                our Terms of Service clearly states that the user should have a basic knowledge on what trading is
                                as well as the risks associated with it. Forex and Cryptocurrency trading involves significant risk to
                                your invested capital, losses can and will be encountered. <span style={{fontWeight: 'bold'}}>Ocula Finance shall not be liable for
                                any losses you may encounter, or any disputes you may encounter with the broker of your
                                choosing, or any money lost to scammers disguised as Ocula Finance (as highlighted in section
                                1.1 of our Terms of Service).</span>
                            </p>
                        </div>
                    </Container>
                }
                <br/><br/><br/>
            </div>
        );
    }

};

export default withCookies(TermsOfService);