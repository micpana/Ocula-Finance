import React, { Component, useReducer } from 'react';
import {
    Collapse, 
    Nav, NavItem, NavLink, 
    UncontrolledDropdown, Dropdown, DropdownToggle, DropdownMenu, DropdownItem, 
    Input, InputGroup, InputGroupText,
    Button, Row, Col, Form, Container, Label
} from "reactstrap";
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
import Logo from '../images/logo.png'
import {Facebook, X, Instagram, LinkedIn, Telegram } from '../social_links'
import { FaMailBulk, Whatsapp, FaTelegram, FaPhone, FaSearchLocation, FaFacebook, FaTwitter, FaLinkedin, FaInstagram, FaWhatsapp, FaLocationArrow, FaPhoneAlt } from 'react-icons/fa';

class Footer extends Component{
    constructor(props) { 
        super(props);
        this.state = {

        };
    }

    componentDidMount() {
    
    }

    render() {
        return (
            <div  style={{minHeight: '250px', backgroundColor: '#EEECEC'}}>
                <Container>
                    <Row style={{textAlign: 'left', color: ''}}>
                        <Col sm='4'>
                            <br/><br/>
                            <h6 style={{fontWeight: 'bold', color: '#000000'}}>Get In Touch</h6>
                            <br/>
                            <FaMailBulk /> <a href="mailto:support@oculafinance.com" style={{color: 'inherit'}}>support@oculafinance.com</a>
                            <br/><br/>
                            <FaWhatsapp /> <a href="https://wa.me/+263784111412" style={{color: 'inherit'}}>+263 784 111 412</a>
                            <br/><br/>
                            <FaTelegram /> <a href={Telegram} style={{color: 'inherit'}}>+263 784 111 412</a>
                            {/* <br/><br/>
                            <FaPhoneAlt /> <a href="tel:+263784111412" style={{color: 'inherit'}}>+263 784 111 412</a> */}
                        </Col>
                        <Col sm='3'>
                            <br/><br/>
                            <h6 style={{fontWeight: 'bold', color: '#000000'}}>Quick Links</h6>
                            <br/>
                            <a href='/' style={{color: 'inherit'}}>
                                Home
                            </a>
                            <br/><br/>
                            <a href='/how-it-works' style={{color: 'inherit'}}>
                                How it works
                            </a>
                            <br/><br/>
                            <a href='/pricing' style={{color: 'inherit'}}>
                                Pricing
                            </a>
                            <br/><br/>
                            <a href='/about-us' style={{color: 'inherit'}}>
                                About us
                            </a>
                            <br/><br/>
                            <a href='/contact-us' style={{color: 'inherit'}}>
                                Contact us
                            </a>
                            <br/><br/>
                            <a href='/ai-performance' style={{color: 'inherit'}}>
                                AI Performance
                            </a>
                            <br/><br/>
                            <a href='/signin' style={{color: 'inherit'}}>
                                Signin
                            </a>
                            <br/><br/>
                            <a href='/signup' style={{color: 'inherit'}}>
                                Signup
                            </a>
                        </Col>
                        <Col>
                            <br/><br/>
                            <h6 style={{fontWeight: 'bold', color: '#000000'}}>Social Media</h6>
                            <br/>
                            <FaFacebook /> <a href={Facebook} target='_blank'  rel='noreferrer' style={{color: 'inherit'}}>
                                Facebook
                            </a>
                            <br/><br/>
                            <FaTwitter /> <a href={X} target='_blank'  rel='noreferrer' style={{color: 'inherit'}}>
                                X
                            </a>
                            <br/><br/>
                            <FaInstagram /> <a href={Instagram} target='_blank'  rel='noreferrer' style={{color: 'inherit'}}>
                                Instagram
                            </a>
                            <br/><br/>
                            <FaLinkedin /> <a href={LinkedIn} target='_blank'  rel='noreferrer' style={{color: 'inherit'}}>
                                LinkedIn
                            </a>
                        </Col>
                        <Col sm=''>
                            <br/><br/>
                            <h6 style={{fontWeight: 'bold', color: '#000000'}}>Terms and Privacy Policy</h6>
                            <br/>
                            <a href='/terms-of-service' style={{color: 'inherit'}}>
                                Terms of Service
                            </a>
                            <br/><br/>
                            <a href='/privacy-policy' style={{color: 'inherit'}}>
                                Privacy Policy
                            </a>
                        </Col>
                    </Row>
                    <br/>
                    <Row style={{marginTop: '20px'}}>
                        <Col sm='6'>
                            <Col sm='3' style={{alignItems: 'left', textAlign: 'left', justifyContent: 'left'}}>

                            </Col>
                        </Col>
                        <Col>
                            Copyright 2025 &copy; {Platform_Name}
                        </Col>
                    </Row>
                    <br/>
                </Container>
            </div>
        );
    }
};

export default Footer;