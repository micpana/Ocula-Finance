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
import { FaUserAlt, FaEnvelope, FaRegFolderOpen, FaEnvelopeOpenText } from 'react-icons/fa';

class ContactUs extends Component{
    static propTypes = {
        cookies: instanceOf(Cookies).isRequired
    };
    constructor(props) { 
        super(props);
        this.state = {
            loading: false,
            input_errors: {},
            name: '',
            email: '',
            subject: '',
            message: ''
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

        this.GetInTouch = () => {

        }
    }

    componentDidMount() {
        
    }

    render() {
        return (
            <div>
                <Helmet>
                    <title>Contact Us | {Platform_Name}</title>
                    {/* <meta name="description" content="" /> */}
                </Helmet>
                {
                    this.state.loading == true
                    ? <LoadingScreen />
                    : <Container>
                        <br/><br/><br/>
                        <h4 style={{fontWeight: 'bold'}}>
                            Contact us
                        </h4>
                        <br/><br/>
                        <h5>We're here to help</h5>
                        <br/>
                        <p>
                            At Ocula Finance, we're committed to providing traders with innovative, data-driven solutions for more 
                            informed trading decisions. If you have any questions, need more information, or require support, 
                            don't hesitate to get in touch.
                        </p>
                        <br/><br/><br/>
                        <h6 style={{fontWeight: 'bold'}}>
                            Contact Information
                        </h6>
                        <br/><br/>
                        <p style={{textAlign: 'left'}}>
                            <span style={{fontWeight: 'bold'}}>Email:</span> <a href="mailto:support@oculafinance.com" style={{color: 'inherit'}}>support@oculafinance.com</a>
                            <br/><br/>
                            <span style={{fontWeight: 'bold'}}>WhatsApp:</span>
                        </p>
                        <br/><br/><br/>
                        <h6 style={{fontWeight: 'bold'}}>
                            Get In Touch
                        </h6>
                        <br/><br/>
                        <p style={{textAlign: 'left'}}>
                            Use the form below to send us your questions, comments or feedback. We aim to respond within 24 hours.
                        </p>
                        <br/>
                        <Form onSubmit={this.GetInTouch}>
                            <Label>Name <span style={{color: 'red'}}>*</span></Label>
                            <InputGroup>
                                <InputGroupAddon addonType="prepend">
                                    <FaUserAlt style={{margin:'10px'}}/>
                                </InputGroupAddon>
                                <Input style={{border: 'none', borderBottom: '1px solid #828884', backgroundColor: 'inherit'}}
                                    placeholder="Name" name="name" id="name"
                                    value={this.state.name} onChange={this.HandleChange} type="text" 
                                />
                            </InputGroup>
                            <InputErrors field_error_state={this.state.input_errors['name']} field_label='Name' />
                            <br/><br/>
                            <Label>Email <span style={{color: 'red'}}>*</span></Label>
                            <InputGroup>
                                <InputGroupAddon addonType="prepend">
                                    <FaEnvelope style={{margin:'10px'}}/>
                                </InputGroupAddon>
                                <Input style={{border: 'none', borderBottom: '1px solid #828884', backgroundColor: 'inherit'}}
                                    placeholder="Email" name="email" id="email"
                                    value={this.state.email} onChange={this.HandleChange} type="text" 
                                />
                            </InputGroup>
                            <InputErrors field_error_state={this.state.input_errors['email']} field_label='Email' />
                            <br/><br/>
                            <Label>Subject <span style={{color: 'red'}}>*</span></Label>
                            <InputGroup>
                                <InputGroupAddon addonType="prepend">
                                    <FaRegFolderOpen style={{margin:'10px'}}/>
                                </InputGroupAddon>
                                <Input style={{border: 'none', borderBottom: '1px solid #828884', backgroundColor: 'inherit'}}
                                    placeholder="Subject" name="subject" id="subject"
                                    value={this.state.subject} onChange={this.HandleChange} type="text" 
                                />
                            </InputGroup>
                            <InputErrors field_error_state={this.state.input_errors['subject']} field_label='Subject' />
                            <br/><br/>
                            <Label>Message <span style={{color: 'red'}}>*</span></Label>
                            <InputGroup>
                                <InputGroupAddon addonType="prepend">
                                    <FaEnvelopeOpenText style={{margin:'10px'}}/>
                                </InputGroupAddon>
                                <Input style={{border: 'none', borderBottom: '1px solid #828884', backgroundColor: 'inherit'}}
                                    placeholder="Message" name="message" id="message"
                                    value={this.state.message} onChange={this.HandleChange} type="textarea" rows={5}
                                />
                            </InputGroup>
                            <InputErrors field_error_state={this.state.input_errors['message']} field_label='Message' />
                            <br/><br/><br/>
                            <Button onClick={this.GetInTouch}
                                style={{border: '1px solid #00539C', borderRadius: '20px', color: '#00539C', fontWeight: 'bold'}}
                            >
                                Submit
                            </Button>
                        </Form>
                    </Container>
                }
                <br/><br/><br/>
            </div>
        );
    }

};

export default withCookies(ContactUs);