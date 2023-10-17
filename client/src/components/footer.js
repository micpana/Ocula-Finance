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
import Instagram from '../images/instagram.png'
import Facebook from '../images/facebook.png'
import Twitter from '../images/twitter.png'
import Logo from '../images/logo.png'

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
                            <a href="mailto:support@oculafinance.com" style={{color: 'inherit'}}>support@oculafinance.com</a>
                            <br/><br/>
                            <a href="tel:+263" style={{color: 'inherit'}}>+263 </a>
                            <br/><br/>
                            <a href="tel:+263" style={{color: 'inherit'}}>+263 </a>
                            <br/><br/>
                            <a href="https://www.google.com/maps/place/21+Mull+Rd,+Harare/@-17.822603,31.0154291,17z/data=!4m5!3m4!1s0x1931a5b3de5b7695:0x5c5e0e4fb34aebb0!8m2!3d-17.8228481!4d31.017886?entry=ttu" target='_blank' style={{color: 'inherit'}}>
                                Harare, Zimbabwe
                            </a>
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
                        </Col>
                        <Col>
                            <br/><br/>
                            <h6 style={{fontWeight: 'bold', color: '#000000'}}>Social Media</h6>
                            <br/>
                            <a href='https://www.facebook.com/' target='_blank' style={{color: 'inherit'}}>
                                Facebook
                            </a>
                            <br/><br/>
                            <a href='https://www.instagram.com/' target='_blank' style={{color: 'inherit'}}>
                                Instagram
                            </a>
                        </Col>
                        <Col sm='4'>
                            
                        </Col>
                    </Row>
                    <br/>
                    <Row style={{marginTop: '20px'}}>
                        <Col>
                            <Col sm='3' style={{alignItems: 'left', textAlign: 'left', justifyContent: 'left'}}>
                                <Row style={{marginTop: '15px'}}>
                                    <Col xs='5'>
                                        <a href='https://www.facebook.com/' target='_blank'><img src={Facebook} style={{width: '80%'}} /></a>
                                    </Col>
                                    <Col xs='5'>
                                        <a href='https://www.instagram.com/' target='_blank'><img src={Instagram} style={{width: '80%'}} /></a>
                                    </Col>
                                </Row>
                            </Col>
                        </Col>
                        <Col>
                            Copyright 2023 &copy; {Platform_Name}
                        </Col>
                    </Row>
                    <br/>
                </Container>
            </div>
        );
    }
};

export default Footer;