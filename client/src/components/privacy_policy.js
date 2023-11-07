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

class PrivacyPolicy extends Component{
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
                    <title>Privacy Policy | {Platform_Name}</title>
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
                            Privacy Policy
                        </h3>
                        <br/><br/><br/>
                        <div style={{textAlign: 'left'}}>
                            <p>
                                The privacy of your information is very important to us and our transparency as to how we collect
                                and handle your information is important too. This policy will help you understand:
                                <br/><br/>
                                <ul>
                                    <li>
                                        How we collect your information
                                    </li>
                                    <li>
                                        What information we collect
                                    </li>
                                    <li>
                                        How we use the information we collect
                                    </li>
                                    <li>
                                        How we store and secure your information
                                    </li>
                                </ul>
                            </p>
                            <br/><br/>
                            <h6 style={{fontWeight: 'bold'}}>How we collect your information</h6>
                            <br/>
                            <p>
                                We will obtain your personal information when you signup. Furthermore, we may collect more
                                information from you when you contact us in instances where the information will be required to
                                assist you.
                            </p>
                            <br/><br/>
                            <h6 style={{fontWeight: 'bold'}}>What information we collect</h6>
                            <br/>
                            <p>
                                When you signup, we collect your firstname, lastname, email address, country and phonenumber.
                                When you contact us with queries that might require more personal information we will inform you
                                about it first and why, we will only collect it if you disclose it. For example, if you paid for a
                                subscription but your subscription wasn't automatically activated by our software, we will ask for
                                your payment details.
                            </p>
                            <br/><br/>
                            <h6 style={{fontWeight: 'bold'}}>How we use information we collect</h6>
                            <br/>
                            <p>
                                The information you provide during signup is mainly used for identification, contact and
                                authentication purposes. For example, we use the email address you give us to identify your
                                account, you'll be asked for it when you login, furthermore we will use it to send you subscription
                                reminders, important notices, alerts when we change our Terms of Service and Privacy Policy, and
                                to reset your password. We also use your information for statistical analysis, for example, to see
                                how many users we have per country.
                            </p>
                            <br/><br/>
                            <h6 style={{fontWeight: 'bold'}}>How we store and secure your information</h6>
                            <br/>
                            <p>
                                We use various standards of encryption to protect your information and where we store it. While we
                                do our best to implement safeguards to protect your information, you need to understand that no
                                security system is impenetrable, and due to the infrastructure of the internet, we cannot guarantee
                                that the information being transmitted through the internet or stored on our systems is totaly safe
                                from intruders.
                            </p>
                        </div>
                    </Container>
                }
                <br/><br/><br/>
            </div>
        );
    }

};

export default withCookies(PrivacyPolicy);