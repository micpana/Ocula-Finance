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
import { IsEmailStructureValid, IsPasswordStructureValid } from './input_syntax_checks'
import ContactUs1 from '../images/contact_us_1.svg'
import { FaUserAlt, FaAt, FaRegFolderOpen, FaEnvelopeOpenText } from 'react-icons/fa';
import * as emailjs from 'emailjs-com'
import { EmailJsServiceID, EmailJsTemplateID, EmailJsAPIKey } from '../credentials'
import {Facebook, X, Instagram, LinkedIn, Telegram } from '../social_links'
import { FaMailBulk, Whatsapp, FaTelegram, FaPhone, FaSearchLocation, FaFacebook, FaTwitter, FaLinkedin, FaInstagram, FaWhatsapp, FaLocationArrow, FaPhoneAlt } from 'react-icons/fa';

class ContactUs extends Component{
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
            name: '',
            email: '',
            subject: '',
            message: ''
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

        this.GetInTouch = (e) => {
            e.preventDefault()
            
            // initialize variable to store input validation status
            var data_checks_out = true

            // clear existing input errors if any
            this.ClearInputErrors()

            // validate input data
            if (this.state.name === ''){ this.SetInputError('name', 'required'); data_checks_out = false }
            if (this.state.email === ''){ this.SetInputError('email', 'required'); data_checks_out = false }
            if (IsEmailStructureValid(this.state.email) === false){ this.SetInputError('email', 'invalid'); data_checks_out = false }
            if (this.state.subject === ''){ this.SetInputError('subject', 'required'); data_checks_out = false }
            if (this.state.message === ''){ this.SetInputError('message', 'required'); data_checks_out = false }

            // check data collection status
            if (data_checks_out === false){ // user needs to check their input data
                Notification('Check input fields for errors.', 'error')
            }else{ // send data to server
                this.LoadingOn()

                // get message and replace new line characters with line breaks
                // let message = this.state.message.replace('\n', '<br/>')
        
                // template parameters
                let templateParams = {
                    from_name: this.state.firstname + ' ' + this.state.lastname,
                    to_name: {Platform_Name},
                    reply_to: this.state.email,
                    subject: this.state.subject,
                    message: this.state.message,
                }
        
                // send email
                try{
                    emailjs.send(
                        EmailJsServiceID,
                        EmailJsTemplateID,
                        templateParams,
                        EmailJsAPIKey
                    )
                    Notification('Your message has been submitted successfully.', 'success')
                    window.location.reload()
                }catch(err){
                    console.log(err)
                    Notification('Something went wrong while trying to submit your message. Please try again.', 'error')
                }
                this.LoadingOff()
            }
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
                    <title>Contact Us | {Platform_Name}</title>
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
                                Contact us
                            </h3>
                        </div>
                        <Container>
                            <br/><br/>
                            <h6 style={{fontWeight: 'bold'}}>We're here to help</h6>
                            <br/><br/>
                            <p style={{textAlign: 'left'}}>
                                At Ocula Finance, we're committed to providing traders with innovative, data-driven solutions for more 
                                informed trading decisions. If you have any questions, need more information, or require support, 
                                don't hesitate to get in touch.
                            </p>
                            <br/><br/>
                            <Row style={{margin: '0px'}}>
                                <Col sm='6'>
                                    <img src={ContactUs1} onError={(e) => e.target.src = ContactUs1} style={{width: '100%', minHeight: '400px', backgroundColor: '#D0DFE9', border: '1px solid #F9C961', borderRadius: '10px'}}/>
                                    <br/><br/>
                                </Col>
                                <Col>
                                    <br/><br/><br/>
                                    <h6 style={{fontWeight: 'bold'}}>
                                        Contact Information
                                    </h6>
                                    <br/><br/>
                                    <Row style={{margin: '0px', textAlign: 'left'}}>
                                        <Col sm='6'>
                                            <span style={{fontWeight: 'bold'}}>Email:</span> 
                                            <br/>
                                        </Col>
                                        <Col>
                                            <a href="mailto:support@oculafinance.com" style={{color: 'inherit'}}>
                                                support@oculafinance.com
                                            </a>
                                            <br/><br/>
                                        </Col>
                                    </Row>
                                    <Row style={{margin: '0px', textAlign: 'left'}}>
                                        <Col sm='6'>
                                            <span style={{fontWeight: 'bold'}}>WhatsApp:</span>
                                            <br/>
                                        </Col>
                                        <Col>
                                            <a href="https://wa.me/263784111412" style={{color: 'inherit'}}>
                                                +263 784 111 412
                                            </a>
                                            <br/><br/>
                                        </Col>
                                    </Row>
                                    <Row style={{margin: '0px', textAlign: 'left'}}>
                                        <Col sm='6'>
                                            <span style={{fontWeight: 'bold'}}>Calls:</span>
                                            <br/>
                                        </Col>
                                        <Col>
                                            <a href="tel:" style={{color: 'inherit'}}>
                                                +263 784 111 412
                                            </a>
                                            <br/><br/>
                                        </Col>
                                    </Row>
                                    <br/>
                                    <Row style={{margin: '0px'}}>
                                        <Col xs=''>
                                            <a href={Facebook} target='_blank' style={{color: 'inherit'}}>
                                                <FaFacebook />
                                            </a>
                                        </Col>
                                        <Col xs=''>
                                            <a href={X} target='_blank' style={{color: 'inherit'}}>
                                                <FaTwitter /> 
                                            </a>
                                        </Col>
                                        <Col xs=''>
                                            <a href={Instagram} target='_blank' style={{color: 'inherit'}}>
                                                <FaInstagram /> 
                                            </a>
                                        </Col>
                                        <Col xs=''>
                                            <a href={LinkedIn} target='_blank' style={{color: 'inherit'}}>
                                                <FaLinkedin /> 
                                            </a>
                                        </Col>
                                        <Col xs=''>
                                            <a href={Telegram} target='_blank' style={{color: 'inherit'}}>
                                                <FaTelegram /> 
                                            </a>
                                        </Col>
                                    </Row>
                                    <br/><br/>
                                </Col>
                            </Row>
                            <br/>
                            <h6 style={{fontWeight: 'bold'}}>
                                Get In Touch
                            </h6>
                            <br/><br/>
                            <p>
                                Use the form below to send us your questions, comments or feedback. We aim to respond within 24 hours.
                            </p>
                            <br/>
                            <Form onSubmit={this.GetInTouch}>
                                <Row style={{margin: '0px'}}>
                                    <Col sm='6'>
                                        <Label style={{fontWeight: 'bold'}}>Name <span style={{color: 'red'}}>*</span></Label>
                                        <InputGroup>
                                            <InputGroupText>
                                                <FaUserAlt style={{margin:'10px'}}/>
                                            </InputGroupText>
                                            <Input style={{backgroundColor: 'inherit'}}
                                                placeholder="Name" name="name" id="name"
                                                value={this.state.name} onChange={this.HandleChange} type="text" 
                                            />
                                        </InputGroup>
                                        <InputErrors field_error_state={this.state.input_errors['name']} field_label='Name' />
                                        <br/><br/>
                                    </Col>
                                    <Col>
                                        <Label style={{fontWeight: 'bold'}}>Email <span style={{color: 'red'}}>*</span></Label>
                                        <InputGroup>
                                            <InputGroupText>
                                                <FaAt style={{margin:'10px'}}/>
                                            </InputGroupText>
                                            <Input style={{backgroundColor: 'inherit'}}
                                                placeholder="Email" name="email" id="email"
                                                value={this.state.email} onChange={this.HandleChange} type="text" 
                                            />
                                        </InputGroup>
                                        <InputErrors field_error_state={this.state.input_errors['email']} field_label='Email' />
                                        <br/><br/>
                                    </Col>
                                </Row>
                                <Row style={{margin: '0px'}}>
                                    <Col sm='6'>
                                        <Label style={{fontWeight: 'bold'}}>Subject <span style={{color: 'red'}}>*</span></Label>
                                        <InputGroup>
                                            <InputGroupText>
                                                <FaRegFolderOpen style={{margin:'10px'}}/>
                                            </InputGroupText>
                                            <Input style={{backgroundColor: 'inherit'}}
                                                placeholder="Subject" name="subject" id="subject"
                                                value={this.state.subject} onChange={this.HandleChange} type="text" 
                                            />
                                        </InputGroup>
                                        <InputErrors field_error_state={this.state.input_errors['subject']} field_label='Subject' />
                                        <br/><br/>
                                    </Col>
                                    <Col>
                                        <Label style={{fontWeight: 'bold'}}>Message <span style={{color: 'red'}}>*</span></Label>
                                        <InputGroup>
                                            <InputGroupText>
                                                <FaEnvelopeOpenText style={{margin:'10px'}}/>
                                            </InputGroupText>
                                            <Input style={{backgroundColor: 'inherit'}}
                                                placeholder="Message" name="message" id="message"
                                                value={this.state.message} onChange={this.HandleChange} type="textarea" rows={5}
                                            />
                                        </InputGroup>
                                        <InputErrors field_error_state={this.state.input_errors['message']} field_label='Message' />
                                        <br/><br/>
                                    </Col>
                                </Row>
                                <br/><br/>
                                <Button type="submit"
                                    style={{backgroundColor: '#ffffff', color: '#005fc9', fontWeight: 'bold', border: '1px solid #005fc9', borderRadius: '20px', width: '180px'}}
                                >
                                    Submit
                                </Button>
                            </Form>
                        </Container>
                    </div>
                }
                <br/><br/><br/>
            </div>
        );
    }

};

export default withCookies(ContactUs);