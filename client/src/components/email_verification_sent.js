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
import { Platform_Name } from '../platform_name';
import { Backend_Server_Address } from '../backend_server_url';
import { Access_Token_Cookie_Name } from '../access_token_cookie_name';
import axios from 'axios';
import { Unknown_Non_2xx_Message, Network_Error_Message, No_Network_Access_Message } from '../network_error_messages';
import LoadingScreen from './loading_screen';
import InputErrors from './input_errors';
import Notification from './notification_alert';
import { IsEmailStructureValid, IsPasswordStructureValid } from './input_syntax_checks'
import { FaAt } from 'react-icons/fa';

class EmailVerificationSent extends Component{
    static propTypes = {
        cookies: instanceOf(Cookies).isRequired
    };
    constructor(props) { 
        super(props);
        this.state = {
            loading: false,
            input_errors: {},
            on_mobile: false,
            email: '',
            screen: 'sent', // sent / already verified / invalid / invalid account id / email already registered / account already verified 
            corrected_email: ''
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

        this.GetUserVerificationEmailByUserId = () => {
            this.setState({loading: true})

            var data = new FormData()
            data.append('account_id', this.props.match.params.account_id)

            axios.post(Backend_Server_Address + 'getUserVerificationEmailByUserId', data, { headers: { 'access_token': null }  })
            .then((res) => {
                let result = res.data
                var user_email = result
                // set user email to state
                this.setState({email: user_email, loading: false})
            }).catch((error) => {
                console.log(error)
                if (error.response){ // server responded with a non-2xx status code
                    let status_code = error.response.status
                    let result = error.response.data
                    var notification_message = ''
                    if(result === 'already verified'){ this.setState({screen: 'already verified'}) }
                    else if (result === 'invalid'){ this.setState({screen: 'invalid'}) }
                    else if (result === 'redirect to signin'){ 
                        // redirect to signin
                        let port = (window.location.port ? ':' + window.location.port : '')
                        window.location.href = '//' + window.location.hostname + port + '/signin'
                    }
                    else{
                        notification_message = Unknown_Non_2xx_Message + ' (Error '+status_code.toString()+': '+result+')'
                        Notification(notification_message, 'error')
                    }
                }else if (error.request){ // request was made but no response was received ... network error
                    Notification(Network_Error_Message, 'error')
                }else{ // error occured during request setup ... no network access
                    Notification(No_Network_Access_Message, 'error')
                }
                this.setState({loading: false})
            })
        }

        this.ResendEmailVerification = (e) => {
            e.preventDefault()
            
            this.setState({loading: true})

            var data = new FormData()
            data.append('account_id', this.props.match.params.account_id)

            axios.post(Backend_Server_Address + 'resendEmailVerification', data, { headers: { 'access_token': null }  })
            .then((res) => {
                let result = res.data
                // change screen to sent
                this.setState({screen: 'sent', loading: false})
            }).catch((error) => {
                console.log(error)
                if (error.response){ // server responded with a non-2xx status code
                    let status_code = error.response.status
                    let result = error.response.data
                    var notification_message = ''
                    if(result === 'invalid account id'){ this.setState({screen: 'invalid account id'}) }
                    else if (result === 'email already verified'){ this.setState({screen: 'email already verified'}) }
                    else{
                        notification_message = Unknown_Non_2xx_Message + ' (Error '+status_code.toString()+': '+result+')'
                        Notification(notification_message, 'error')
                    }
                }else if (error.request){ // request was made but no response was received ... network error
                    Notification(Network_Error_Message, 'error')
                }else{ // error occured during request setup ... no network access
                    Notification(No_Network_Access_Message, 'error')
                }
                this.setState({loading: false})
            })
        }

        this.CorrectRegistrationEmail = (e) => {
            e.preventDefault()
            
            // initialize variable to store input validation status
            var data_checks_out = true

            // clear existing input errors if any
            this.ClearInputErrors()

            // validate input data
            if (this.state.corrected_email === ''){ this.SetInputError('corrected_email', 'required'); data_checks_out = false }
            if (IsEmailStructureValid(this.state.corrected_email) === false){ this.SetInputError('corrected_email', 'invalid'); data_checks_out = false }

            // check data collection status
            if (data_checks_out === false){ // user needs to check their input data
                Notification('Check input fields for errors.', 'error')
            }else{ // send data to server
                this.setState({loading: true})

                var data = new FormData()
                data.append('account_id', this.props.match.params.account_id)
                data.append('email', this.state.corrected_email)

                axios.post(Backend_Server_Address + 'correctRegistrationEmail', data, { headers: { 'access_token': null }  })
                .then((res) => {
                    let result = res.data
                    // set new user email to state
                    this.setState({
                        email: this.state.corrected_email,
                        corrected_email: '',
                        screen: 'sent', 
                        loading: false
                    })
                }).catch((error) => {
                    console.log(error)
                    if (error.response){ // server responded with a non-2xx status code
                        let status_code = error.response.status
                        let result = error.response.data
                        var notification_message = ''
                        if(result === 'invalid account id'){ this.setState({screen: 'invalid account id'}) }
                        else if (result === 'email already registered'){ this.setState({screen: 'email already registered'}) }
                        else if (result === 'account already verified'){ this.setState({screen: 'account already verified'}) }
                        else{
                            notification_message = Unknown_Non_2xx_Message + ' (Error '+status_code.toString()+': '+result+')'
                            Notification(notification_message, 'error')
                        }
                    }else if (error.request){ // request was made but no response was received ... network error
                        Notification(Network_Error_Message, 'error')
                    }else{ // error occured during request setup ... no network access
                        Notification(No_Network_Access_Message, 'error')
                    }
                    this.setState({loading: false})
                })
            }
        }
    }

    Notification = (message, message_type) => { // message type -> info / success / warning / error
        const toaster = useToaster();
        
        // push notification message
        toaster.push(<Message>{message}</Message>, {
            placement: 'topCenter',
            closable: true,
            type: message_type,
            showIcon: true,
            duration: 15000
        });
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
            this.GetUserVerificationEmailByUserId()
        }
    }

    render() {
        var screen = this.state.screen
        
        return (
            <div>
                <Helmet>
                    <title>Email Verification Sent | {Platform_Name}</title>
                    {/* <meta name="description" content="" /> */}
                </Helmet>
                {
                    this.state.loading === true
                    ? <LoadingScreen />
                    : <Container>
                        <br/><br/><br/><br/>
                        {
                            screen === 'sent'
                            ? <div>
                                <h3 style={{marginTop: '30px'}}>
                                    We've sent you a verification email at <span style={{color: '#00539C'}}>{this.state.email}</span>
                                </h3>
                                <h5 style={{marginTop: '50px'}}>
                                    Follow the instructions stated in the email inorder to verify your account and gain access to {Platform_Name}.
                                </h5>
                                <h6 style={{marginTop: '70px'}}>
                                    Did not receive our email? Click the button below to resend.
                                </h6>
                                <br/>
                                <Button onClick={this.ResendEmailVerification} 
                                    style={{mborder: '1px solid #00539C', borderRadius: '20px', color: '#ffffff', fontWeight: 'bold', backgroundColor: '#00539C'}}
                                >
                                    Resend verification email
                                </Button>
                                <h6 style={{marginTop: '100px'}}>
                                    Made a typo on your email address? Correct it below.
                                </h6>
                                <br/>
                                <Label>Corrected email <span style={{color: 'red'}}>*</span></Label>
                                <InputGroup>
                                    <InputGroupText addonType="prepend">
                                        <FaAt style={{margin:'10px'}}/>
                                    </InputGroupText>
                                    <Input style={{border: 'none', borderBottom: '1px solid #828884', backgroundColor: 'inherit'}}
                                        placeholder="Corrected email" name="corrected_email" id="corrected_email"
                                        value={this.state.corrected_email} onChange={this.HandleChange} type="text" 
                                    />
                                </InputGroup>
                                <InputErrors field_error_state={this.state.input_errors['corrected_email']} field_label='Corrected email' />
                                <br/><br/><br/>
                                <Button onClick={this.CorrectRegistrationEmail} 
                                    style={{border: '1px solid #00539C', borderRadius: '20px', color: '#ffffff', fontWeight: 'bold', backgroundColor: '#00539C'}}
                                >
                                    Correct registration email
                                </Button>
                            </div>
                            : screen === 'already verified'
                            ? <div>
                                <h3 style={{marginTop: '30px'}}>
                                    The supplied email address (<span style={{color: '#00539C'}}>{this.state.email}</span>) has already been verified
                                </h3>
                                <h5 style={{marginTop: '50px'}}>
                                    <a href='/signin' style={{color: '#00539C'}}>Click here to signin.</a>
                                </h5>
                            </div>
                            : screen === 'invalid' || screen === 'invalid account id'
                            ? <div>
                                <h3 style={{marginTop: '30px'}}>
                                    The supplied email verification ID is invalid
                                </h3>
                                <h5 style={{marginTop: '50px'}}>
                                    <a href='/' style={{color: '#00539C'}}>Click here to visit our homepage instead.</a>
                                </h5>
                            </div>
                            : screen === 'email already registered'
                            ? <div>
                                <h3 style={{marginTop: '30px'}}>
                                    The supplied email address (<span style={{color: '#00539C'}}>{this.state.email}</span>) is already registered on this platform
                                </h3>
                                <Button onClick={() => this.setState({screen: 'sent'})}
                                    style={{width: '180px', marginTop: '50px', border: '1px solid #00539C', borderRadius: '20px', color: '#ffffff', fontWeight: 'bold', backgroundColor: '#00539C'}}
                                >
                                    Retry
                                </Button>
                            </div>
                            : screen === 'account already verified'
                            ? <div>
                                <h3 style={{marginTop: '30px'}}>
                                    The supplied email address (<span style={{color: '#00539C'}}>{this.state.email}</span>) is already in use on this platform
                                </h3>
                                <Button onClick={() => this.setState({screen: 'sent'})}
                                    style={{width: '180px', marginTop: '50px', border: '1px solid #00539C', borderRadius: '20px', color: '#ffffff', fontWeight: 'bold', backgroundColor: '#00539C'}}
                                >
                                    Retry
                                </Button>
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

export default withCookies(EmailVerificationSent);