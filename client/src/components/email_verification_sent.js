import React, { Component, useReducer } from 'react';
import {
    Collapse, 
    Nav, NavItem, NavLink, 
    UncontrolledDropdown, Dropdown, DropdownToggle, DropdownMenu, DropdownItem, 
    Input, InputGroup, InputGroupAddon,
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
import { Unknown_Non_2xx_Message, Network_Error_Message, No_Network_Access_Message } from '../network_error_messages';
import LoadingScreen from './loading_screen';
import InputErrors from './input_errors';
import { Message, useToaster } from "rsuite";
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
            email: '',
            screen: 'sent', // sent / already verified / invalid / invalid account id / email already registered / account already verified 
            corrected_email: ''
        };

        this.HandleChange = (e) => {
            this.setState({[e.target.name]: e.target.value});
        };

        this.SetInputError = (field, error) => { // error -> required / invalid
            // if field error state doesn't already exist
            if (this.state.input_errors[field] == undefined){
                // new error
                var new_error = {
                    [field]: error
                }

                // existing errors + new
                var updated_input_errors = {
                    ...this.state.input_errors,
                    ...new_error
                }

                // update state
                this.setState({input_errors: updated_input_errors})
            }else{ // field error state already exists
                // existing errors
                var existing_errors = this.state.input_errors

                // existing errors modified
                existing_errors[field] = error

                // update state
                this.setState({input_errors: existing_errors})
            }
        }

        this.ClearInputErrors = () => {
            this.setState({input_errors: {}})
        }

        this.IsEmailStructureValid = (email) => {
            // regex
            const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

            // return true if email has proper structure
            return regex.test(email)
        }

        this.Notification = (message, message_type) => { // message type -> info / success / warning / error
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
                        this.Notification(notification_message, 'error')
                    }
                }else if (error.request){ // request was made but no response was received ... network error
                    this.Notification(Network_Error_Message, 'error')
                }else{ // error occured during request setup ... no network access
                    this.Notification(No_Network_Access_Message, 'error')
                }
                this.setState({loading: false})
            })
        }

        this.ResendEmailVerification = () => {
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
                        this.Notification(notification_message, 'error')
                    }
                }else if (error.request){ // request was made but no response was received ... network error
                    this.Notification(Network_Error_Message, 'error')
                }else{ // error occured during request setup ... no network access
                    this.Notification(No_Network_Access_Message, 'error')
                }
                this.setState({loading: false})
            })
        }

        this.CorrectRegistrationEmail = () => {
            // initialize variable to store input validation status
            var data_checks_out = true

            // clear existing input errors if any
            this.ClearInputErrors()

            // validate input data
            if (this.state.corrected_email === ''){ this.SetInputError('corrected_email', 'required'); data_checks_out = false }
            if (this.IsEmailStructureValid(this.state.corrected_email) === false){ this.SetInputError('corrected_email', 'invalid'); data_checks_out = false }

            // check data collection status
            if (data_checks_out === false){ // user needs to check their input data
                this.Notification('Check input fields for errors.', 'error')
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
                            this.Notification(notification_message, 'error')
                        }
                    }else if (error.request){ // request was made but no response was received ... network error
                        this.Notification(Network_Error_Message, 'error')
                    }else{ // error occured during request setup ... no network access
                        this.Notification(No_Network_Access_Message, 'error')
                    }
                    this.setState({loading: false})
                })
            }
        }
    }

    componentDidMount() {
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
                        {
                            screen === 'sent'
                            ? <div>
                                <br/>
                                <h3 style={{marginTop: '150px'}}>
                                    We've sent you a verification email at <span style={{color: '#00539C'}}>{this.state.email}</span>
                                </h3>
                                <h5 style={{marginTop: '50px'}}>
                                    Follow the instructions stated in the email inorder to verify your account and gain access to {Platform_Name}.
                                </h5>
                                <h6 style={{marginTop: '100px'}}>
                                    Did not receive our email? Click the button below to resend.
                                </h6>
                                <br/>
                                <Button onClick={this.ResendEmailVerification} 
                                    style={{marginTop: '50px', border: '1px solid #00539C', borderRadius: '20px', color: '#ffffff', fontWeight: 'bold', backgroundColor: '#00539C'}}
                                >
                                    Resend verification email
                                </Button>
                                <h6 style={{marginTop: '100px'}}>
                                    Made a typo on your email address? Correct it below.
                                </h6>
                                <br/><br/>
                                <Label>Corrected email <span style={{color: 'red'}}>*</span></Label>
                                <InputGroup>
                                    <InputGroupAddon addonType="prepend">
                                        <FaAt style={{margin:'10px'}}/>
                                    </InputGroupAddon>
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
                                <br/>
                                <h3 style={{marginTop: '150px'}}>
                                    The supplied email address (<span style={{color: '#00539C'}}>{this.state.email}</span>) has already been verified
                                </h3>
                                <h5 style={{marginTop: '50px'}}>
                                    <a href='/signin' style={{color: 'inherit'}}>Click here to signin.</a>
                                </h5>
                            </div>
                            : screen === 'invalid' || screen === 'invalid account id'
                            ? <div>
                                <br/>
                                <h3 style={{marginTop: '150px'}}>
                                    The supplied email verification ID is invalid
                                </h3>
                                <h5 style={{marginTop: '50px'}}>
                                    <a href='/' style={{color: 'inherit'}}>Click here to visit our homepage instead.</a>
                                </h5>
                            </div>
                            : screen === 'email already registered'
                            ? <div>
                                <br/>
                                <h3 style={{marginTop: '150px'}}>
                                    The supplied email address (<span style={{color: '#00539C'}}>{this.state.email}</span>) is already registered on this platform
                                </h3>
                                <Button onClick={() => this.setState({screen: 'sent'})}
                                    style={{marginTop: '50px', border: '1px solid #00539C', borderRadius: '20px', color: '#ffffff', fontWeight: 'bold', backgroundColor: '#00539C'}}
                                >
                                    Retry
                                </Button>
                            </div>
                            : screen === 'account already verified'
                            ? <div>
                                <br/>
                                <h3 style={{marginTop: '150px'}}>
                                    The supplied email address (<span style={{color: '#00539C'}}>{this.state.email}</span>) is already in use on this platform
                                </h3>
                                <Button onClick={() => this.setState({screen: 'sent'})}
                                    style={{marginTop: '50px', border: '1px solid #00539C', borderRadius: '20px', color: '#ffffff', fontWeight: 'bold', backgroundColor: '#00539C'}}
                                >
                                    Retry
                                </Button>
                            </div>
                            : <div>
                                <br/>
                                <h3 style={{marginTop: '150px'}}>
                                    An unknown error has occured
                                </h3>
                                <h5 style={{marginTop: '50px'}}>
                                    <a href='/' style={{color: 'inherit'}}>Click here to visit our homepage instead.</a>
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