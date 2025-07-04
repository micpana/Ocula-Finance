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
import { IsEmailStructureValid, IsPasswordStructureValid } from './input_syntax_checks'
import Signin1 from '../images/signin_1.svg'
import { FaUserCheck, FaUserLock } from 'react-icons/fa';

class Signin extends Component{
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
            email_or_username: '',
            password: ''
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

        this.Signin = (e) => {
            e.preventDefault()
            
            // initialize variable to store input validation status
            var data_checks_out = true

            // clear existing input errors if any
            this.ClearInputErrors()

            // validate input data
            if (this.state.email_or_username === ''){ this.SetInputError('email_or_username', 'required'); data_checks_out = false }
            if (this.state.password === ''){ this.SetInputError('password', 'required'); data_checks_out = false }

            // check data collection status
            if (data_checks_out === false){ // user needs to check their input data
                Notification('Check input fields for errors.', 'error')
            }else{ // send data to server
                this.LoadingOn()

                var data = new FormData()
                data.append('email_or_username', this.state.email_or_username)
                data.append('password', this.state.password)

                axios.post(Backend_Server_Address + 'signin', data, { headers: { 'access_token': null }  })
                .then((res) => {
                    let result = res.data
                    var user_access_token = result
                    // cookie expiry date construction, should expire in 90 days
                    const in90Days = new Date();
                    in90Days.setDate(in90Days.getDate() + 90);
                    // set user access token to cookies
                    const { cookies } = this.props;
                    cookies.set(Access_Token_Cookie_Name, user_access_token, { 
                        path: '/',
                        expires: in90Days,
                        sameSite: 'strict',
                        // httpOnly: true
                    })
                    // redirect to user dashboard
                    let port = (window.location.port ? ':' + window.location.port : '')
                    window.location.href = '//' + window.location.hostname + port + '/dashboard'
                }).catch((error) => {
                    console.log(error)
                    if (error.response){ // server responded with a non-2xx status code
                        let status_code = error.response.status
                        let result = error.response.data
                        var notification_message = ''
                        if(result === 'incorrect details entered'){ notification_message = "Incorrect details entered." }
                        else if (result === 'email not verified'){ notification_message = "Email address not verified. Please check your mailbox for the verification email we sent you." }
                        else if (result === 'email or username not registered'){ notification_message = "Email address / username not registered on this platform." }
                        else if (result === 'banned'){ notification_message = "User banned from accessing this platform." }
                        else{
                            notification_message = Unknown_Non_2xx_Message + ' (Error '+status_code.toString()+': '+result+')'
                        }
                        Notification(notification_message, 'error')
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
        return (
            <div>
                <Helmet>
                    <title>Signin | {Platform_Name}</title>
                    {/* <meta name="description" content="" /> */}
                </Helmet>
                <ToastContainer />
                {
                    this.state.loading === true
                    ? <LoadingScreen />
                    : this.state.network_error_screen === true
                    ? <NetworkErrorScreen error_message={this.state.network_error_message} retryFunction={this.state.retry_function} />
                    : <div>
                        <Row style={{margin: '0px'}}>
                            <Col sm='6'>
                                <img src={Signin1} onError={(e) => e.target.src = Signin1} style={{width: '100%'}} />
                                <a href='https://storyset.com/user'
                                    style={{marginTop: '10px', color: 'grey', fontSize: '13px'}} target='_blank'  rel='noreferrer'
                                >
                                    User illustrations by Storyset
                                </a>
                            </Col>
                            <Col>
                                <Container>
                                    <Form onSubmit={this.Signin}>
                                        <br/><br/><br/><br/>
                                        <h2 style={{color: '#00539C'}}>Signin</h2>
                                        <br/><br/>
                                        <Label>Email or Username <span style={{color: 'red'}}>*</span></Label>
                                        <InputGroup>
                                            <InputGroupText addonType="prepend">
                                                <FaUserCheck style={{margin:'10px'}}/>
                                            </InputGroupText>
                                            <Input style={{border: 'none', borderBottom: '1px solid #828884', backgroundColor: 'inherit'}}
                                                placeholder="Email or Username" name="email_or_username" id="email_or_username"
                                                value={this.state.email_or_username} onChange={this.HandleChange} type="text" 
                                            />
                                        </InputGroup>
                                        <InputErrors field_error_state={this.state.input_errors['email_or_username']} field_label='Email or Username' />
                                        <br/><br/>
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
                                        <br/><br/>
                                        <Button type="submit"
                                            style={{border: '1px solid #00539C', borderRadius: '20px', color: '#ffffff', fontWeight: 'bold', backgroundColor: '#00539C', width: '180px'}}
                                        >
                                            Signin
                                        </Button>
                                    </Form>
                                    <br/><br/>
                                    <a href='/forgot-password' style={{color: '#00539C'}}>
                                        Forgot your password? Click here to reset it.
                                    </a>
                                    <br/><br/>
                                    <a href='/signup' style={{color: '#00539C'}}>
                                        Not yet registered? Click here to signup.
                                    </a>
                                </Container>
                                <br/><br/><br/>
                            </Col>
                        </Row>
                    </div>
                }
            </div>
        );
    }

};

export default withCookies(Signin);