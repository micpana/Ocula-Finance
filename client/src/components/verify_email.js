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
import axios from 'axios';
import { Unknown_Non_2xx_Message, Network_Error_Message, No_Network_Access_Message } from '../network_error_messages';
import LoadingScreen from './loading_screen';
import InputErrors from './input_errors';
import Notification from './notification_alert';
import NetworkErrorScreen from './network_error_screen';

class VerifyEmail extends Component{
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
            on_mobile: false,
            screen: 'ok' // ok / invalid token / used / expired
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

        this.VerifyEmail = () => {
            this.LoadingOn()
            this.NetworkErrorScreenOff()

            var data = new FormData()
            const path = window.location.pathname.split('/')
            const verification_token = path[path.length -1]
            data.append('token', verification_token)

            axios.post(Backend_Server_Address + 'verifyEmail', data, { headers: { 'access_token': null }  })
            .then((res) => {
                let result = res.data
                // set screen to ok
                this.setState({screen: 'ok'})
                this.LoadingOff()
            }).catch((error) => {
                console.log(error)
                if (error.response){ // server responded with a non-2xx status code
                    let status_code = error.response.status
                    let result = error.response.data
                    var notification_message = ''
                    if(result === 'invalid token'){ this.setState({screen: 'invalid token'}) }
                    else if (result === 'used'){ this.setState({screen: 'used'}) }
                    else if (result === 'expired'){ this.setState({screen: 'expired'}) }
                    else{
                        notification_message = Unknown_Non_2xx_Message + ' (Error '+status_code.toString()+': '+result+')'
                        Notification(notification_message, 'error')
                        this.NetworkErrorScreenOn(notification_message, this.VerifyEmail)
                    }
                }else if (error.request){ // request was made but no response was received ... network error
                    Notification(Network_Error_Message, 'error')
                    this.NetworkErrorScreenOn(Network_Error_Message, this.VerifyEmail)
                }else{ // error occured during request setup ... no network access
                    Notification(No_Network_Access_Message, 'error')
                    this.NetworkErrorScreenOn(No_Network_Access_Message, this.VerifyEmail)
                }
                this.LoadingOff()
            })
        }
    }

    componentDidMount() {
        if( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
            this.setState({
                on_mobile: true
            })
        }

        // check access token existance
        const { cookies } = this.props;
        if(cookies.get(Access_Token_Cookie_Name) != null){
            let port = (window.location.port ? ':' + window.location.port : '');
            window.location.href = '//' + window.location.hostname + port + '/dashboard';
        }else{
            this.VerifyEmail()
        }
    }

    render() {
        var screen = this.state.screen

        return (
            <div>
                <Helmet>
                    <title>Verify Email | {Platform_Name}</title>
                    {/* <meta name="description" content="" /> */}
                </Helmet>
                <ToastContainer />
                {
                    this.state.loading === true
                    ? <LoadingScreen />
                    : this.state.network_error_screen === true
                    ? <NetworkErrorScreen error_message={this.state.network_error_message} retryFunction={this.state.retry_function} />
                    : <Container>
                        <br/><br/><br/><br/>
                        {
                            screen === 'ok'
                            ? <div>
                                <h3 style={{marginTop: '30px'}}>
                                    Your email has been verified successfully.
                                </h3>
                                <h5 style={{marginTop: '50px'}}>
                                    <a href='/signin' style={{color: '#00539C'}}>Click here to signin.</a>
                                </h5>
                            </div>
                            : screen === 'invalid token'
                            ? <div>
                                <h3 style={{marginTop: '30px'}}>
                                    Invalid verification token.
                                </h3>
                                <h5 style={{marginTop: '50px'}}>
                                    <a style={{color: '#00539C'}}>Make sure you've completed the signup process and clicked the link we sent to the email address you provided upon signing up.</a>
                                </h5>
                            </div>
                            : screen === 'used'
                            ? <div>
                                <h3 style={{marginTop: '30px'}}>
                                    This verification token has already been used.
                                </h3>
                                <h5 style={{marginTop: '50px'}}>
                                    <a href='/signin' style={{color: '#00539C'}}>Click here to signin.</a>
                                </h5>
                            </div>
                            : screen === 'expired'
                            ? <div>
                                <h3 style={{marginTop: '30px'}}>
                                    This verification token expired before its use.
                                </h3>
                                <h5 style={{marginTop: '50px'}}>
                                    <a href='/signin' style={{color: '#00539C'}}>Click here to attemp a signin and another one will be generated for you.</a>
                                </h5>
                            </div>
                            : <div>
                                <h3 style={{marginTop: '30px'}}>
                                    An unknown error has occured
                                </h3>
                                <h5 style={{marginTop: '50px'}}>
                                    <a href='/' style={{color: '#00539C'}}>Click here to visit our homepage instead.</a>
                                </h5>
                            </div>
                        }
                    </Container>
                }
                <br/><br/><br/>
            </div>
        );
    }

};

export default withCookies(VerifyEmail);