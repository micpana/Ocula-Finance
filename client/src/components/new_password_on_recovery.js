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
import { useParams } from 'react-router-dom';
import { Unknown_Non_2xx_Message, Network_Error_Message, No_Network_Access_Message } from '../network_error_messages';
import LoadingScreen from './loading_screen';
import InputErrors from './input_errors';
import Notification from './notification_alert';
import NetworkErrorScreen from './network_error_screen';
import { IsEmailStructureValid, IsPasswordStructureValid } from './input_syntax_checks'
import { FaUserLock, FaKey } from 'react-icons/fa';

class NewPasswordOnRecovery extends Component{
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
            password: '',
            password_confirmation: '',
            screen: 'new password' // new password / ok / invalid token / expired / used 
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

        this.SetNewPassword = (e) => {
            e.preventDefault()
            
            // initialize variable to store input validation status
            var data_checks_out = true

            // clear existing input errors if any
            this.ClearInputErrors()

            // validate input data
            if (this.state.password === ''){ this.SetInputError('password', 'required'); data_checks_out = false }
            if (IsPasswordStructureValid(this.state.password) === false){ this.SetInputError('password', 'invalid'); data_checks_out = false }
            if (this.state.password_confirmation === ''){ this.SetInputError('password_confirmation', 'required'); data_checks_out = false }
            if (this.state.password != this.state.password_confirmation){ this.SetInputError('password_mismatch', 'invalid'); data_checks_out = false }

            // check data collection status
            if (data_checks_out === false){ // user needs to check their input data
                Notification('Check input fields for errors.', 'error')
            }else{ // send data to server
                this.LoadingOn()

                var data = new FormData()
                const {recovery_token} = useParams();
                data.append('token', recovery_token)
                data.append('password', this.state.password)

                axios.post(Backend_Server_Address + 'setNewPassword', data, { headers: { 'access_token': null }  })
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
                        else if (result === 'expired'){ this.setState({screen: 'expired'}) }
                        else if (result === 'used'){ this.setState({screen: 'used'}) }
                        else if (result === 'invalid password structure'){ notification_message = "The password you've entered does not have a valid structure."; Notification(notification_message, 'invalid') }
                        else{
                            notification_message = Unknown_Non_2xx_Message + ' (Error '+status_code.toString()+': '+result+')'
                            Notification(notification_message, 'error')
                        }
                    }else if (error.request){ // request was made but no response was received ... network error
                        Notification(Network_Error_Message, 'error')
                    }else{ // error occured during request setup ... no network access
                        Notification(No_Network_Access_Message, 'error')
                    }
                    this.LoadingOff()
                })
            }
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
        }
    }

    render() {
        var screen = this.state.screen
        
        return (
            <div>
                <Helmet>
                    <title>New Password | {Platform_Name}</title>
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
                            screen === 'new password'
                            ? <div>
                                <h6>
                                    Create a new password below
                                </h6>
                                <br/><br/>
                                <Row style={{margin: '0px'}}>
                                    <Col sm='6'>
                                        <Label>Password <span style={{color: 'red'}}>*</span></Label>
                                        <InputGroup>
                                            <InputGroupText addonType="prepend">
                                                <FaUserLock style={{margin:'10px'}}/>
                                            </InputGroupText>
                                            <Input style={{border: 'none', borderBottom: '1px solid #828884', backgroundColor: 'inherit'}}
                                                placeholder="Password" name="password" id="password"
                                                value={this.state.password} onChange={this.HandleChange} type="password" 
                                            />
                                        </InputGroup>
                                        <InputErrors field_error_state={this.state.input_errors['password']} field_label='Password' />
                                        <br/>
                                    </Col>
                                    <Col>
                                        <Label>Password Confirmation<span style={{color: 'red'}}>*</span></Label>
                                        <InputGroup>
                                            <InputGroupText addonType="prepend">
                                                <FaKey style={{margin:'10px'}}/>
                                            </InputGroupText>
                                            <Input style={{border: 'none', borderBottom: '1px solid #828884', backgroundColor: 'inherit'}}
                                                placeholder="Password Confirmation" name="password_confirmation" id="password_confirmation"
                                                value={this.state.password_confirmation} onChange={this.HandleChange} type="password" 
                                            />
                                        </InputGroup>
                                        <InputErrors field_error_state={this.state.input_errors['password_confirmation']} field_label='Password Confirmation' />
                                        <br/>
                                    </Col>
                                </Row>
                                <br/><br/>
                                <Button onClick={this.SetNewPassword} 
                                    style={{border: '1px solid #00539C', borderRadius: '20px', color: '#ffffff', fontWeight: 'bold', backgroundColor: '#00539C'}}
                                >
                                    Save new password
                                </Button>
                            </div>
                            : screen === 'ok'
                            ? <div>
                                <h3 style={{marginTop: '30px'}}>
                                    Your password has been reset successfully.
                                </h3>
                                <h5 style={{marginTop: '50px'}}>
                                    <a href='/signin' style={{color: '#00539C'}}>Click here to signin.</a>
                                </h5>
                            </div>
                            : screen === 'invalid token'
                            ? <div>
                                <h3 style={{marginTop: '30px'}}>
                                    Invalid password reset token.
                                </h3>
                                <h5 style={{marginTop: '50px'}}>
                                    <a style={{color: '#00539C'}}>Make sure you've followed the instructions stated in the password recovery email you received.</a>
                                </h5>
                            </div>
                            : screen === 'expired'
                            ? <div>
                                <h3 style={{marginTop: '30px'}}>
                                    This password reset token expired before its use.
                                </h3>
                                <h5 style={{marginTop: '50px'}}>
                                    <a href='/forgot-password' style={{color: '#00539C'}}>Click here to generate another one.</a>
                                </h5>
                            </div>
                            : screen === 'used'
                            ? <div>
                                <h3 style={{marginTop: '30px'}}>
                                    This password reset token has been used already.
                                </h3>
                                <h5 style={{marginTop: '50px'}}>
                                    <a href='/signin' style={{color: '#00539C'}}>Click here to signin.</a>
                                </h5>
                            </div>
                            : <div>
                                <h3 style={{marginTop: '30px'}}>
                                    An unknown error has occured.
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

export default withCookies(NewPasswordOnRecovery);